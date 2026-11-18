"""Register-class flags: the announcement-register tag.

These findings are guidance, not bans - see the REGISTER_PATTERNS comment
in patterns.py for the measured motivation. Like the banned-phrase rules,
each pattern runs twice: per line (so single-line matches attribute to the
right line) and over the joined paragraph (so a match straddling a hard
wrap still fires, deduplicated against the line-level findings).
"""

from ..patterns import REGISTER_GUIDANCE, REGISTER_PATTERNS
from ..models import Finding
from ..tags import Tag
from ..text import strip_inline_code, strip_link_urls


def _finding(rel, line_no: int, name: str, hint: str) -> Finding:
    return Finding(
        rel,
        line_no,
        Tag.ANNOUNCEMENT_REGISTER,
        f"'{name}' - {hint}. {REGISTER_GUIDANCE}",
    )


def check_register_line(plain: str, line_no: int, rel) -> list[Finding]:
    findings: list[Finding] = []
    for name, pattern, hint in REGISTER_PATTERNS:
        if pattern.search(plain):
            findings.append(_finding(rel, line_no, name, hint))
    return findings


def check_register_paragraph(
    paragraph_lines: list[tuple[int, str]], rel
) -> list[Finding]:
    if not paragraph_lines:
        return []
    start_line = paragraph_lines[0][0]
    joined = " ".join(text for _, text in paragraph_lines)
    joined = strip_inline_code(strip_link_urls(joined))
    findings: list[Finding] = []
    for name, pattern, hint in REGISTER_PATTERNS:
        if not pattern.search(joined):
            continue
        already_flagged = any(
            pattern.search(strip_inline_code(strip_link_urls(line)))
            for _, line in paragraph_lines
        )
        if not already_flagged:
            findings.append(_finding(rel, start_line, name, hint))
    return findings
