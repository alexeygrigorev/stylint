"""Find noun-smell review candidates in workshop and note corpora.

This is a calibration tool, not a linter. It over-collects likely lines so a
human can label good and bad examples for the review prompts.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


ABSTRACT_NOUNS = (
    "growth",
    "impact",
    "success",
    "failure",
    "result",
    "results",
    "outcome",
    "outcomes",
    "approach",
    "process",
    "workflow",
    "flow",
    "setup",
    "pattern",
    "principle",
    "idea",
    "lesson",
    "takeaway",
    "insight",
    "strategy",
    "habit",
    "practice",
    "routine",
    "step",
    "rule",
    "experience",
    "struggle",
    "challenge",
    "problem",
    "hurdle",
    "story",
    "account",
    "post",
    "section",
    "part",
    "workshop",
    "README",
    "tutorial",
    "guide",
)

ABSTRACT_VERBS = (
    "is",
    "was",
    "are",
    "were",
    "becomes",
    "became",
    "stays",
    "remains",
    "makes",
    "keeps",
    "drives",
    "forces",
    "creates",
    "builds",
    "starts",
    "continues",
    "follows",
    "followed",
    "ends",
    "moves",
    "shows",
    "teaches",
    "explains",
    "proves",
    "reminds",
    "covers",
    "introduces",
    "turns",
    "sets up",
    "blocks",
    "waits",
    "hangs",
    "lets",
    "allows",
    "enables",
    "means",
)

CONCRETE_SUBJECTS = (
    "frontend",
    "front end",
    "backend",
    "back end",
    "database",
    "app",
    "stack",
    "setup",
    "service layer",
    "service",
    "workflow",
    "prompt",
    "code",
    "implementation",
    "file",
    "index",
    "data",
    "workshop",
    "page",
    "section",
    "tutorial",
    "reader",
    "user",
    "mock",
    "root",
    "repo",
    "repository",
    "OpenAPI spec",
    "spec",
    "Docker Compose",
    "Compose",
    "two apps",
)

CONCRETE_VERBS = (
    "defines",
    "decides",
    "starts as",
    "starts",
    "becomes",
    "became",
    "turns into",
    "moves into",
    "moves",
    "switches to",
    "forces",
    "owns",
    "drives",
    "grows into",
    "ends up as",
    "lets you",
    "lets",
    "allows you",
    "allows",
    "enables",
    "needs",
    "requires",
    "expects",
    "stays",
    "keeps",
    "exists so",
    "would collide",
    "collides",
)

CONTROL_PATTERNS = (
    re.compile(r"\bfunction\s+returns\b", re.IGNORECASE),
    re.compile(r"\bdatabase\s+stores\b", re.IGNORECASE),
    re.compile(r"\bDocker Compose\s+starts\b", re.IGNORECASE),
    re.compile(r"\blatency\s+(?:drops|dropped)\s+from\b", re.IGNORECASE),
)


def compile_subject_pattern(subjects: tuple[str, ...]) -> str:
    escaped = sorted((re.escape(s) for s in subjects), key=len, reverse=True)
    return r"(?:" + "|".join(escaped) + r")"


ABSTRACT_RE = re.compile(
    r"\b(?P<phrase>(?:The|This|That|These|Those|A|An|One|Two|Three|\d+)\s+"
    + compile_subject_pattern(ABSTRACT_NOUNS)
    + r"(?:\s+\w+){0,3}\s+"
    + compile_subject_pattern(ABSTRACT_VERBS)
    + r")\b",
    re.IGNORECASE,
)

CONCRETE_RE = re.compile(
    r"\b(?P<phrase>(?:The|This|That|These|Those|A|An|One|Two|Three|\d+)?\s*"
    + compile_subject_pattern(CONCRETE_SUBJECTS)
    + r"(?:\s+\w+){0,5}\s+"
    + compile_subject_pattern(CONCRETE_VERBS)
    + r")\b",
    re.IGNORECASE,
)

EXACT_CONCRETE_RES = (
    re.compile(r"\ball of this\b", re.IGNORECASE),
    re.compile(r"\bthe rest of the workshop needs\b", re.IGNORECASE),
    re.compile(r"\bso replacing it (?:with .+? )?later is easier\b", re.IGNORECASE),
)


@dataclass
class Candidate:
    id: str
    smell: str
    source: str
    path: str
    line_no: int
    line: str
    highlighted_line: str
    phrase: str
    start: int
    end: int
    before: list[str]
    after: list[str]
    signals: list[str]
    paragraph: str = ""
    highlighted_paragraph: str = ""
    target_sentence: str = ""
    highlighted_target_sentence: str = ""
    before_sentence: str = ""
    after_sentence: str = ""
    classifier_label: str = ""
    classifier_reason: str = ""
    classifier_rewrite: str = ""
    human_label: str = ""
    human_note: str = ""


def iter_workshop_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for year in ("2025", "2026"):
        year_root = root / year
        if year_root.exists():
            files.extend(sorted(year_root.rglob("*.md")))
    return files


def iter_telegram_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    files: list[Path] = []
    include_dirs = ("articles", "inbox", "feedback")
    for dirname in include_dirs:
        directory = root / dirname
        if directory.exists():
            files.extend(sorted(directory.rglob("*.md")))
            files.extend(sorted(directory.rglob("*.txt")))
    return [
        p
        for p in files
        if ".git" not in p.parts
        and ".venv" not in p.parts
        and ".pytest_cache" not in p.parts
    ]


@dataclass
class Block:
    start_line: int
    text: str
    char_lines: list[int]


@dataclass
class Sentence:
    block_index: int
    start: int
    end: int
    text: str
    line_no: int


def readable_blocks(path: Path) -> list[Block]:
    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        raw_lines = path.read_text(errors="ignore").splitlines()

    in_fence = False
    in_frontmatter = False
    blocks: list[Block] = []
    current_lines: list[tuple[int, str]] = []

    def flush() -> None:
        nonlocal current_lines
        if not current_lines:
            return
        text_parts: list[str] = []
        char_lines: list[int] = []
        for line_no, line_text in current_lines:
            cleaned = line_text.strip()
            if text_parts:
                text_parts.append(" ")
                char_lines.append(line_no)
            text_parts.append(cleaned)
            char_lines.extend([line_no] * len(cleaned))
        blocks.append(
            Block(
                start_line=current_lines[0][0],
                text="".join(text_parts),
                char_lines=char_lines,
            )
        )
        current_lines = []

    for idx, line in enumerate(raw_lines, start=1):
        stripped = line.strip()
        if idx == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped:
            flush()
            continue
        if stripped.startswith("#"):
            flush()
            continue
        if stripped.startswith("|"):
            flush()
            continue
        if re.match(r"^\s*(?:[-*]|\d+\.)\s+", line) and current_lines:
            flush()
        current_lines.append((idx, line.rstrip()))
    flush()
    return blocks


def highlighted(line: str, start: int, end: int) -> str:
    return (
        html.escape(line[:start])
        + "<mark>"
        + html.escape(line[start:end])
        + "</mark>"
        + html.escape(line[end:])
    )


def find_matches(smell: str, line: str) -> list[tuple[int, int, str, list[str]]]:
    matches: list[tuple[int, int, str, list[str]]] = []
    regexes = [ABSTRACT_RE] if smell == "abstract_subject" else [CONCRETE_RE, *EXACT_CONCRETE_RES]
    for regex in regexes:
        for match in regex.finditer(line):
            start, end = match.span("phrase") if "phrase" in match.groupdict() else match.span()
            phrase = line[start:end]
            signals = [regex.pattern[:80]]
            matches.append((start, end, phrase, signals))

    if smell == "concrete_noun_phrase":
        for control in CONTROL_PATTERNS:
            if control.search(line):
                matches.append((0, len(line), line, ["control"]))

    deduped: list[tuple[int, int, str, list[str]]] = []
    seen: set[tuple[int, int, str]] = set()
    for start, end, phrase, signals in sorted(matches, key=lambda item: (item[0], item[1])):
        key = (start, end, phrase.lower())
        if key not in seen:
            seen.add(key)
            deduped.append((start, end, phrase, signals))
    return deduped


def sentence_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    start = 0
    for match in re.finditer(r"(?<=[.!?])\s+(?=[A-Z`])", text):
        end = match.start()
        if text[start:end].strip():
            spans.append((start, end))
        start = match.end()
    if text[start:].strip():
        spans.append((start, len(text)))
    return spans


def is_complete_sentence(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if stripped.startswith("<") or stripped.endswith(">"):
        return False
    return bool(re.search(r"[.!?][)'\"\]`*_]*$", stripped))


def document_sentences(blocks: list[Block]) -> tuple[list[Sentence], dict[tuple[int, int, int], int]]:
    sentences: list[Sentence] = []
    by_span: dict[tuple[int, int, int], int] = {}
    for block_index, block in enumerate(blocks):
        for start, end in sentence_spans(block.text):
            text = block.text[start:end].strip()
            if not is_complete_sentence(text):
                continue
            line_no = block.char_lines[start] if start < len(block.char_lines) else block.start_line
            sentence = Sentence(
                block_index=block_index,
                start=start,
                end=end,
                text=text,
                line_no=line_no,
            )
            by_span[(block_index, start, end)] = len(sentences)
            sentences.append(sentence)
    return sentences, by_span


def target_sentence_for_match(
    block_index: int,
    text: str,
    match_start: int,
    sentences_by_span: dict[tuple[int, int, int], int],
) -> tuple[int, int, int] | None:
    for start, end in sentence_spans(text):
        if start <= match_start < end:
            sentence_index = sentences_by_span.get((block_index, start, end))
            if sentence_index is None:
                return None
            return sentence_index, start, end
    return None


def scan_source(source: str, root: Path, files: list[Path], window: int) -> list[Candidate]:
    candidates: list[Candidate] = []
    counters = {"abstract_subject": 0, "concrete_noun_phrase": 0}
    for path in files:
        blocks = readable_blocks(path)
        sentences, sentences_by_span = document_sentences(blocks)
        for block_index, block in enumerate(blocks):
            for smell in ("abstract_subject", "concrete_noun_phrase"):
                for start, end, phrase, signals in find_matches(smell, block.text):
                    sentence_match = target_sentence_for_match(
                        block_index, block.text, start, sentences_by_span
                    )
                    if sentence_match is None:
                        continue
                    sentence_index, sentence_start, sentence_end = sentence_match
                    target = sentences[sentence_index]
                    before_sentence = (
                        sentences[sentence_index - 1].text if sentence_index > 0 else ""
                    )
                    after_sentence = (
                        sentences[sentence_index + 1].text
                        if sentence_index + 1 < len(sentences)
                        else ""
                    )
                    target_sentence = target.text
                    counters[smell] += 1
                    rel = path.relative_to(root) if path.is_relative_to(root) else path
                    target_start = start - sentence_start
                    target_end = end - sentence_start
                    candidates.append(
                        Candidate(
                            id=f"{source}-{smell}-{counters[smell]:04d}",
                            smell=smell,
                            source=source,
                            path=str(rel),
                            line_no=target.line_no,
                            line=target_sentence,
                            highlighted_line=highlighted(target_sentence, target_start, target_end),
                            phrase=phrase,
                            start=target_start,
                            end=target_end,
                            before=[before_sentence] if before_sentence else [],
                            after=[after_sentence] if after_sentence else [],
                            paragraph=block.text,
                            highlighted_paragraph=highlighted(block.text, start, end),
                            target_sentence=target_sentence,
                            highlighted_target_sentence=highlighted(
                                target_sentence, target_start, target_end
                            ),
                            before_sentence=before_sentence,
                            after_sentence=after_sentence,
                            signals=signals,
                        )
                    )
    return candidates


def write_markdown(candidates: list[Candidate], path: Path, limit: int | None) -> None:
    selected = candidates[:limit] if limit else candidates
    lines = ["# Noun smell candidates", ""]
    for candidate in selected:
        location = f"{candidate.source}:{candidate.path}:{candidate.line_no}"
        lines.extend(
            [
                f"## {candidate.id}",
                "",
                f"- smell: `{candidate.smell}`",
                f"- location: `{location}`",
                f"- phrase: `{candidate.phrase}`",
                "",
            ]
        )
        if candidate.before:
            lines.append("Context before:")
            lines.append("")
            for text in candidate.before:
                lines.append(f"> {text}")
            lines.append("")
        lines.append("Candidate:")
        lines.append("")
        lines.append(f"> {candidate.highlighted_line}")
        lines.append("")
        if candidate.after:
            lines.append("Context after:")
            lines.append("")
            for text in candidate.after:
                lines.append(f"> {text}")
            lines.append("")
        lines.extend(["Decision: TODO", "Rewrite: TODO", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workshops-root", type=Path, required=True)
    parser.add_argument("--telegram-root", type=Path)
    parser.add_argument("--out", type=Path, default=Path("/tmp/noun-smell-candidates.json"))
    parser.add_argument("--markdown-out", type=Path)
    parser.add_argument("--context", type=int, default=2)
    parser.add_argument("--markdown-limit", type=int)
    args = parser.parse_args()

    all_candidates: list[Candidate] = []
    workshop_files = iter_workshop_files(args.workshops_root)
    all_candidates.extend(scan_source("workshop", args.workshops_root, workshop_files, args.context))

    if args.telegram_root:
        telegram_files = iter_telegram_files(args.telegram_root)
        all_candidates.extend(scan_source("telegram", args.telegram_root, telegram_files, args.context))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps([asdict(candidate) for candidate in all_candidates], indent=2),
        encoding="utf-8",
    )
    if args.markdown_out:
        args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
        write_markdown(all_candidates, args.markdown_out, args.markdown_limit)

    counts: dict[tuple[str, str], int] = {}
    for candidate in all_candidates:
        key = (candidate.source, candidate.smell)
        counts[key] = counts.get(key, 0) + 1
    for (source, smell), count in sorted(counts.items()):
        print(f"{source} {smell}: {count}")
    print(f"wrote {args.out}")
    if args.markdown_out:
        print(f"wrote {args.markdown_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
