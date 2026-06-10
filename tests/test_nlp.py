"""Tests for the optional NLP-based checks (stylint/nlp.py)."""

import builtins

import pytest

from stylint import nlp
from stylint.tags import Tag


def _tags(line):
    return [f.tag for f in nlp.check_line(line)]


def test_flags_simple_passive():
    findings = nlp.check_line("the file was deleted by the script")
    assert [f.tag for f in findings] == [Tag.PASSIVE_VOICE]
    assert "active voice" in findings[0].message
    assert "deleted" in findings[0].span


def test_flags_agentless_passive():
    assert _tags("mistakes were made") == [Tag.PASSIVE_VOICE]


def test_does_not_flag_active_voice():
    assert _tags("the script deletes the file") == []


def test_allowlist_suppresses_predicate_idioms():
    # "is based on" and "is done" are stative idioms, not true passives.
    assert _tags("the pipeline is based on a queue") == []
    assert _tags("the migration is done") == []


def test_blank_line_does_not_touch_engine(monkeypatch):
    # check_line on empty/whitespace must short-circuit before loading.
    called = {"n": 0}
    monkeypatch.setattr(nlp, "_load_engine", lambda: called.__setitem__("n", 1))
    assert nlp.check_line("   ") == []
    assert called["n"] == 0


def test_missing_nltk_raises_actionable_error(monkeypatch):
    # Reset the cached engine so _load_engine re-imports.
    monkeypatch.setattr(nlp, "_TAGGER", None)
    monkeypatch.setattr(nlp, "_TOKENIZE", None)

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "nltk" or name.startswith("nltk."):
            raise ImportError("No module named nltk")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(nlp.NlpUnavailableError) as exc:
        nlp.check_line("the file was deleted")

    msg = str(exc.value)
    assert 'pip install "stylint[nlp]"' in msg
    assert "nltk.downloader" in msg
