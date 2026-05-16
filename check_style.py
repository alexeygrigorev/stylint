#!/usr/bin/env python3
"""Check mechanical markdown style rules.

Add a banned word / phrase / opener to the lists below and the check picks
it up automatically. Each entry maps to a one-line guidance message so the
agent reading the failure knows how to fix it.

Usage:
    check_style.py                    # scan *.md recursively from cwd
    check_style.py path/to/file.md    # check one file
    check_style.py docs/ notes/       # check several dirs

Files and directories listed in a .prose-style-ignore file at the scan
root are skipped (one path per line, # for comments, glob patterns OK).
"""

import argparse
import fnmatch
from pathlib import Path
import re
import sys


LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
QUESTION_HEADING_RE = re.compile(
    r"^#{1,6}\s+(Why|How|What|When|Where|Which|Who)\b"
)
QUESTION_MARK_HEADING_RE = re.compile(r"^#{1,6}\s+.*\?\s*$")
DEEP_HEADING_RE = re.compile(r"^#{3,}\s")
ITALIC_RE = re.compile(
    r"(?<![\w*])\*[^*\s][^*]*\*(?![\w*])|(?<![\w_])_[^_\s][^_]*_(?![\w_])",
)
SMART_QUOTES = {
    "‘": "left smart single quote",
    "’": "right smart single quote",
    "“": "left smart double quote",
    "”": "right smart double quote",
}
BARE_URL_RE = re.compile(r"\bhttps?://")
ANGLE_URL_RE = re.compile(r"<https?://")
DOUBLE_HYPHEN_RE = re.compile(r"(?<!<)(?<!/)--(?!/)(?!>)")
DASH_PARENTHETICAL_RE = re.compile(
    r"[a-zA-Z]\s+-\s+.*?\s+-\s+[a-zA-Z]"
)
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+")
# Sentence-start "No X, no Y..." anaphora — typical verbless rhetorical
# fragment like "No frameworks, no magic - just Python and an LLM."
# Requires capital `No` at sentence start to skip "there are no X, no Y..."
# (which is grammatically complete).
ANAPHORIC_NO_RE = re.compile(
    r"(?:^|[.!?]\s+)No\s+\w+(?:\s+\w+){0,2},\s+no\s+\w+"
)

# Single banned tokens. Whole-word, case-insensitive in prose.
BANNED_WORDS: dict[str, str] = {
    "delve": "use 'look at' / 'dig into' / 'explore'",
    "crucial": "drop or use 'important' / 'essential'",
    "pivotal": "drop the puffery",
    "vibrant": "drop the puffery",
    "intricate": "use 'detailed' or rewrite",
    "garner": "use 'gather' / 'get'",
    "bolster": "use 'strengthen' / 'add'",
    "foster": "use 'build' / 'help'",
    "showcase": "use 'show'",
    "enhance": "use a specific verb (improve / add / extend)",
    "emphasize": "name the concrete thing",
    "leverage": "use 'use'",
    "multifaceted": "drop or use the concrete description",
    "realm": "drop the metaphor",
    "captivating": "drop the puffery",
    "elevate": "use 'raise' / 'improve'",
    "suddenly": "drop",
    "basically": "drop",
    "very": "drop",
    "really": "drop",
    "underneath": "use 'under the hood' / 'inside' / 'behind'",
    "surprisingly": "drop the editorializing",
    "remarkably": "drop the editorializing",
    "faithful": "drop the metaphor; describe the concrete match",
    "itself": "use sparingly; if it does not change the meaning, drop it",
}

