"""Tests for optional local ONNX slop detection and clear-trigger analysis."""

from __future__ import annotations

import builtins
import json
from pathlib import Path
import sys

import pytest

from stylint import slop
from stylint.cli import main as cli_main
from stylint.config import ConfigError, parse_config
from stylint.lint import check_page
from stylint.tags import Tag


class _FakeEncoded:
    def __init__(self, ids: list[int]) -> None:
        self.ids = ids


class _FakeTokenizer:
    def encode(self, text: str, add_special_tokens: bool = False) -> _FakeEncoded:
        # Represent each whitespace-separated word as 1 token id.
        words = text.split()
        return _FakeEncoded(list(range(1, len(words) + 1)))

    def token_to_id(self, token: str) -> int:
        return 0


class _FakeNp:
    int64 = "int64"

    class _Array:
        def __init__(self, data) -> None:
            self.data = data

        def reshape(self, *args):
            return self.data

    @classmethod
    def array(cls, data, dtype=None):
        return cls._Array(data)

    @classmethod
    def ones_like(cls, arr):
        return arr


class _FakeSession:
    """Fake ONNX session whose logit is determined by token count or callback."""

    def __init__(self, score_fn) -> None:
        self._score_fn = score_fn
        self.calls: list[int] = []

    def run(self, outputs, feeds):
        arr = feeds["input_ids"].data
        # Strip BOS token (index 0)
        tokens = arr[0][1:]
        self.calls.append(len(tokens))
        logit = self._score_fn(tokens)
        return [_FakeNp._Array([logit])]


def _make_engine(score_fn, tmp_path: Path | None = None):
    bands = {"human_max": 0.15, "generated_min": 0.75}
    return (_FakeNp, _FakeTokenizer(), _FakeSession(score_fn), bands, tmp_path or Path("."))


def test_empty_text_does_not_load_engine(monkeypatch):
    called = {"n": 0}
    monkeypatch.setattr(slop, "_load_engine", lambda *a, **k: called.__setitem__("n", 1))
    res, findings = slop.check_slop("   \n\t ", Path("post.md"))
    assert res.score == 0.0
    assert findings == []
    assert called["n"] == 0


def test_missing_dependencies_raises_actionable_error(monkeypatch, tmp_path):
    monkeypatch.setattr(slop, "_ENGINE", None)
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name in ("onnxruntime", "tokenizers", "numpy"):
            raise ImportError(f"No module named {name}")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(slop.SlopUnavailableError) as exc:
        slop._load_engine(model_dir=tmp_path, download=False)

    assert 'pip install "stylint[slop]"' in str(exc.value)


def test_missing_model_files_without_download_raises(monkeypatch, tmp_path):
    monkeypatch.setattr(slop, "_ENGINE", None)
    # Provide fake modules so import succeeds, then fail on missing files.
    monkeypatch.setitem(sys.modules, "numpy", _FakeNp)
    monkeypatch.setitem(sys.modules, "onnxruntime", type("ort", (), {}))
    monkeypatch.setitem(sys.modules, "tokenizers", type("tok", (), {"Tokenizer": object}))

    with pytest.raises(slop.SlopUnavailableError) as exc:
        slop._load_engine(model_dir=tmp_path, download=False)

    assert "model_quantized.onnx" in str(exc.value)


def test_resolve_model_dir_env_and_shared_fallback(monkeypatch, tmp_path):
    custom = tmp_path / "custom-model"
    monkeypatch.setenv("STYLINT_SLOP_MODEL_DIR", str(custom))
    assert slop.resolve_model_dir() == custom

    monkeypatch.delenv("STYLINT_SLOP_MODEL_DIR")
    monkeypatch.setenv("SLOP_DETECT_MODEL_DIR", str(tmp_path / "shared-env"))
    assert slop.resolve_model_dir() == tmp_path / "shared-env"

    monkeypatch.delenv("SLOP_DETECT_MODEL_DIR")
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    shared = tmp_path / ".local" / "share" / "slop-detect" / "model"
    shared.mkdir(parents=True)
    for name in slop.REQUIRED_LOCAL_FILES:
        (shared / name).write_text("x")
    assert slop.resolve_model_dir() == shared


def test_score_text_strips_code_fences_and_chunks_long_text():
    # Logit = -3.0 for <= 10 tokens (prob ~0.047), +2.0 for > 10 tokens (prob ~0.881)
    engine = _make_engine(lambda toks: 2.0 if len(toks) > 10 else -3.0)

    # Code block has 50 words, prose has 4 words -> code block must be emptied.
    code_heavy = "Short prose here.\n\n```python\n" + " ".join(["x"] * 50) + "\n```\n"
    res = slop.score_text(code_heavy, engine=engine)
    assert res.chunks == 1
    assert res.score < 0.10
    assert res.band == "human"

    # 600 words -> 2 chunks (510 + 90). Both > 10 -> ai-generated.
    long_text = " ".join(["word"] * 600)
    res_long = slop.score_text(long_text, engine=engine)
    assert res_long.chunks == 2
    assert res_long.score > 0.75
    assert res_long.band == "ai-generated"


