"""Per-repo configuration.

Stylint reads ``[tool.stylint]`` from the nearest ``pyproject.toml`` or the
top level of the nearest ``.stylint.toml``, searching upward from the first
scanned path (or the current directory). CLI flags override config values;
``--exclude`` patterns add to the configured ones.

Example::

    [tool.stylint]
    author_name = "Alexey"
    profile = "alexey"
    exclude = ["_docs", "AGENTS.md"]

    [tool.stylint.workflow]
    smell_prompts = ["abstract-subject", "noun-phrase-smell"]
    final_steps = ["uv run python scripts/check_workshops.py"]
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

try:  # Python 3.11+
    import tomllib as _toml
except ModuleNotFoundError:  # pragma: no cover - Python 3.10
    try:
        import tomli as _toml  # type: ignore[no-redef]
    except ModuleNotFoundError:
        _toml = None

from .styleguide import SMELL_PROMPTS

PROFILES = ("alexey",)


class ConfigError(ValueError):
    """Raised for an unreadable or invalid stylint config."""


@dataclass
class Config:
    author_name: str | None = None
    profile: str | None = None
    exclude: list[str] = field(default_factory=list)
    smell_prompts: list[str] = field(default_factory=lambda: list(SMELL_PROMPTS))
    final_steps: list[str] = field(default_factory=list)
    source: Path | None = None


def _read_toml(path: Path) -> dict:
    if _toml is None:
        raise ConfigError(
            f"{path}: reading config needs Python 3.11+ or the 'tomli' package"
        )
    try:
        with path.open("rb") as fh:
            return _toml.load(fh)
    except (OSError, ValueError) as exc:
        raise ConfigError(f"{path}: {exc}") from exc


def find_config_table(start: Path) -> tuple[Path, dict] | None:
    """Return (file, table) for the nearest stylint config above ``start``.

    A ``.stylint.toml`` always counts. A ``pyproject.toml`` counts only when
    it has a ``[tool.stylint]`` table, so unrelated Python projects on the
    way up don't stop the search."""
    start = start.resolve()
    directory = start if start.is_dir() else start.parent
    for candidate in (directory, *directory.parents):
        dedicated = candidate / ".stylint.toml"
        if dedicated.is_file():
            data = _read_toml(dedicated)
            return dedicated, data.get("tool", {}).get("stylint", data)
        pyproject = candidate / "pyproject.toml"
        if pyproject.is_file():
            table = _read_toml(pyproject).get("tool", {}).get("stylint")
            if table is not None:
                return pyproject, table
    return None


def _str_list(value, key: str, source: Path) -> list[str]:
    if isinstance(value, str):
        return [value]
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise ConfigError(f"{source}: '{key}' must be a list of strings")
    return list(value)


def parse_config(table: dict, source: Path) -> Config:
    config = Config(source=source)
    if "author_name" in table:
        if not isinstance(table["author_name"], str):
            raise ConfigError(f"{source}: 'author_name' must be a string")
        config.author_name = table["author_name"]
    if "profile" in table:
        profile = table["profile"]
        if profile not in PROFILES and profile not in ("", None):
            raise ConfigError(
                f"{source}: unknown profile '{profile}' "
                f"(choose one of: {', '.join(PROFILES)})"
            )
        config.profile = profile or None
    if "exclude" in table:
        config.exclude = _str_list(table["exclude"], "exclude", source)

    workflow = table.get("workflow", {})
    if not isinstance(workflow, dict):
        raise ConfigError(f"{source}: 'workflow' must be a table")
    if "smell_prompts" in workflow:
        prompts = _str_list(workflow["smell_prompts"], "workflow.smell_prompts", source)
        unknown = [p for p in prompts if p not in SMELL_PROMPTS]
        if unknown:
            raise ConfigError(
                f"{source}: unknown smell prompt(s) {', '.join(unknown)} "
                f"(choose from: {', '.join(SMELL_PROMPTS)})"
            )
        config.smell_prompts = prompts
    if "final_steps" in workflow:
        config.final_steps = _str_list(
            workflow["final_steps"], "workflow.final_steps", source
        )
    return config


def load_config(start: Path) -> Config:
    """Load the nearest config, or defaults when none exists."""
    found = find_config_table(start)
    if found is None:
        return Config()
    source, table = found
    if not isinstance(table, dict):
        raise ConfigError(f"{source}: [tool.stylint] must be a table")
    return parse_config(table, source)
