#!/usr/bin/env python3
"""Describe reference prose and lint AI candidates without rewriting either.

Run from the checkout with `uv run python tools/voice_compare.py --help`.
The numbers are diagnostics, not a voice score or an authorship detector.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import statistics

from stylint import check_page
from stylint.discovery import iter_markdown_pages
from stylint.tags import DEFAULT_OFF_TAGS
from stylint.version import __version__


WORD = re.compile(r"\b\w+(?:['’]\w+)*\b")
LINK = re.compile(r"\[([^\]\n]*)\]\((?:[^()\n]|\([^()\n]*\))*\)")
IMAGE = re.compile(r"!\[[^\]\n]*\]\((?:[^()\n]|\([^()\n]*\))*\)")
LIST = re.compile(r"^\s*(?:[-*+] |\d+[.)] )")
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")


def prose_blocks(text: str) -> list[str]:
    """Extract paragraph prose, excluding lists and other structural blocks.

    This deliberately small Markdown heuristic is not a CommonMark parser.
    Keep inline code identifiers and link labels; omit standalone link cards.
    Lists are excluded to avoid counting command/roadmap items as sentences.
    """
    text = re.sub(r"\A---\r?\n.*?\r?\n---(?:\r?\n|$)", "", text, count=1, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    blocks: list[str] = []
    pending: list[str] = []
    fence_char = ""
    fence_size = 0
    in_list = False

    def flush() -> None:
        if pending:
            blocks.append(" ".join(pending))
            pending.clear()

    for line in text.splitlines():
        stripped = line.strip()
        fence = FENCE.match(line)
        if fence_char:
            if fence and fence.group(1)[0] == fence_char and len(fence.group(1)) >= fence_size:
                if not line[fence.end():].strip():
                    fence_char = ""
            continue
        if fence:
            flush()
            fence_char = fence.group(1)[0]
            fence_size = len(fence.group(1))
            continue
        if not stripped:
            flush()
            in_list = False
            continue
        if LIST.match(line):
            flush()
            in_list = True
            continue
        if in_list and line.startswith((" ", "\t")):
            continue
        in_list = False
        if (stripped.startswith(("#", ">", "|", "![", "[![", "[^"))
                or re.fullmatch(r"[-*_ ]{3,}", stripped)
                or LINK.fullmatch(stripped)
                or re.fullmatch(r"<?https?://\S+>?", stripped)
                or line.startswith(("    ", "\t"))):
            flush()
            continue
        line = IMAGE.sub("", line)
        line = LINK.sub(r"\1", line)
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"https?://\S+", "", line)
        line = re.sub(r"[`*_]", "", line).strip()
        if WORD.search(line):
            pending.append(line)
    flush()
    return blocks


def sentences(paragraph: str) -> list[str]:
    # Protect periods inside decimals and dotted identifiers. Abbreviations
    # such as "Dr." still need judgment; this is a descriptive approximation.
    protected = re.sub(r"(?<=\w)\.(?=\w)", "\x00", paragraph)
    return [part.replace("\x00", ".").strip()
            for part in re.split(r"(?<=[.!?])\s+", protected) if WORD.search(part)]


def percentile(values: list[int], fraction: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    return round(ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower), 3)


def features(text: str) -> dict[str, int | float]:
    blocks = prose_blocks(text)
    parts = [sentence for block in blocks for sentence in sentences(block)]
    tokens = WORD.findall(" ".join(blocks).lower())
    if not tokens:
        return {"words": 0, "paragraphs": 0, "sentences": 0}
    lengths = [len(WORD.findall(sentence)) for sentence in parts]
    count = len(tokens)
    first_person = sum(token in {"i", "i'm", "i’ve", "i've", "i’m", "i’d", "i'd", "i’ll", "i'll", "me", "my", "mine"} for token in tokens)
    return {
        "words": count,
        "paragraphs": len(blocks),
        "sentences": len(parts),
        "sentence_words_median": statistics.median(lengths),
        "sentence_words_p90": percentile(lengths, 0.9),
        "paragraph_sentences_median": statistics.median(len(sentences(block)) for block in blocks),
        "short_sentences_pct": round(100 * sum(n < 10 for n in lengths) / len(lengths), 3),
        "long_sentences_pct": round(100 * sum(n > 25 for n in lengths) / len(lengths), 3),
        "first_person_per_1000_words": round(1000 * first_person / count, 3),
        "because_so_but_per_1000_words": round(1000 * sum(t in {"because", "so", "but"} for t in tokens) / count, 3),
        "contractions_per_1000_words": round(1000 * sum(bool(re.search(r"(?:n['’]t|['’](?:m|re|ve|ll|d))$", t)) for t in tokens) / count, 3),
    }


def markdown_paths(path: Path) -> list[Path]:
    if not path.exists():
        raise ValueError(f"path does not exist: {path}")
    paths = sorted({page.resolve() for _, page in iter_markdown_pages([path])})
    if not paths:
        raise ValueError(f"no Markdown files found: {path}")
    return paths


def corpus(paths: list[Path], *, lint: bool) -> dict:
    rows = []
    tags: Counter = Counter()
    for path in paths:
        raw = path.read_bytes()
        row = {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(),
               "features": features(raw.decode("utf-8"))}
        if lint:
            findings = [finding for finding in check_page(path.parent, path)
                        if finding.tag not in DEFAULT_OFF_TAGS]
            row["lint"] = [{"line": finding.line, "tag": finding.tag.value,
                            "message": finding.message} for finding in findings]
            tags.update(finding.tag.value for finding in findings)
        rows.append(row)
    measured = [row["features"] for row in rows if row["features"]["words"]]
    if not measured:
        raise ValueError("corpus has no measurable paragraph prose after Markdown cleaning")
    medians = {key: round(statistics.median(row[key] for row in measured), 3)
               for key in measured[0]}
    result = {"files": len(rows), "measured_files": len(measured),
              "empty_prose_files": len(rows) - len(measured),
              "total_prose_words": sum(row["words"] for row in measured),
              "median_per_document": medians, "documents": rows}
    if lint:
        result["lint"] = {
            "findings": sum(tags.values()), "tags": dict(sorted(tags.items())),
            "files_without_findings": sum(not row["lint"] for row in rows),
            # Keep raw counts: the checker also scans lists and code, while
            # the prose metrics exclude them, so their denominators differ.
            "scope": "Full Markdown, default tags, NLP off; reference is never linted.",
        }
    return result


def compare(reference: Path, candidate: Path) -> dict:
    refs, candidates = markdown_paths(reference), markdown_paths(candidate)
    if set(refs) & set(candidates):
        raise ValueError("reference and candidate corpora overlap")
    return {
        "schema_version": 1,
        "stylint_version": __version__,
        "method": {
            "parser": "Approximate Markdown paragraph extraction; see tools/voice_compare.py.",
            "excluded": ["frontmatter", "headings", "lists", "code blocks", "blockquotes",
                         "images", "standalone links", "HTML comments"],
            "retained": ["inline code identifiers", "inline link labels", "newsletter prose and captions"],
            "aggregation": "Unweighted median of each document's features; empty documents excluded from medians.",
            "warning": "Descriptive diagnostics, not a voice score. Match genre and length for comparisons. No human preference inferred.",
        },
        "reference": corpus(refs, lint=False),
        "candidate": corpus(candidates, lint=True),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True, help="Author-selected Markdown; read only, never linted.")
    parser.add_argument("--candidate", type=Path, required=True, help="AI-generated Markdown to measure and lint.")
    parser.add_argument("--output", type=Path, required=True, help="JSON report, outside both input file sets.")
    args = parser.parse_args()
    try:
        inputs = set(markdown_paths(args.reference)) | set(markdown_paths(args.candidate))
        if args.output.resolve() in inputs:
            raise ValueError("output would overwrite an input document")
        report = compare(args.reference, args.candidate)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(f"Wrote {args.output}: {report['reference']['files']} reference files, "
          f"{report['candidate']['files']} candidates, {report['candidate']['lint']['findings']} lint findings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
