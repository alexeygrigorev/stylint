"""Narrow author-calibrated framing and paragraph-run checks."""

import re

from ..models import Finding
from ..patterns import (
    DENSE_PARAGRAPH_MIN_RUN,
    DENSE_PARAGRAPH_MIN_SENTENCES,
    DENSE_PARAGRAPH_MIN_WORDS,
    EVALUATIVE_FRAMING_RE,
)
from ..tags import Tag
from ..text import count_words, split_sentences, strip_double_quoted, strip_inline_code, strip_link_urls


def check_evaluative_framing(paragraph_lines: list[tuple[int, str]], rel) -> list[Finding]:
    joined = ' '.join(text for _, text in paragraph_lines)
    plain = strip_inline_code(strip_link_urls(joined))
    plain = strip_double_quoted(plain)
    plain = re.sub(r'“[^”]*”', '', plain)
    findings = []
    for sentence in split_sentences(plain):
        match = EVALUATIVE_FRAMING_RE.match(sentence)
        if match:
            findings.append(Finding(
                rel, paragraph_lines[0][0], Tag.EVALUATIVE_FRAMING,
                f"'{match.group()}' announces an evaluation before stating it. "
                "Name the action, constraint or consequence directly. If the "
                "preceding text already explains it, delete the recap instead "
                "of replacing it with another summary label. Preserve the "
                "author's actual judgment and its qualifications.",
            ))
    return findings


def check_dense_paragraph_runs(
    paragraphs: list[list[tuple[int, str]]], source_lines: list[str], rel,
) -> list[Finding]:
    """Report one finding per uninterrupted run, not one per paragraph.

    A structural block between paragraphs ends a run. Source line numbers
    retain frontmatter offsets and distinguish wrapping from paragraph breaks.
    """
    findings = []
    run: list[int] = []
    previous_end: int | None = None

    def flush() -> None:
        if len(run) >= DENSE_PARAGRAPH_MIN_RUN:
            findings.append(Finding(
                rel, run[0], Tag.DENSE_PARAGRAPH_RUN,
                f"{len(run)} consecutive paragraphs each contain at least "
                f"{DENSE_PARAGRAPH_MIN_SENTENCES} sentences and "
                f"{DENSE_PARAGRAPH_MIN_WORDS} words (starting on lines "
                + ', '.join(map(str, run)) + "). "
                "Break paragraphs where the subject moves from a need to an "
                "action, observation or decision. Keep related sentences "
                "together and preserve facts; don't pad, shorten every "
                "sentence, or add decorative headings just to break the run.",
            ))
        run.clear()

    for paragraph in paragraphs:
        if not paragraph:
            flush()
            previous_end = None
            continue
        start, end = paragraph[0][0], paragraph[-1][0]
        if previous_end is not None and any(line.strip() for line in source_lines[previous_end:start - 1]):
            flush()
        # An ignored HTML line inside an accumulated paragraph is a boundary
        # too. Do not count text on both sides as an uninterrupted paragraph.
        prose_line_numbers = {number for number, _ in paragraph}
        has_structure = any(source_lines[number - 1].strip()
                            for number in range(start, end + 1)
                            if number not in prose_line_numbers)
        plain = strip_inline_code(strip_link_urls(' '.join(text for _, text in paragraph)))
        dense = (not has_structure
                 and len(split_sentences(plain)) >= DENSE_PARAGRAPH_MIN_SENTENCES
                 and count_words(plain) >= DENSE_PARAGRAPH_MIN_WORDS)
        if dense:
            run.append(start)
        else:
            flush()
        previous_end = end
    flush()
    return findings