# Multi-word banned phrases. Substring match, case-insensitive.
BANNED_PHRASES: dict[str, str] = {
    "in order to": "use 'to'",
    "this matters because": "give the concrete reason directly",
    "at this point": "use 'now' or cut",
    "this gives us": "use 'now we have' / 'we'll use'",
    "this is useful because": "name the use directly",
    "the point is": "rewrite around what the reader should learn",
    "the point of": "rewrite around what the reader should learn",
    "the intent is": "name the action directly; abstract opener",
    "the goal is": "state what we are doing, not the goal",
    "the idea is": "state the idea directly",
    "the short rule": "drop the preamble; state the rule",
    "the short answer": "drop the preamble; give the answer",
    "the longer answer": "drop the preamble; give the answer",
    "the long answer": "drop the preamble; give the answer",
    "the important difference": "rewrite as a direct contrast",
    "reference implementation": "use 'finished app' / 'example app' / 'working version'",
    "demo artifact": "name the file/app/output",
    "framework-agnostic": "use 'works across frameworks'",
    "direct command interception": "use 'run slash commands before the model sees them'",
    "further reading": "use 'to learn more'",
    "known-good version": "use 'working version'",
    "a clear pattern emerged": "drop the cliche",
    "here's the catch": "drop the cliche",
    "plot twist": "drop the cliche",
    "but there's a twist": "drop the cliche",
    "now for the fun part": "drop the cliche",
    "marks a pivotal moment": "drop the puffery",
    "a testament to": "drop the puffery",
    "reflects broader trends": "drop the puffery",
    "experts argue": "drop the vague attribution",
    "industry reports suggest": "drop the vague attribution",
    "the wider picture": "use a concrete pivot",
    "the bigger picture": "use a concrete pivot",
    "zooming out": "use a concrete pivot",
    "stepping back": "use a concrete pivot",
    "if you squint": "use a concrete pivot",
    "the bird's-eye view": "use a concrete pivot",
    "low-hanging fruit": "drop the idiom",
    "off the table": "say it directly",
    "at the end of the day": "drop the idiom",
    "cut to the chase": "drop the idiom",
    "the elephant in the room": "drop the idiom",
    "that bites us": "describe the event neutrally",
    "that bit me": "describe the event neutrally",
    "we got burned": "describe the event neutrally",
    "what follows is": "drop; let the headings show what is next",
    "in this section we will": "drop the meta-narration",
    "below you will find": "drop the meta-narration",
    "the next few paragraphs": "drop the meta-narration",
    "as we shall see": "drop the meta-narration",
    "for reasons that will become clear": "give the reason on the same line",
    "the single most": "drop the superlative",
    "the hardest part": "drop the superlative",
    "the trickiest step": "drop the superlative",
    "the key insight": "drop the editorializing",
    "the big idea is": "state the idea directly",
    "this is where it gets interesting": "drop the editorializing",
    "the shape of": "show the shape, do not announce it",
    "on the wire": "name the bytes/payload directly; 'on the wire' is network jargon",
    "out of the box": "describe the default behavior in plain words",
    "tight inner loop": "describe the actual workflow (rebuild time, edit-test cycle)",
    "tight loop": "describe the actual workflow (rebuild time, edit-test cycle)",
    "reusable principle": "name the workflow or habit directly",
    "serves as": "use 'is'",
    "stands as": "use 'is'",
    "diverse array": "drop the puffery",
    "commitment to excellence": "drop the puffery",
    "boasts a": "use 'has'",
    "let me tell you": "drop the filler",
    "let me explain": "drop the filler",
    "let me expand on": "drop the filler",
    "i want to be clear": "state the thing directly",
    "is a reminder that": "drop the abstract framing; state the point directly",
    "pull request ceremony": "drop the jargon noun",
    "one benefit of": "state the benefit directly",
    "on the table": "say it directly",
}

# Sentence openers. Capitalized, must start the line (allowing optional list
# marker). Match is case-sensitive on the opener token itself.
BANNED_OPENERS: dict[str, str] = {
    "Additionally": "drop or rewrite",
    "Moreover": "drop or rewrite",
    "Furthermore": "drop or rewrite",
    "Notably": "drop or rewrite",
    "Importantly": "drop or rewrite",
    "Consequently": "drop or rewrite",
}
OPENER_RE = re.compile(
    r"^(?:[-*]\s+|\d+\.\s+)?(" + "|".join(re.escape(w) for w in BANNED_OPENERS) + r")\b"
)
WORD_RES: dict[str, re.Pattern[str]] = {
    word: re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
    for word in BANNED_WORDS
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check mechanical markdown style rules.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Files or directories to scan. Defaults to the current directory.",
    )
    return parser.parse_args()


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text

    parts = text.split("---\n", 2)
    if len(parts) == 3:
        return parts[2]
    return text


