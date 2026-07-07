"""Code block rule constants."""

from ..patterns import CODE_BLOCK_MAX_LINES, PYTHON_CHAINED_GET_RE
from ..models import Finding
from ..tags import Tag

__all__ = ["CODE_BLOCK_MAX_LINES", "PYTHON_CHAINED_GET_RE"]

SHELL_LANGS = frozenset({"bash", "sh", "shell", "zsh", "console"})


def check_code_prompt_line(line: str, code_lang: str, line_no: int, rel) -> list[Finding]:
    if code_lang not in SHELL_LANGS:
        return []
    if not line.lstrip().startswith("$ "):
        return []
    return [
        Finding(
            rel,
            line_no,
            Tag.CODE_PROMPT,
            "shell command in code block starts with '$ '; remove the prompt marker",
        )
    ]


def check_python_code_line(
    line: str,
    previous_code_line_blank: bool,
    line_no: int,
    rel,
) -> list[Finding]:
    findings: list[Finding] = []
    if PYTHON_CHAINED_GET_RE.search(line):
        findings.append(
            Finding(
                rel,
                line_no,
                Tag.CHAINED_GET,
                "chained .get(...).get(...) in example; access known keys directly",
            )
        )
    if line.strip() == "" and previous_code_line_blank:
        findings.append(
            Finding(
                rel,
                line_no,
                Tag.DOUBLE_BLANK,
                "double blank line in code; use one blank line between definitions",
            )
        )
    return findings


def check_code_block_length(code_block_start: int | None, line_count: int, rel) -> list[Finding]:
    if code_block_start is None or line_count <= CODE_BLOCK_MAX_LINES:
        return []
    return [
        Finding(
            rel,
            code_block_start,
            Tag.CODE_TOO_LONG,
            f"code block has {line_count} lines (max {CODE_BLOCK_MAX_LINES}); split with prose",
        )
    ]
