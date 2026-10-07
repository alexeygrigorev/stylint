"""Helpers for locating the bundled style guide."""

from __future__ import annotations

from importlib import resources
from pathlib import Path


def style_guide_path() -> Path:
    """Return the installed directory that contains the style guide docs."""
    return Path(str(resources.files("stylint.style_guide")))


def style_guide_files() -> dict[str, Path]:
    """Return style guide document names mapped to installed paths."""
    guide = style_guide_path()
    return {
        "voice": guide / "voice.md",
        "formatting": guide / "formatting.md",
        "code-style": guide / "code-style.md",
        "polish": guide / "polish.md",
        "alexey": guide / "alexey.md",
    }


def style_guide_file(name: str) -> Path:
    """Return one style guide document by short name or filename."""
    normalized = name.removesuffix(".md")
    files = style_guide_files()
    if normalized not in files:
        names = ", ".join(files)
        raise KeyError(f"unknown style guide document '{name}' (choose one of: {names})")
    return files[normalized]


def agents_guide_file() -> Path:
    """Return the short agent-facing guide document."""
    return style_guide_path() / "agents.md"


def prompt_files() -> dict[str, Path]:
    """Return drafting and review-prompt names mapped to installed paths.

    These cover source briefing, author voice, and judgment-only smells that
    no regex catches reliably."""
    guide = style_guide_path()
    return {
        "abstract-subject": guide / "prompt-abstract-subject.md",
        "noun-phrase-smell": guide / "prompt-noun-phrase-smell.md",
        "empty-rhetoric": guide / "prompt-empty-rhetoric.md",
        "simplify": guide / "prompt-simplify.md",
        "alexey-brief": guide / "prompt-alexey-brief.md",
        "alexey-draft": guide / "prompt-alexey-draft.md",
        "alexey-rewrite": guide / "prompt-alexey-rewrite.md",
    }


# One-line summaries shown by `stylint --help` and `stylint --prompt`.
# Smell checks are LLM review passes for patterns no regex catches reliably.
SMELL_PROMPTS: dict[str, str] = {
    "abstract-subject": "an abstraction is the subject ('A vague request makes this visible')",
    "noun-phrase-smell": "a tool or component stands in for our choice ('Lovable generates the frontend')",
    "empty-rhetoric": "announcements, mirrored aphorisms, staged choices, and recaps ('The star count is noise. The postmortems are signal.')",
    "simplify": "idioms, clefts, undefined terms, and repeated points for non-native readers",
}

DRAFTING_PROMPTS: dict[str, str] = {
    "alexey-brief": "turn source material into a brief before drafting",
    "alexey-draft": "draft from a brief in Alexey's voice",
    "alexey-rewrite": "rewrite an AI draft into Alexey's voice",
}


def prompt_file(name: str) -> Path:
    """Return one review-prompt document by short name."""
    normalized = name.removesuffix(".md").removeprefix("prompt-")
    files = prompt_files()
    if normalized not in files:
        names = ", ".join(files)
        raise KeyError(f"unknown review prompt '{name}' (choose one of: {names})")
    return files[normalized]
