"""Command-line interface."""

import argparse
from pathlib import Path
import sys

from .discovery import iter_markdown_pages
from .lint import check_page
from .output import print_findings
from . import explanations
from .styleguide import (
    DRAFTING_PROMPTS,
    SMELL_PROMPTS,
    agents_guide_file,
    prompt_file,
    prompt_files,
    style_guide_file,
    style_guide_files,
    style_guide_path,
)
from .tags import DEFAULT_OFF_TAGS, Tag
from .version import __version__
from .autofix import apply_auto_fixes
from .candidates import find_candidates

# The prompt that classifies tool-as-actor candidates found by the finder.
CANDIDATES_PROMPT = "noun-phrase-smell"


def _exclude_patterns(args: argparse.Namespace) -> list[str]:
    return [
        pattern.strip()
        for raw_exclude in args.exclude
        for pattern in raw_exclude.split(",")
        if pattern.strip()
    ]


def _print_candidates_section(args: argparse.Namespace) -> None:
    """Append the static tool-as-actor candidates to the printed prompt."""
    pages = iter_markdown_pages([Path(p) for p in args.paths], _exclude_patterns(args))
    candidates = find_candidates(pages)
    print("\n## Candidates found by stylint\n")
    print(
        "Classify every candidate below as role or runtime. These are the "
        "minimum list; also check the text for anything the list missed.\n"
    )
    if not candidates:
        print("(no candidates found)")
    for candidate in candidates:
        print(candidate.render())


def _print_candidates_hint(args: argparse.Namespace, pages) -> None:
    """One non-failing line pointing at the review prompt when the static
    finder sees tool-as-actor candidates. Not a finding."""
    count = len(find_candidates(pages))
    if not count:
        return
    targets = " ".join(args.paths) or "."
    suffix = "s" if count != 1 else ""
    print(
        f"note: {count} tool-as-actor candidate{suffix}; run "
        f"`stylint --prompt {CANDIDATES_PROMPT} {targets}` to review them"
    )


def _prompt_table(prompts: dict[str, str]) -> str:
    width = max(len(name) for name in prompts)
    return "\n".join(f"  {name:<{width}}  {text}" for name, text in prompts.items())