def test_clear_trigger_analysis_pinpoints_triggering_sentence_and_line():
    # A sentence containing "landscape" drives the logit to +1.0 (~0.731);
    # without it, logit is -3.0 (~0.047).
    class _WordTokenizer:
        def encode(self, text: str, add_special_tokens: bool = False):
            words = text.lower().split()
            return _FakeEncoded([1 if "landscape" in w else 2 for w in words])

        def token_to_id(self, token: str) -> int:
            return 0

    engine = (
        _FakeNp,
        _WordTokenizer(),
        _FakeSession(lambda toks: 1.0 if 1 in toks else -3.0),
        {"human_max": 0.15, "generated_min": 0.75},
        Path("."),
    )

    body = (
        "We ran the benchmark on a 4-core VM.\n"
        "In today's fast-paced landscape, this robust tool unlocks value.\n"
        "Total runtime dropped from 12s to 4s.\n"
    )
    score_res, findings = slop.check_slop(
        body, Path("post.md"), line_offset=4, threshold=0.10, engine=engine
    )

    assert score_res.score > 0.70
    assert score_res.band == "ai-edited"
    assert findings[0].tag == Tag.SLOP_SCORE
    assert findings[0].line is None

    trigger_findings = [f for f in findings if f.tag == Tag.SLOP_TRIGGER]
    assert len(trigger_findings) == 1
    # Line 2 in body + line_offset 4 = line 6 in original file.
    assert trigger_findings[0].line == 6
    assert "landscape" in trigger_findings[0].message
    assert "drops slop score by -" in trigger_findings[0].message


def test_clear_trigger_analysis_handles_multi_paragraph_and_masking():
    # Two paragraphs both contain "delve" -> removing one paragraph doesn't
    # lower max doc score, so fallback standalone paragraph scoring must still
    # pinpoint the triggering sentences in each paragraph.
    class _WordTokenizer:
        def encode(self, text: str, add_special_tokens: bool = False):
            words = text.lower().split()
            return _FakeEncoded([1 if "delve" in w else 2 for w in words])

        def token_to_id(self, token: str) -> int:
            return 0

    engine = (
        _FakeNp,
        _WordTokenizer(),
        _FakeSession(lambda toks: 1.0 if 1 in toks else -3.0),
        {"human_max": 0.15, "generated_min": 0.75},
        Path("."),
    )

    body = (
        "First concrete sentence. Let us delve into the details.\n\n"
        "Another concrete note. We delve deeper here too.\n"
    )
    _, findings = slop.check_slop(body, Path("post.md"), threshold=0.10, engine=engine)
    triggers = [f for f in findings if f.tag == Tag.SLOP_TRIGGER]
    assert len(triggers) == 2
    assert {f.line for f in triggers} == {1, 3}


def test_check_page_with_slop_respects_frontmatter_offset(monkeypatch, tmp_path):
    class _WordTokenizer:
        def encode(self, text: str, add_special_tokens: bool = False):
            words = text.lower().split()
            return _FakeEncoded([1 if "tapestry" in w else 2 for w in words])

        def token_to_id(self, token: str) -> int:
            return 0

    engine = (
        _FakeNp,
        _WordTokenizer(),
        _FakeSession(lambda toks: 1.5 if 1 in toks else -3.0),
        {"human_max": 0.15, "generated_min": 0.75},
        tmp_path,
    )
    monkeypatch.setattr(slop, "_load_engine", lambda *a, **k: engine)

    page = tmp_path / "post.md"
    page.write_text(
        "---\ntitle: Test\n---\n\nPlain opening.\nThis weaves a rich tapestry.\n",
        encoding="utf-8",
    )
    findings = check_page(tmp_path, page, slop=True, slop_threshold=0.10)
    trigger_lines = [f.line for f in findings if f.tag == Tag.SLOP_TRIGGER]
    assert trigger_lines == [6]


def test_cli_slop_flags_and_explain(monkeypatch, capsys, tmp_path):
    # --explain works for both slop tags
    for tag in ("slop-score", "slop-trigger"):
        monkeypatch.setattr(sys, "argv", ["stylint", "--explain", tag])
        assert cli_main() == 0
        assert tag in capsys.readouterr().out

    # Invalid --slop-threshold returns 2
    page = tmp_path / "post.md"
    page.write_text("Plain text.\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["stylint", "--slop", "--slop-threshold", "1.5", str(page)])
    assert cli_main() == 2
    assert "Invalid --slop-threshold" in capsys.readouterr().err

    # --slop with mocked engine
    class _WordTokenizer:
        def encode(self, text: str, add_special_tokens: bool = False):
            words = text.lower().split()
            return _FakeEncoded([1 if "unlock" in w else 2 for w in words])

        def token_to_id(self, token: str) -> int:
            return 0

    engine = (
        _FakeNp,
        _WordTokenizer(),
        _FakeSession(lambda toks: 1.5 if 1 in toks else -3.0),
        {"human_max": 0.15, "generated_min": 0.75},
        tmp_path,
    )
    monkeypatch.setattr(slop, "_load_engine", lambda *a, **k: engine)

    monkeypatch.setattr(sys, "argv", ["stylint", "--no-next", "--slop", str(page)])
    assert cli_main() == 0
    assert "Style check passed" in capsys.readouterr().out

    page.write_text("This will unlock everything.\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["stylint", "--no-next", "--slop", str(page)])
    assert cli_main() == 1
    out = capsys.readouterr().out
    assert "[slop-score]" in out
    assert "[slop-trigger]" in out


def test_config_slop_threshold(tmp_path):
    cfg = parse_config({"slop_threshold": 0.25}, tmp_path / "pyproject.toml")
    assert cfg.slop_threshold == 0.25

    with pytest.raises(ConfigError):
        parse_config({"slop_threshold": 1.5}, tmp_path / "pyproject.toml")
    with pytest.raises(ConfigError):
        parse_config({"slop_threshold": True}, tmp_path / "pyproject.toml")
