"""Optional local ONNX slop detection (VoightKampffLabs/voi-slop-detect-380M).

Enabled only when the user passes ``--slop`` (or calls ``check_page(..., slop=True)``).
Kept out of the base install so default runs stay light and fast.

Design notes:
- ``onnxruntime``, ``numpy``, ``tokenizers``, and ``huggingface_hub`` are
  imported lazily in ``_load_engine`` so importing this module has zero
  runtime cost when ``--slop`` is off.
- Uses the same model, chunking (510 tokens + BOS, up to 40 chunks, max chunk
  score), fenced-code-block stripping, and 0.10 default threshold as
  ``bots-management/tools/slop-detect``.
- When a file's score meets or exceeds the threshold, runs hierarchical
  leave-one-out (ablation) clear-trigger analysis to pinpoint the exact
  sentences or paragraphs driving the score.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
import os
from pathlib import Path
import re
import shutil
from typing import Any

from .models import Finding
from .tags import Tag

REPO_ID = "VoightKampffLabs/voi-slop-detect-380M"
MODEL_FILES = (
    "onnx/model_quantized.onnx",
    "onnx/model_quantized.onnx_data",
    "tokenizer.json",
    "tokenizer_config.json",
    "bands.json",
    "config.json",
)
REQUIRED_LOCAL_FILES = (
    "model_quantized.onnx",
    "model_quantized.onnx_data",
    "tokenizer.json",
    "bands.json",
)

DEFAULT_THRESHOLD = 0.10
CHUNK_TOKENS = 510
MAX_CHUNKS = 40
MIN_TRIGGER_DELTA = 0.02
MAX_TRIGGERS = 5
MAX_ABLATION_PARAGRAPHS = 40

FENCE_RE = re.compile(r"```.*?```", re.S)
_FENCE_LINE_RE = re.compile(r"^\s*(?:```|~~~)")
_HR_RE = re.compile(r"^\s*(?:[-*_]\s*){3,}$")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[\"'(\[]?[A-Z0-9])")


class SlopUnavailableError(RuntimeError):
    """Raised when --slop is requested but dependencies or model files are
    missing. Carries an actionable, install-focused message."""


_INSTALL_HINT = (
    "Slop detection requires the optional 'slop' extra.\n"
    "  Install it with:  pip install \"stylint[slop]\"\n"
    "The model (VoightKampffLabs/voi-slop-detect-380M, ~433 MB) is\n"
    "downloaded automatically on first use, or set STYLINT_SLOP_MODEL_DIR\n"
    "to a directory containing model_quantized.onnx, model_quantized.onnx_data,\n"
    "tokenizer.json, and bands.json."
)

# Cached engine: (np, tokenizer, ort_session, bands_dict, model_dir)
_ENGINE: tuple[Any, Any, Any, dict[str, float], Path] | None = None


@dataclass(frozen=True)
class SlopScore:
    """Model score summary for a document."""

    score: float
    mean_score: float
    chunks: int
    chunk_scores: tuple[float, ...]
    band: str


@dataclass(frozen=True)
class SlopTrigger:
    """A sentence or paragraph identified as a clear trigger by ablation."""

    line: int
    text: str
    delta: float
    base_score: float
    without_score: float
    kind: str  # "sentence" or "paragraph"
    standalone_score: float | None = None


@dataclass(frozen=True)
class _ProseBlock:
    start_line: int
    lines: tuple[tuple[int, str], ...]

    @property
    def text(self) -> str:
        return "\n".join(line for _, line in self.lines)


def resolve_model_dir() -> Path:
    """Return the directory where the quantized ONNX model files live."""
    for env_var in ("STYLINT_SLOP_MODEL_DIR", "SLOP_DETECT_MODEL_DIR"):
        override = os.environ.get(env_var, "").strip()
        if override:
            return Path(override).expanduser()

    shared = Path.home() / ".local" / "share" / "slop-detect" / "model"
    if all((shared / name).is_file() for name in REQUIRED_LOCAL_FILES):
        return shared

    return Path.home() / ".cache" / "stylint" / "voi-slop-detect-380M"


def _ensure_model_files(model_dir: Path, *, download: bool = True) -> None:
    """Ensure all required ONNX and tokenizer files exist in ``model_dir``."""
    missing = [name for name in REQUIRED_LOCAL_FILES if not (model_dir / name).is_file()]
    if not missing:
        return

    no_dl = os.environ.get("STYLINT_SLOP_NO_DOWNLOAD", "").strip().lower()
    if not download or no_dl not in ("", "0", "false", "no"):
        raise SlopUnavailableError(
            f"Slop model files missing in {model_dir}: {', '.join(missing)}.\n"
            f"{_INSTALL_HINT}"
        )

    try:
        from huggingface_hub import hf_hub_download
    except ImportError as exc:
        raise SlopUnavailableError(
            f"Could not import huggingface_hub to download {REPO_ID}: {exc}.\n"
            f"{_INSTALL_HINT}"
        ) from exc

    model_dir.mkdir(parents=True, exist_ok=True)
    try:
        for rel_file in MODEL_FILES:
            dest = model_dir / os.path.basename(rel_file)
            if dest.is_file():
                continue
            cached = Path(hf_hub_download(REPO_ID, rel_file))
            shutil.copyfile(os.path.realpath(cached), dest)
    except Exception as exc:
        raise SlopUnavailableError(
            f"Failed to download {REPO_ID} into {model_dir}: {exc}.\n"
            f"{_INSTALL_HINT}"
        ) from exc


def _load_engine(model_dir: Path | None = None, *, download: bool = True):
    """Import onnxruntime/tokenizers/numpy and load the ONNX session. Cached."""
    global _ENGINE
    target_dir = model_dir if model_dir is not None else resolve_model_dir()
    if _ENGINE is not None and _ENGINE[4] == target_dir:
        return _ENGINE

    try:
        import numpy as np
        import onnxruntime as ort
        from tokenizers import Tokenizer
    except ImportError as exc:
        raise SlopUnavailableError(
            f"Could not import slop detection dependencies: {exc}.\n{_INSTALL_HINT}"
        ) from exc

    _ensure_model_files(target_dir, download=download)

    try:
        tok = Tokenizer.from_file(str(target_dir / "tokenizer.json"))
        opts = ort.SessionOptions()
        opts.log_severity_level = 3
        sess = ort.InferenceSession(
            str(target_dir / "model_quantized.onnx"),
            opts,
            providers=["CPUExecutionProvider"],
        )
        bands = json.loads((target_dir / "bands.json").read_text(encoding="utf-8"))
    except Exception as exc:
        raise SlopUnavailableError(
            f"Failed to load slop model from {target_dir}: {exc}.\n{_INSTALL_HINT}"
        ) from exc

    _ENGINE = (np, tok, sess, bands, target_dir)
    return _ENGINE


def _classify_band(score: float, bands: dict[str, float]) -> str:
    if score < bands["human_max"]:
        return "human"
    return "ai-generated" if score >= bands["generated_min"] else "ai-edited"


def score_text(text: str, *, engine: Any = None) -> SlopScore:
    """Score ``text`` with voi-slop-detect-380M.

    Fenced code blocks are emptied as in training, and text longer than 510
    tokens is scored in chunks (up to 40) taking the maximum chunk score.
    """
    if not text.strip():
        return SlopScore(0.0, 0.0, 0, (), "human")

    np, tok, sess, bands, _ = engine if engine is not None else _load_engine()
    cleaned = FENCE_RE.sub("```\n```", text)
    ids = tok.encode(cleaned, add_special_tokens=False).ids
    bos = tok.token_to_id("<|endoftext|>")
    chunks = [
        ids[i : i + CHUNK_TOKENS]
        for i in range(0, max(len(ids), 1), CHUNK_TOKENS)
    ][:MAX_CHUNKS]

    scores: list[float] = []
    for chunk in chunks:
        arr = np.array([[bos] + chunk], dtype=np.int64)
        logits = sess.run(
            ["logits"],
            {"input_ids": arr, "attention_mask": np.ones_like(arr)},
        )[0]
        raw_logit = float(logits.reshape(-1)[0])
        prob = 1.0 / (1.0 + math.exp(-raw_logit))
        scores.append(prob)

    max_score = max(scores)
    mean_score = sum(scores) / len(scores)
    return SlopScore(
        score=max_score,
        mean_score=mean_score,
        chunks=len(scores),
        chunk_scores=tuple(scores),
        band=_classify_band(max_score, bands),
    )


def _extract_prose_blocks(body: str, *, line_offset: int = 0) -> list[_ProseBlock]:
    """Split markdown body into contiguous prose blocks outside code fences."""
    blocks: list[_ProseBlock] = []
    current: list[tuple[int, str]] = []
    in_code = False

    def flush() -> None:
        if not current:
            return
        joined = "\n".join(line for _, line in current).strip()
        if joined and not _HR_RE.match(joined) and not (
            joined.startswith("<!--") and joined.endswith("-->")
        ):
            blocks.append(_ProseBlock(start_line=current[0][0], lines=tuple(current)))
        current.clear()

    for idx, line in enumerate(body.splitlines(), start=1):
        file_line = idx + line_offset
        if _FENCE_LINE_RE.match(line):
            flush()
            in_code = not in_code
            continue
        if in_code:
            continue
        if not line.strip():
            flush()
            continue
        current.append((file_line, line))
    flush()
    return blocks


def _split_block_sentences(block: _ProseBlock) -> list[tuple[int, str]]:
    """Split a prose block into (start_line, sentence_text) pairs."""
    if len(block.lines) == 1:
        text = block.lines[0][1].strip()
        parts = _SENTENCE_SPLIT_RE.split(text)
        return [(block.lines[0][0], p.strip()) for p in parts if p.strip()]

    # Build a single string while tracking which file line each character came from.
    char_lines: list[int] = []
    pieces: list[str] = []
    for i, (line_no, line_text) in enumerate(block.lines):
        stripped = line_text.strip()
        if not stripped:
            continue
        if pieces:
            pieces.append(" ")
            char_lines.append(line_no)
        pieces.append(stripped)
        char_lines.extend([line_no] * len(stripped))

    full_text = "".join(pieces)
    if not full_text:
        return []

    sentences: list[tuple[int, str]] = []
    start = 0
    for match in _SENTENCE_SPLIT_RE.finditer(full_text):
        seg = full_text[start : match.start()].strip()
        if seg:
            sentences.append((char_lines[start], seg))
        start = match.end()
    tail = full_text[start:].strip()
    if tail:
        sentences.append((char_lines[start], tail))
    return sentences


def _truncate_snippet(text: str, limit: int = 120) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 3] + "..."


def analyze_triggers(
    body: str,
    *,
    base_score: SlopScore | None = None,
    line_offset: int = 0,
    threshold: float = DEFAULT_THRESHOLD,
    min_delta: float = MIN_TRIGGER_DELTA,
    max_triggers: int = MAX_TRIGGERS,
    engine: Any = None,
) -> list[SlopTrigger]:
    """Identify sentences or paragraphs that clearly drive a high slop score.

    Uses hierarchical leave-one-out ablation:
    1. If there are multiple paragraphs, measure how removing each paragraph
       changes the document score (falling back to standalone paragraph scores
       when multiple chunks mask single-paragraph removals).
    2. Within the top triggering paragraphs (or the sole paragraph), measure how
       removing each sentence changes the paragraph/document score.
    """
    eng = engine if engine is not None else _load_engine()
    doc_score = base_score if base_score is not None else score_text(body, engine=eng)
    blocks = _extract_prose_blocks(body, line_offset=line_offset)
    if not blocks:
        return []

    triggers: list[SlopTrigger] = []

    if len(blocks) == 1:
        candidate_blocks = [(blocks[0], doc_score.score, 0.0)]
    else:
        para_results: list[tuple[_ProseBlock, float, float]] = []
        for idx, block in enumerate(blocks[:MAX_ABLATION_PARAGRAPHS]):
            without_text = "\n\n".join(
                b.text for j, b in enumerate(blocks) if j != idx
            )
            without_score = (
                score_text(without_text, engine=eng).score
                if without_text.strip()
                else 0.0
            )
            delta = doc_score.score - without_score
            para_results.append((block, delta, without_score))

        positive = [item for item in para_results if item[1] > 0]
        if positive:
            positive.sort(key=lambda item: item[1], reverse=True)
            candidate_blocks = [
                (b, doc_score.score, d) for b, d, _ in positive[:3]
            ]
        else:
            # Multi-chunk documents can mask single-paragraph ablation; score
            # paragraphs standalone so we still inspect the highest-slop ones.
            scored = [
                (b, score_text(b.text, engine=eng).score)
                for b in blocks[:MAX_ABLATION_PARAGRAPHS]
            ]
            scored.sort(key=lambda item: item[1], reverse=True)
            candidate_blocks = [
                (b, s, 0.0) for b, s in scored[:3] if s >= threshold
            ]
            if not candidate_blocks and scored:
                candidate_blocks = [(scored[0][0], scored[0][1], 0.0)]

    for block, _, para_delta in candidate_blocks:
        sentences = _split_block_sentences(block)
        ref_text = body if len(blocks) == 1 else block.text
        ref_base = doc_score.score if len(blocks) == 1 else score_text(block.text, engine=eng).score

        if len(sentences) <= 1:
            standalone = score_text(block.text, engine=eng).score
            triggers.append(
                SlopTrigger(
                    line=block.start_line,
                    text=_truncate_snippet(block.text),
                    delta=para_delta if len(blocks) > 1 else ref_base,
                    base_score=doc_score.score if len(blocks) > 1 else ref_base,
                    without_score=(doc_score.score - para_delta) if len(blocks) > 1 else 0.0,
                    kind="paragraph",
                    standalone_score=standalone,
                )
            )
            continue

        sent_results: list[tuple[int, str, float, float]] = []
        for s_idx, (s_line, s_text) in enumerate(sentences):
            without_sent = " ".join(
                text for j, (_, text) in enumerate(sentences) if j != s_idx
            )
            if len(blocks) == 1:
                without_full = without_sent
            else:
                without_full = without_sent
            without_s_score = (
                score_text(without_full, engine=eng).score
                if without_full.strip()
                else 0.0
            )
            s_delta = ref_base - without_s_score
            sent_results.append((s_line, s_text, s_delta, without_s_score))

        sent_results.sort(key=lambda item: item[2], reverse=True)
        clear = [item for item in sent_results if item[2] >= min_delta]
        if not clear:
            clear = [item for item in sent_results if item[2] > 0][:2]

        if clear:
            for s_line, s_text, s_delta, without_s_score in clear:
                triggers.append(
                    SlopTrigger(
                        line=s_line,
                        text=_truncate_snippet(s_text),
                        delta=s_delta,
                        base_score=ref_base,
                        without_score=without_s_score,
                        kind="sentence",
                    )
                )
        else:
            # No single sentence removal reduced the score; report the paragraph.
            triggers.append(
                SlopTrigger(
                    line=block.start_line,
                    text=_truncate_snippet(block.text),
                    delta=para_delta,
                    base_score=doc_score.score,
                    without_score=doc_score.score - para_delta,
                    kind="paragraph",
                    standalone_score=ref_base,
                )
            )

    seen: set[tuple[int, str]] = set()
    unique: list[SlopTrigger] = []
    triggers.sort(key=lambda t: (t.delta, t.standalone_score or 0.0), reverse=True)
    for t in triggers:
        key = (t.line, t.text)
        if key in seen:
            continue
        seen.add(key)
        unique.append(t)
        if len(unique) >= max_triggers:
            break
    return unique


def check_slop(
    body: str,
    rel: Path,
    *,
    line_offset: int = 0,
    threshold: float = DEFAULT_THRESHOLD,
    engine: Any = None,
) -> tuple[SlopScore, list[Finding]]:
    """Score ``body`` and return ``(SlopScore, findings)`` for ``rel``."""
    if not body.strip():
        return SlopScore(0.0, 0.0, 0, (), "human"), []

    eng = engine if engine is not None else _load_engine()
    result = score_text(body, engine=eng)
    if result.score < threshold:
        return result, []

    findings: list[Finding] = [
        Finding(
            rel,
            None,
            Tag.SLOP_SCORE,
            (
                f"slop score {result.score:.3f} >= threshold {threshold:.2f} "
                f"({result.band}, mean {result.mean_score:.3f}, "
                f"{result.chunks} chunk(s))"
            ),
        )
    ]

    triggers = analyze_triggers(
        body,
        base_score=result,
        line_offset=line_offset,
        threshold=threshold,
        engine=eng,
    )
    for trig in triggers:
        if trig.delta > 0:
            msg = (
                f"removing {trig.kind} drops slop score by -{trig.delta:.3f} "
                f"({trig.base_score:.3f} -> {trig.without_score:.3f}): \"{trig.text}\""
            )
        else:
            standalone = (
                f"standalone {trig.standalone_score:.3f}"
                if trig.standalone_score is not None
                else f"score {trig.base_score:.3f}"
            )
            msg = f"high-slop {trig.kind} ({standalone}): \"{trig.text}\""
        findings.append(Finding(rel, trig.line, Tag.SLOP_TRIGGER, msg))

    return result, findings