def _epilog() -> str:
    return (
        "LLM smell checks (no regex catches these; print the prompt with\n"
        "'stylint --prompt NAME' and apply it to the edited files):\n"
        + _prompt_table(SMELL_PROMPTS)
        + "\n\nDrafting prompts:\n"
        + _prompt_table(DRAFTING_PROMPTS)
        + "\n\nAgent workflow: run 'stylint --agents' first to see which style\n"
        "guide to use before editing, during structure changes, and before\n"
        "the final full check."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check mechanical markdown style rules.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_epilog(),
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=[],
        help=(
            "Files or directories to scan. Defaults to the current directory. "
            "With --prompt noun-phrase-smell, the files to list "
            "tool-as-actor candidates for."
        ),
    )
    parser.add_argument(
        "--ignore",
        default="",
        metavar="TAGS",
        help=(
            "Comma-separated rule tags to suppress "
            "(e.g. --ignore tables,long-clause-likely). Run with --list-tags "
            "to see all known tags."
        ),
    )
    parser.add_argument(
        "--enable",
        default="",
        metavar="TAGS",
        help=(
            "Comma-separated rule tags to enable that are off by default "
            "(e.g. --enable backticks-in-link). Off-by-default tags: "
            + ", ".join(sorted(t.value for t in DEFAULT_OFF_TAGS))
            + "."
        ),
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PATTERN",
        help=(
            "Exclude files or folders by fnmatch pattern. Can be repeated "
            "or comma-separated, e.g. --exclude _docs --exclude AGENTS.md."
        ),
    )
    parser.add_argument(
        "--author-name",
        default="Alexey",
        metavar="NAME",
        help=(
            "Name of the page's author/presenter. The third-person check "
            "flags this name as a self-reference. Defaults to 'Alexey'. "
            "Pass a guest instructor's name (e.g. --author-name Valeriia) "
            "so their own name flags while other people's names do not. "
            "Pass an empty string to disable the check."
        ),
    )
    parser.add_argument(
        "--nlp",
        action="store_true",
        help=(
            "Enable slower NLP-based checks (passive voice, etc.). Off by "
            "default; loads an NLP tagger only when set. Requires the "
            "optional extra: pip install \"stylint[nlp]\"."
        ),
    )
    parser.add_argument(
        "--list-tags",
        action="store_true",
        help="Print all known rule tags and exit.",
    )
    parser.add_argument(
        "--explain",
        metavar="TAG",
        nargs="?",
        const="",
        help=(
            "Print a detailed explanation for one rule tag and exit. "
            "Accepts hyphens, underscores, or spaces, and also resolves "
            "pattern labels (e.g. 'content as actor'). Pass nothing to "
            "list all explainable tags."
        ),
    )
    parser.add_argument(
        "--agents",
        action="store_true",
        help=(
            "Print the short agent editing checklist: when to read each "
            "style guide and how to verify edits."
        ),
    )
    parser.add_argument(
        "--prompt",
        metavar="NAME",
        nargs="?",
        const="",
        help=(
            "Print an LLM smell check or drafting prompt. Pass a name "
            "(see the list below) to print it; pass nothing to list names "
            "with descriptions. With paths, noun-phrase-smell also appends "
            "the tool-as-actor candidates stylint finds in those files."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"stylint {__version__}",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help=(
            "Auto-fix mechanical findings in place. Currently fixes "
            "contractions (e.g. 'do not' -> 'don't'). Re-runs the "
            "check after fixing and prints remaining findings."
        ),
    )
    parser.add_argument(
        "--style-guide",
        metavar="NAME",
        nargs="?",
        const="",
        help=(
            "Print the installed style guide paths. Pass a guide name "
            "(voice, formatting, code-style, polish, alexey) to print that document."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.list_tags:
        for tag in Tag:
            print(tag.value)
        return 0

    if args.explain == "":
        for tag in explanations.all_tags():
            print(tag)
        return 0

    if args.explain:
        try:
            entry = explanations.explain(args.explain)
        except KeyError:
            print(
                f"Unknown tag for --explain: '{args.explain}'. "
                "Run with --explain (no argument) or --list-tags to see "
                "known tags.",
                file=sys.stderr,
            )
            return 2
        print(entry.render())
        return 0

    if args.agents:
        print(agents_guide_file().read_text(encoding="utf-8"), end="")
        return 0

    if args.prompt == "":
        print("LLM smell checks:")
        print(_prompt_table(SMELL_PROMPTS))
        print("\nDrafting prompts:")
        print(_prompt_table(DRAFTING_PROMPTS))
        return 0

    if args.prompt:
        try:
            path = prompt_file(args.prompt)
        except KeyError:
            print(
                "Unknown review prompt. Use one of: "
                + ", ".join(prompt_files()),
                file=sys.stderr,
            )
            return 2
        print(path.read_text(encoding="utf-8"), end="")
        if args.paths and path == prompt_file(CANDIDATES_PROMPT):
            _print_candidates_section(args)
        return 0

    if args.style_guide == "":
        print(style_guide_path())
        for name, path in style_guide_files().items():
            print(f"{name}: {path}")
        return 0

    if args.style_guide:
        try:
            path = style_guide_file(args.style_guide)
        except KeyError:
            print(
                "Unknown style guide. Use one of: "
                + ", ".join(style_guide_files()),
                file=sys.stderr,
            )
            return 2
        print(path.read_text(encoding="utf-8"), end="")
        return 0

    valid_tags = {t.value for t in Tag}
    # Backwards-compat: the single 'long-and-commas' tag was split into
    # two (long-list-likely and long-clause-likely). Accept the old name
    # as an alias that expands to both.
    tag_aliases = {
        "long-and-commas": ("long-list-likely", "long-clause-likely"),
    }
    raw = [t.strip() for t in args.ignore.split(",") if t.strip()]
    ignore_list: list[str] = []
    for t in raw:
        if t in tag_aliases:
            ignore_list.extend(tag_aliases[t])
        else:
            ignore_list.append(t)
    unknown = [t for t in ignore_list if t not in valid_tags]
    if unknown:
        print(f"Unknown tag(s) for --ignore: {', '.join(unknown)}", file=sys.stderr)
        print("Run with --list-tags to see known tags.", file=sys.stderr)
        return 2
    ignore_tags = {Tag(t) for t in ignore_list}

    raw_enable = [t.strip() for t in args.enable.split(",") if t.strip()]
    unknown_enable = [t for t in raw_enable if t not in valid_tags]
    if unknown_enable:
        print(
            f"Unknown tag(s) for --enable: {', '.join(unknown_enable)}",
            file=sys.stderr,
        )
        print("Run with --list-tags to see known tags.", file=sys.stderr)
        return 2
    enable_tags = {Tag(t) for t in raw_enable}
    effective_off = DEFAULT_OFF_TAGS - enable_tags

    exclude_patterns = _exclude_patterns(args)

    paths = [Path(p) for p in args.paths or ["."]]
    pages = iter_markdown_pages(paths, exclude_patterns)
    if not pages:
        print("No markdown files found.", file=sys.stderr)
        return 0

    if args.nlp:
        # Surface a missing dependency/data up front with one clean
        # message instead of failing partway through the first page.
        from .nlp import NlpUnavailableError, check_line

        try:
            check_line("warm up the tagger")
        except NlpUnavailableError as exc:
            print(str(exc), file=sys.stderr)
            return 2

    findings = []
    for root, page in pages:
        findings.extend(check_page(root, page, nlp=args.nlp, author_name=args.author_name))

    if effective_off:
        findings = [finding for finding in findings if finding.tag not in effective_off]

    if ignore_tags:
        findings = [finding for finding in findings if finding.tag not in ignore_tags]

    if args.fix:
        fixed = apply_auto_fixes(findings, pages)
        if fixed:
            suffix = "s" if fixed != 1 else ""
            print(f"Auto-fixed {fixed} contraction{suffix} in place.")
        # Re-run the check to show remaining findings
        findings = []
        for root, page in pages:
            findings.extend(
                check_page(root, page, nlp=args.nlp, author_name=args.author_name)
            )
        if effective_off:
            findings = [f for f in findings if f.tag not in effective_off]
        if ignore_tags:
            findings = [f for f in findings if f.tag not in ignore_tags]

    if findings:
        print_findings(findings)
        _print_candidates_hint(args, pages)
        return 1

    suffix = "s" if len(pages) != 1 else ""
    print(f"Style check passed ({len(pages)} file{suffix}).")
    _print_candidates_hint(args, pages)
    return 0
