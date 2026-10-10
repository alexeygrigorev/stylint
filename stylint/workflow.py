"""The editing workflow an agent follows around the static check.

The static check covers mechanical rules only. This module renders the
ordered steps for each stage (draft, edit, final) and the short "next step"
footer printed after every static run, so a passing check doesn't read as
"done". Smell-pass names come from ``SMELL_PROMPTS`` (or the repo config),
so the text can't drift from the prompts the CLI ships.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import shlex

from .config import Config
from .output import pluralize

STAGES = ("draft", "edit", "final")

STAGE_SUMMARIES = {
    "draft": "read guides, write, fix-verify loop until the static check is clean",
    "edit": "same loop for changes to existing text",
    "final": "smell passes (LLM review), re-verify, then the repo's own checks",
}

CANDIDATES_PROMPT = "noun-phrase-smell"


@dataclass
class StaticStatus:
    """Result of a static run over the workflow's paths."""

    files: int
    findings: int
    files_with_findings: int
    contractions: int = 0
    candidates: int = 0

    @property
    def passed(self) -> bool:
        return self.findings == 0

    def render(self) -> str:
        if self.passed:
            return f"PASS ({pluralize(self.files, 'file')})"
        return (
            f"FAIL ({pluralize(self.findings, 'finding')} in "
            f"{pluralize(self.files_with_findings, 'file')})"
        )


@dataclass
class Context:
    """What the rendered commands should point at."""

    paths: list[str] = field(default_factory=list)
    config: Config = field(default_factory=Config)
    # Only set when the caller passed --author-name explicitly; a configured
    # author is picked up by plain `stylint`, so it isn't repeated.
    author_flag: str | None = None
    excludes: list[str] = field(default_factory=list)
    author_name: str = "Alexey"
    status: StaticStatus | None = None

    @property
    def target(self) -> str:
        if not self.paths:
            return "PATHS"
        return " ".join(shlex.quote(p) for p in self.paths)

    def check_cmd(self, *, fix: bool = False) -> str:
        parts = ["stylint"]
        if fix:
            parts.append("--fix")
        if self.author_flag is not None:
            parts += ["--author-name", shlex.quote(self.author_flag)]
        for pattern in self.excludes:
            parts += ["--exclude", shlex.quote(pattern)]
        parts.append(self.target)
        return " ".join(parts)

    def workflow_cmd(self, stage: str) -> str:
        parts = ["stylint", "--workflow", stage]
        if self.author_flag is not None:
            parts += ["--author-name", shlex.quote(self.author_flag)]
        parts.append(self.target)
        return " ".join(parts)


def _header(stage: str, ctx: Context) -> str:
    where = ctx.target if ctx.paths else "no paths given"
    details = [where]
    if ctx.status is not None:
        details.append(pluralize(ctx.status.files, "file"))
    details.append(f"author: {ctx.author_name or 'none'}")
    if ctx.config.profile:
        details.append(f"profile: {ctx.config.profile}")
    return f"Stage: {stage} ({', '.join(details)})"


def _status_line(ctx: Context) -> list[str]:
    if ctx.status is None:
        return []
    return ["", f"Static status now: {ctx.status.render()}"]


def _fix_loop(ctx: Context, start: int, write_step: str) -> list[str]:
    n = start
    return [
        f"{n}. {write_step}",
        f"{n + 1}. Auto-fix contractions:   {ctx.check_cmd(fix=True)}",
        f"{n + 2}. Static check:            {ctx.check_cmd()}",
        f"{n + 3}. Fix every finding, re-run step {n + 2}. Repeat until "
        '"Style check passed".',
    ]


def _profile_step(ctx: Context) -> list[str]:
    if ctx.config.profile != "alexey":
        return []
    return [
        "0. Brief, then draft in Alexey's voice:",
        "     stylint --style-guide alexey",
        "     stylint --prompt alexey-brief     # source notes -> brief",
        "     stylint --prompt alexey-draft     # brief -> draft",
        "   (or stylint --prompt alexey-rewrite to rewrite an existing AI draft)",
    ]


def render_draft(ctx: Context) -> str:
    lines = [_header("draft", ctx), ""]
    lines += _profile_step(ctx)
    lines += [
        "1. Read before writing (bake these in from the first sentence):",
        "     stylint --style-guide voice",
        "     stylint --style-guide formatting",
        "     stylint --style-guide code-style     # if the text has code or commands",
    ]
    lines += _fix_loop(ctx, 2, "Write one file.")
    lines += [
        "6. Repeat 2-5 for each file.",
        f"7. Continue with: {ctx.workflow_cmd('final')}",
    ]
    lines += _status_line(ctx)
    return "\n".join(lines) + "\n"


def render_edit(ctx: Context) -> str:
    lines = [
        _header("edit", ctx),
        "",
        "1. Read the guide for what you're changing:",
        "     stylint --style-guide voice          # rewriting paragraphs",
        "     stylint --style-guide formatting     # headings, lists, code blocks, links",
        "     stylint --style-guide code-style     # example code or commands",
        "     stylint --style-guide polish         # cuts and tightening",
    ]
    lines += _fix_loop(ctx, 2, "Make the edit.")
    lines += [f"6. Continue with: {ctx.workflow_cmd('final')}"]
    lines += _status_line(ctx)
    return "\n".join(lines) + "\n"


