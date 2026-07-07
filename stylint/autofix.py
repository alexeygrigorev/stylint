"""Auto-fix mechanical style findings in place.

Currently fixes contractions only: replaces expanded forms like
"do not" with their contracted equivalents ("don't") in the source
markdown files, preserving case.
"""

from pathlib import Path

from .patterns import CONTRACTION_RES
from .tags import Tag


def apply_auto_fixes(findings: list, pages: list[tuple[Path, Path]]) -> int:
    """Fix contraction findings by rewriting the source files.

    Returns the number of fixes applied. Only findings tagged
    ``Tag.CONTRACTION`` are auto-fixed; everything else is left
    for the human.
    """
    # Build a map from relative path string -> absolute Path
    path_map: dict[str, Path] = {}
    for root, page in pages:
        try:
            rel = page.relative_to(root)
        except ValueError:
            rel = page
        path_map[str(rel)] = page

    contraction_findings = [f for f in findings if f.tag == Tag.CONTRACTION]
    if not contraction_findings:
        return 0

    # Group by file so we read/write each file once
    by_file: dict = {}
    for f in contraction_findings:
        by_file.setdefault(str(f.file), set()).add(f.line)

    fixed = 0
    for rel_str, line_numbers in by_file.items():
        path = path_map.get(rel_str)
        if path is None:
            continue
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        for line_no in sorted(line_numbers):
            idx = line_no - 1
            if idx >= len(lines):
                continue
            original = lines[idx]
            new = original
            for pattern, replacement in CONTRACTION_RES:
                new = pattern.sub(_replace_with_case(replacement), new)
            if new != original:
                lines[idx] = new
                fixed += 1
        path.write_text("".join(lines), encoding="utf-8")

    return fixed


def _replace_with_case(replacement: str):
    """Return a repl function that preserves the case of the match."""
    def repl(match):
        matched = match.group(0)
        if matched[0].isupper():
            return replacement[0].upper() + replacement[1:]
        return replacement
    return repl