def load_ignore_patterns(root: Path) -> list[str]:
    ignore_file = root / ".prose-style-ignore"
    if not ignore_file.is_file():
        return []
    patterns: list[str] = []
    for raw in ignore_file.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def is_ignored(rel: Path, patterns: list[str]) -> bool:
    rel_str = str(rel)
    for pattern in patterns:
        if fnmatch.fnmatch(rel_str, pattern):
            return True
        if any(fnmatch.fnmatch(part, pattern) for part in rel.parts):
            return True
    return False


def iter_markdown_pages(paths: list[Path]) -> list[tuple[Path, Path]]:
    """Return [(root, page)] pairs so error paths can stay relative to the scan root."""
    pages: list[tuple[Path, Path]] = []
    for p in paths:
        p = p.resolve()
        if p.is_file() and p.suffix.lower() == ".md":
            pages.append((p.parent, p))
        elif p.is_dir():
            ignore = load_ignore_patterns(p)
            for md in sorted(p.rglob("*.md")):
                rel = md.relative_to(p)
                if is_ignored(rel, ignore):
                    continue
                pages.append((p, md))
    return pages


def strip_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


def strip_link_urls(line: str) -> str:
    return LINK_RE.sub(lambda match: match.group(1), line)


CODE_BLOCK_MAX_LINES = 40
HEADING_RE = re.compile(r"^#{1,6}\s")
LIST_RE = re.compile(r"^\s*[-*]\s|^\s*\d+\.\s")
BLOCKQUOTE_RE = re.compile(r"^\s*>")
PYTHON_CHAINED_GET_RE = re.compile(r"\.get\([^)]*\)\.get\(")
PARAGRAPH_MAX_SENTENCES = 5
SENTENCE_END_RE = re.compile(r"[.!?](?=[\s\"')\]]|$)")
ABBREVIATION_RE = re.compile(
    r"\b(?:e\.g|i\.e|etc|vs|cf|Mr|Mrs|Ms|Dr|St|Jr|Sr|U\.S|U\.K|a\.m|p\.m|Inc|Ltd|Co)\.",
    re.IGNORECASE,
)
GERUND_NOUN_EXCEPTIONS = {
    "spring", "string", "building", "setting", "meeting",
    "heading", "wedding", "beginning", "ending", "standing",
    "wing", "sing", "ring", "king", "thing", "bring",
    "everything", "nothing", "something", "anything",
    "morning", "evening", "saying", "streaming",
}
# Participial phrases: -ing phrase, then COMMA, then a likely new subject.
# Matches "Reading through it, I noticed..." but not "Calling them works, but..."
# (the gerund-as-subject form, where the verb sits before the comma).
_PARTICIPIAL_TAIL = r"\b[^.!?]{0,150},\s+(?:I|we|you|they|he|she|it|the|a|an|this|that|these|those)\b"
GERUND_LINE_START_RE = re.compile(r"^([A-Z][a-z]{3,}ing)" + _PARTICIPIAL_TAIL)
GERUND_MIDLINE_RE = re.compile(r"[.!?]\s+([A-Z][a-z]{3,}ing)" + _PARTICIPIAL_TAIL)


def count_sentences(text: str) -> int:
    text = re.sub(r"`[^`]*`", " ", text)
    text = ABBREVIATION_RE.sub("", text)
    return len(SENTENCE_END_RE.findall(text))


def find_gerund_starts(plain: str) -> list[str]:
    flagged: list[str] = []
    line_match = GERUND_LINE_START_RE.match(plain.lstrip())
    if line_match and line_match.group(1).lower() not in GERUND_NOUN_EXCEPTIONS:
        flagged.append(line_match.group(1))
    for match in GERUND_MIDLINE_RE.finditer(plain):
        word = match.group(1)
        if word.lower() not in GERUND_NOUN_EXCEPTIONS:
            flagged.append(word)
    return flagged