def _smell_lines(ctx: Context) -> list[str]:
    lines = []
    letters = "abcdefghijklmnopqrstuvwxyz"
    commands = []
    for name in ctx.config.smell_prompts:
        cmd = f"stylint --prompt {name}"
        note = ""
        if name == CANDIDATES_PROMPT and ctx.paths:
            cmd += f" {ctx.target}"
            if ctx.status is not None and ctx.status.candidates:
                count = ctx.status.candidates
                note = (
                    f"# {count} tool-as-actor candidate{'s' if count != 1 else ''} listed"
                )
        commands.append((cmd, note))
    width = max((len(cmd) for cmd, note in commands if note), default=0)
    for letter, (cmd, note) in zip(letters, commands):
        text = f"{cmd:<{width}}   {note}" if note else cmd
        lines.append(f"     {letter}. {text}")
    return lines


def render_final(ctx: Context) -> str:
    lines = [_header("final", ctx)]
    status = ctx.status
    if status is not None and status.passed:
        lines += [
            "",
            f"Static status now: {status.render()}. That covers mechanical rules only.",
            "These steps remain:",
        ]
    elif status is not None:
        lines += [
            "",
            f"Static status now: {status.render()}. Fix those first, using the loop from:",
            f"  {ctx.workflow_cmd('edit')}",
            "Then:",
        ]
    lines += [""]

    step = 1
    prompts = ctx.config.smell_prompts
    if prompts:
        lines += [
            f"{step}. Smell passes. Run each prompt as its own review, in a "
            "subagent, one file",
            "   (or one small folder) at a time. Don't rewrite inline.",
        ]
        lines += _smell_lines(ctx)
        lines += [
            "   Each reviewer must report every change as `original -> rewrite`,",
            '   or "no offenders" per file.',
        ]
        step += 1
        lines += [
            f"{step}. Re-verify after the rewrites:  {ctx.check_cmd()}",
            f"   Fix anything the rewrites introduced. Repeat {step - 1}-{step} "
            "only for files that changed.",
        ]
    else:
        lines += [f"{step}. Static check:  {ctx.check_cmd()}"]
    step += 1
    lines += [f"{step}. Final read with: stylint --style-guide polish"]
    step += 1
    if ctx.config.final_steps:
        lines += [f"{step}. Repo checks:"]
        lines += [f"     {item}" for item in ctx.config.final_steps]
    else:
        lines += [f"{step}. Run your project's own checks, if any."]
    lines += [f"{step + 1}. Done only when 1-{step} are all complete."]
    return "\n".join(lines) + "\n"


def render_overview(ctx: Context) -> str:
    width = max(len(s) for s in STAGES)
    lines = [
        "stylint workflow - three stages. The static check is one step, "
        "not the finish line.",
        "",
    ]
    lines += [f"  {s:<{width}}  {STAGE_SUMMARIES[s]}" for s in STAGES]
    lines += [""]
    if ctx.config.smell_prompts:
        lines += [
            "Smell passes in final: " + ", ".join(ctx.config.smell_prompts) + ".",
        ]
    if ctx.config.profile == "alexey":
        lines += [
            "Profile alexey: draft starts with the alexey-brief and "
            "alexey-draft prompts.",
        ]
    lines += [
        "",
        f"Start: {ctx.workflow_cmd('draft')}",
        f"Before saying done: {ctx.workflow_cmd('final')}",
        "Put every numbered step in your to-do list, one item each. Don't mark",
        "a smell pass done unless a reviewer actually ran it and reported changes.",
    ]
    if ctx.config.source is not None:
        lines += ["", f"Config: {ctx.config.source}"]
    lines += _status_line(ctx)
    return "\n".join(lines) + "\n"


def render_workflow(stage: str, ctx: Context) -> str:
    renderers = {
        "": render_overview,
        "draft": render_draft,
        "edit": render_edit,
        "final": render_final,
    }
    return renderers[stage](ctx)


def render_next_footer(ctx: Context) -> str:
    """The footer printed after a static run. ``ctx.status`` must be set."""
    status = ctx.status
    assert status is not None
    prompts = ctx.config.smell_prompts
    lines = [""]
    if status.passed:
        lines.append("Not done yet: the static check covers mechanical rules only.")
        if prompts:
            names = ", ".join(prompts)
            lines.append(
                f"Next: run {len(prompts)} smell "
                f"pass{'es' if len(prompts) != 1 else ''}, then re-run this check:"
            )
            lines.append(f"  {names}")
            lines.append("Full steps:")
        else:
            lines.append("Next: the final-stage steps:")
        lines.append(f"  {ctx.workflow_cmd('final')}")
    else:
        lines.append("Next: fix the findings above and re-run this check.")
        if status.contractions:
            n = status.contractions
            lines.append(
                f"{n} of them {'is a contraction' if n == 1 else 'are contractions'}, "
                "auto-fixable with:"
            )
            lines.append(f"  {ctx.check_cmd(fix=True)}")
        if prompts:
            lines.append(
                "After the check passes, the smell passes are still required:"
            )
        else:
            lines.append("After the check passes, finish the final-stage steps:")
        lines.append(f"  {ctx.workflow_cmd('final')}")
    if status.candidates and CANDIDATES_PROMPT in prompts:
        n = status.candidates
        lines.append(
            f"{n} tool-as-actor candidate{'s' if n != 1 else ''} for the "
            f"{CANDIDATES_PROMPT} pass:"
        )
        lines.append(f"  stylint --prompt {CANDIDATES_PROMPT} {ctx.target}")
    return "\n".join(lines) + "\n"
