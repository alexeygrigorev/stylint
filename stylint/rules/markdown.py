"""Markdown mechanics rule patterns."""

from ..patterns import (
    ANGLE_URL_RE,
    BARE_URL_RE,
    DASH_PARENTHETICAL_RE,
    DOUBLE_HYPHEN_RE,
    ITALIC_RE,
    LINK_RE,
    SMART_QUOTES,
)
from ..models import Finding
from ..patterns import LIST_ITEM_RE
from ..tags import Tag

__all__ = [
    "ANGLE_URL_RE",
    "BARE_URL_RE",
    "DASH_PARENTHETICAL_RE",
    "DOUBLE_HYPHEN_RE",
    "ITALIC_RE",
    "LINK_RE",
    "SMART_QUOTES",
]


def check_table_row(rel, line_no: int) -> Finding:
    return Finding(rel, line_no, Tag.TABLES, "markdown tables are not used")


def check_markdown_line(line: str, plain: str, line_no: int, rel) -> list[Finding]:
    findings: list[Finding] = []
    if "**" in plain or "__" in plain:
        findings.append(Finding(rel, line_no, Tag.BOLD, "bold markdown is not used"))
    if ITALIC_RE.search(plain):
        findings.append(Finding(rel, line_no, Tag.ITALIC, "italic markdown is not used"))
    if line.strip() == "---":
        findings.append(Finding(rel, line_no, Tag.HR, "horizontal rules are not used"))
    if "—" in line:
        findings.append(Finding(
            rel, line_no, Tag.EM_DASH,
            "em dash in prose; replace it with a hyphen. The exception is a "
            "parenthetical aside set off by two dashes: split that into two "
            "sentences rather than re-bracketing it with commas.",
        ))
    if DOUBLE_HYPHEN_RE.search(plain) and not line.lstrip().startswith("|"):
        findings.append(Finding(
            rel, line_no, Tag.DOUBLE_HYPHEN,
            "double hyphen in prose; use a single hyphen. When two dashes "
            "bracket a parenthetical aside, split it into two sentences "
            "instead.",
        ))
    if DASH_PARENTHETICAL_RE.search(plain) and not LIST_ITEM_RE.match(line):
        findings.append(
            Finding(
                rel,
                line_no,
                Tag.DASH_PARENTHETICAL,
                "dash-enclosed parenthetical in prose; split it into two "
                "sentences or fold the aside into the main clause. Swapping "
                "the dashes for commas only masks the same interruption.",
            )
        )
    for char, name in SMART_QUOTES.items():
        if char in line:
            findings.append(Finding(rel, line_no, Tag.SMART_QUOTES, f"use straight quotes, not {name}"))
    for match in LINK_RE.finditer(line):
        if "`" in match.group(1):
            findings.append(
                Finding(rel, line_no, Tag.BACKTICKS_IN_LINK, "do not put backticks inside link text")
            )

    line_is_html = line.lstrip().startswith("<")
    line_is_table = line.lstrip().startswith("|")
    if BARE_URL_RE.search(plain) and not line_is_html and not line_is_table:
        findings.append(Finding(rel, line_no, Tag.BARE_URL, "bare URL in prose; use [name](url)"))
    if ANGLE_URL_RE.search(line) and not line_is_html:
        findings.append(
            Finding(rel, line_no, Tag.ANGLE_URL, "angle-bracket URL form not used; use [name](url)")
        )
    return findings