def check_page(root: Path, path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text()
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3 and parts[2] and not parts[2].startswith("\n"):
            fm_close_line = parts[0].count("\n") + parts[1].count("\n") + 2
            errors.append(
                f"{rel}:{fm_close_line + 1}: insert a blank line between frontmatter and body"
            )
    body = strip_frontmatter(text)
    fm_lines = text.count("\n") - body.count("\n") if body != text else 0
    line_offset = fm_lines
    lines = body.splitlines()
    in_code = False
    code_lang = ""
    previous_code_block_end: int | None = None
    code_block_start: int | None = None
    code_block_line_count = 0
    last_heading_line: int | None = None
    seen_prose_since_heading = False
    previous_code_line_blank = False

    paragraph_lines: list[tuple[int, str]] = []

    def flush_paragraph() -> None:
        if not paragraph_lines:
            return
        start_line = paragraph_lines[0][0]
        joined_raw = " ".join(text for _, text in paragraph_lines)
        joined = strip_inline_code(strip_link_urls(joined_raw))
        joined_lower = joined.lower()

        sentences = count_sentences(joined)
        if sentences > PARAGRAPH_MAX_SENTENCES:
            errors.append(
                f"{rel}:{start_line}: paragraph has {sentences} sentences (max {PARAGRAPH_MAX_SENTENCES}); split into 2-4 sentence paragraphs"
            )

        for phrase, hint in BANNED_PHRASES.items():
            if phrase in joined_lower:
                already_flagged = any(
                    phrase in strip_inline_code(strip_link_urls(line)).lower()
                    for _, line in paragraph_lines
                )
                if not already_flagged:
                    errors.append(
                        f"{rel}:{start_line}: banned phrase '{phrase}' across lines ({hint})"
                    )

        for word in find_gerund_starts(joined):
            errors.append(
                f"{rel}:{start_line}: sentence opens with '-ing' word '{word}'; rewrite if it is a participial phrase"
            )

        paragraph_lines.clear()

    for line_no, line in enumerate(lines, start=1 + line_offset):
        stripped = line.strip()
        starts_fence = line.lstrip().startswith("```")

        if not in_code and previous_code_block_end is not None and stripped:
            if starts_fence:
                errors.append(
                    f"{rel}:{line_no}: consecutive code blocks need prose between them"
                )
            previous_code_block_end = None

        if starts_fence:
            flush_paragraph()
            if not in_code:
                fence_tail = line.lstrip()[3:].strip()
                if not fence_tail:
                    errors.append(
                        f"{rel}:{line_no}: code block missing language tag (use ```python, ```bash, ...)"
                    )
                if last_heading_line is not None and not seen_prose_since_heading:
                    errors.append(
                        f"{rel}:{line_no}: code block needs a lead-in sentence after the heading on line {last_heading_line}"
                    )
                code_lang = fence_tail.lower()
                code_block_start = line_no
                code_block_line_count = 0
                previous_code_line_blank = False
            else:
                if (
                    code_block_start is not None
                    and code_block_line_count > CODE_BLOCK_MAX_LINES
                ):
                    errors.append(
                        f"{rel}:{code_block_start}: code block has {code_block_line_count} lines (max {CODE_BLOCK_MAX_LINES}); split with prose"
                    )
                code_block_start = None
                code_lang = ""
            in_code = not in_code
            if not in_code:
                previous_code_block_end = line_no
            continue

        if in_code:
            code_block_line_count += 1
            if code_lang == "python":
                if PYTHON_CHAINED_GET_RE.search(line):
                    errors.append(
                        f"{rel}:{line_no}: chained .get(...).get(...) in example; access known keys directly"
                    )
                if line.strip() == "" and previous_code_line_blank:
                    errors.append(
                        f"{rel}:{line_no}: double blank line in code; use one blank line between definitions"
                    )
                previous_code_line_blank = line.strip() == ""
            continue

        if HEADING_RE.match(line):
            flush_paragraph()
            if QUESTION_HEADING_RE.match(line):
                errors.append(f"{rel}:{line_no}: avoid question-word headings")
            if QUESTION_MARK_HEADING_RE.match(line):
                errors.append(f"{rel}:{line_no}: heading ends with '?' (use a statement)")
            if DEEP_HEADING_RE.match(line):
                errors.append(f"{rel}:{line_no}: heading depth ### or deeper not allowed")
            last_heading_line = line_no
            seen_prose_since_heading = False
            continue

        if not stripped:
            flush_paragraph()
        elif LIST_RE.match(line):
            flush_paragraph()
            if last_heading_line is not None and not seen_prose_since_heading:
                errors.append(
                    f"{rel}:{line_no}: list needs a lead-in sentence after the heading on line {last_heading_line}"
                )
                last_heading_line = None
            seen_prose_since_heading = True
        elif BLOCKQUOTE_RE.match(line) or line.startswith("|"):
            flush_paragraph()
            seen_prose_since_heading = True
        else:
            seen_prose_since_heading = True
            paragraph_lines.append((line_no, stripped))

        plain = strip_inline_code(strip_link_urls(line))
        plain_lower = plain.lower()

        if "**" in plain or "__" in plain:
            errors.append(f"{rel}:{line_no}: bold markdown is not used")
        if ITALIC_RE.search(plain):
            errors.append(f"{rel}:{line_no}: italic markdown is not used")
        if line.startswith("|"):
            errors.append(f"{rel}:{line_no}: markdown tables are not used")
        if line.strip() == "---":
            errors.append(f"{rel}:{line_no}: horizontal rules are not used")
        if "—" in line:
            errors.append(f"{rel}:{line_no}: use a hyphen instead of an em dash")
        if DOUBLE_HYPHEN_RE.search(plain):
            errors.append(f"{rel}:{line_no}: use a single hyphen, not '--'")
        if DASH_PARENTHETICAL_RE.search(plain) and not LIST_ITEM_RE.match(line):
            errors.append(
                f"{rel}:{line_no}: dash-enclosed parenthetical in prose; "
                "split into two sentences or simplify"
            )
        for char, name in SMART_QUOTES.items():
            if char in line:
                errors.append(f"{rel}:{line_no}: use straight quotes, not {name}")
        for match in LINK_RE.finditer(line):
            if "`" in match.group(1):
                errors.append(f"{rel}:{line_no}: do not put backticks inside link text")
        if "Alexey" in plain:
            errors.append(f"{rel}:{line_no}: avoid third-person presenter references")
        if ANAPHORIC_NO_RE.search(plain):
            errors.append(
                f"{rel}:{line_no}: 'No X, no Y' verbless fragment; rewrite with a subject and verb"
            )

        if BARE_URL_RE.search(plain):
            errors.append(f"{rel}:{line_no}: bare URL in prose; use [name](url)")
        if ANGLE_URL_RE.search(line):
            errors.append(f"{rel}:{line_no}: angle-bracket URL form not used; use [name](url)")

        for word, hint in BANNED_WORDS.items():
            if WORD_RES[word].search(plain):
                errors.append(f"{rel}:{line_no}: banned word '{word}' ({hint})")

        for phrase, hint in BANNED_PHRASES.items():
            if phrase in plain_lower:
                errors.append(f"{rel}:{line_no}: banned phrase '{phrase}' ({hint})")

        opener_match = OPENER_RE.match(line)
        if opener_match:
            opener = opener_match.group(1)
            errors.append(
                f"{rel}:{line_no}: banned opener '{opener}' ({BANNED_OPENERS[opener]})"
            )

    flush_paragraph()
    return errors


def main() -> int:
    args = parse_args()
    paths = [Path(p) for p in args.paths]
    pages = iter_markdown_pages(paths)
    if not pages:
        print("No markdown files found.", file=sys.stderr)
        return 0

    errors: list[str] = []
    for root, page in pages:
        errors.extend(check_page(root, page))

    if errors:
        print("Style check failed:")
        print("\n".join(f"  {error}" for error in errors))
        return 1

    print(f"Style check passed ({len(pages)} file{'s' if len(pages) != 1 else ''}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
