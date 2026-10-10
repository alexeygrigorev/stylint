"""Command-line interface."""

import argparse
import os
from pathlib import Path
import sys

from .discovery import iter_markdown_pages
from .lint import check_page
from .output import print_findings
from . import explanations
from .styleguide import (
    DRAFTING_PROMPTS,
    SMELL_PROMPTS,
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
from .config import PROFILES, Config, ConfigError, load_config
from .workflow import (
    CANDIDATES_PROMPT,
    STAGES,
    Context,
    StaticStatus,
    render_next_footer,
    render_workflow,
)

DEFAULT_AUTHOR_NAME = "Alexey"


def _cli_exclude_patterns(args: argparse.Namespace) -> list[str]:
    return [
        pattern.strip()
        for raw_exclude in args.exclude
        for pattern in raw_exclude.split(",")
        if pattern.strip()
    ]


def _exclude_patterns(args: argparse.Namespace, config: Config | None = None) -> list[str]:
    configured = config.exclude if config is not None else []
    return [*configured, *_cli_exclude_patterns(args)]


def _load_config(args: argparse.Namespace) -> Config:
    start = Path(args.paths[0]) if args.paths else Path.cwd()
    if not start.exists():
        start = Path.cwd()
    config = load_config(start)
    if args.profile is not None:
        config.profile = args.profile or None
    return config


def _author_name(args: argparse.Namespace, config: Config) -> str:
    if args.author_name is not None:
        return args.author_name
    if config.author_name is not None:
        return config.author_name
    return DEFAULT_AUTHOR_NAME


def _print_candidates_section(args: argparse.Namespace, config: Config) -> None:
    """Append the static tool-as-actor candidates to the printed prompt."""
    pages = iter_markdown_pages([Path(p) for p in args.paths], _exclude_patterns(args, config))
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
        + "\n\nAgent workflow: the static check is one step, not the finish line.\n"
        "Run 'stylint --workflow' for the stages (draft, edit, final), and\n"
        "'stylint --workflow final PATHS' before reporting the text as done.\n"
        "Every static run ends with a 'Next:' footer; --no-next or\n"
        "STYLINT_NO_NEXT=1 hides it.\n"
        "\nConfig: [tool.stylint] in the nearest pyproject.toml or .stylint.toml\n"
        "(author_name, profile, exclude, workflow.smell_prompts,\n"
        "workflow.final_steps). CLI flags override it."
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
        default=None,
        metavar="NAME",
        help=(
            "Name of the page's author/presenter. The third-person check "
            "flags this name as a self-reference. Defaults to 'Alexey'. "
            "Pass a guest instructor's name (e.g. --author-name Valeriia) "
            "so their own name flags while other people's names do not. "
            "Pass an empty string to disable the check. Overrides "
            "author_name in the config."
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
        "--workflow",
        metavar="STAGE",
        nargs="?",
        const="",
        help=(
            "Print the ordered editing steps for a stage ("
            + ", ".join(STAGES)
            + "), or an overview of all stages when no stage is given. "
            "With paths, the commands name those files and a static "
            "status line is added. Always exits 0."
        ),
    )
    parser.add_argument(
        "--agents",
        action="store_true",
        help="Alias for --workflow with no stage: the workflow overview.",
    )
    parser.add_argument(
        "--no-next",
        action="store_true",
        help=(
            "Don't print the 'Next:' footer after a static run. "
            "STYLINT_NO_NEXT=1 does the same."
        ),
    )
    parser.add_argument(
        "--profile",
        metavar="NAME",
        choices=[*PROFILES, ""],
        default=None,
        help=(
            "Author profile for the workflow ("
            + ", ".join(PROFILES)
            + "). 'alexey' adds the brief/draft prompts to the draft stage. "
            "Overrides profile in the config; pass '' to turn it off."
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
        "--print-style-guide",
        dest="style_guide",
        metavar="NAME",
        nargs="?",
        const="",
        help=(
            "Print the installed style guide paths. Pass a guide name "
            "(voice, formatting, code-style, polish, alexey) to print that document."
        ),
    )
    return parser.parse_args()


def _parse_tag_options(args: argparse.Namespace):
    """Return (ignore_tags, effective_off), or None after printing an error."""
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
        return None
    ignore_tags = {Tag(t) for t in ignore_list}

    raw_enable = [t.strip() for t in args.enable.split(",") if t.strip()]
    unknown_enable = [t for t in raw_enable if t not in valid_tags]
    if unknown_enable:
        print(
            f"Unknown tag(s) for --enable: {', '.join(unknown_enable)}",
            file=sys.stderr,
        )
        print("Run with --list-tags to see known tags.", file=sys.stderr)
        return None
    enable_tags = {Tag(t) for t in raw_enable}
    return ignore_tags, DEFAULT_OFF_TAGS - enable_tags


def _check_pages(pages, *, nlp, author_name, ignore_tags, effective_off):
    findings = []
    for root, page in pages:
        findings.extend(check_page(root, page, nlp=nlp, author_name=author_name))
    return [
        f for f in findings
        if f.tag not in effective_off and f.tag not in ignore_tags
    ]


def _static_status(findings, pages) -> StaticStatus:
    return StaticStatus(
        files=len(pages),
        findings=len(findings),
        files_with_findings=len({str(f.file) for f in findings}),
        contractions=sum(1 for f in findings if f.tag == Tag.CONTRACTION),
        candidates=len(find_candidates(pages)),
    )


def _context(args: argparse.Namespace, config: Config, paths: list[str]) -> Context:
    return Context(
        paths=paths,
        config=config,
        author_flag=args.author_name,
        excludes=_cli_exclude_patterns(args),
        author_name=_author_name(args, config),
    )


def _next_disabled(args: argparse.Namespace) -> bool:
    env = os.environ.get("STYLINT_NO_NEXT", "").strip().lower()
    return args.no_next or env not in ("", "0", "false", "no")


def _run_workflow(args: argparse.Namespace, stage: str) -> int:
    if stage not in ("", *STAGES) and Path(stage).exists():
        # `stylint --workflow docs/` - argparse took the path as the stage.
        args.paths = [stage, *args.paths]
        stage = ""
    if stage not in ("", *STAGES):
        print(
            f"Unknown workflow stage '{stage}'. Use one of: {', '.join(STAGES)}.",
            file=sys.stderr,
        )
        return 2
    try:
        config = _load_config(args)
    except ConfigError as exc:
        print(f"stylint config error: {exc}", file=sys.stderr)
        return 2
    ctx = _context(args, config, list(args.paths))
    if args.paths:
        tag_options = _parse_tag_options(args)
        if tag_options is None:
            return 2
        ignore_tags, effective_off = tag_options
        pages = iter_markdown_pages(
            [Path(p) for p in args.paths], _exclude_patterns(args, config)
        )
        findings = _check_pages(
            pages,
            nlp=False,
            author_name=ctx.author_name,
            ignore_tags=ignore_tags,
            effective_off=effective_off,
        )
        ctx.status = _static_status(findings, pages)
    print(render_workflow(stage, ctx), end="")
    return 0


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

    if args.workflow is not None:
        return _run_workflow(args, args.workflow)

    if args.agents:
        return _run_workflow(args, "")

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
            try:
                config = _load_config(args)
            except ConfigError as exc:
                print(f"stylint config error: {exc}", file=sys.stderr)
                return 2
            _print_candidates_section(args, config)
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

    try:
        config = _load_config(args)
    except ConfigError as exc:
        print(f"stylint config error: {exc}", file=sys.stderr)
        return 2

    tag_options = _parse_tag_options(args)
    if tag_options is None:
        return 2
    ignore_tags, effective_off = tag_options
    author_name = _author_name(args, config)

    exclude_patterns = _exclude_patterns(args, config)

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

    def run_check():
        return _check_pages(
            pages,
            nlp=args.nlp,
            author_name=author_name,
            ignore_tags=ignore_tags,
            effective_off=effective_off,
        )

    findings = run_check()

    if args.fix:
        fixed = apply_auto_fixes(findings, pages)
        if fixed:
            suffix = "s" if fixed != 1 else ""
            print(f"Auto-fixed {fixed} contraction{suffix} in place.")
        # Re-run the check to show remaining findings
        findings = run_check()

    if findings:
        print_findings(findings)
        exit_code = 1
    else:
        suffix = "s" if len(pages) != 1 else ""
        print(f"Style check passed ({len(pages)} file{suffix}).")
        exit_code = 0

    if not _next_disabled(args):
        ctx = _context(args, config, list(args.paths) or ["."])
        ctx.status = _static_status(findings, pages)
        print(render_next_footer(ctx), end="")
    return exit_code
