"""Tests for --workflow, the next-step footer, and per-repo config."""

import sys
from pathlib import Path

import pytest

from stylint.cli import main
from stylint.config import ConfigError, load_config
from stylint.styleguide import SMELL_PROMPTS

CLEAN = (
    "We use FastAPI for the backend because it has good docs and a small API, "
    "so the first version takes an afternoon.\n"
)
CONTRACTION = "We do not use a database because the data fits in a single JSON file.\n"
BOLD = "We use **FastAPI** for the backend because it has good docs and a small API.\n"


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    monkeypatch.delenv("STYLINT_NO_NEXT", raising=False)
    monkeypatch.chdir(tmp_path)


def run(monkeypatch, capsys, *argv) -> tuple[int, str]:
    monkeypatch.setattr(sys, "argv", ["stylint", *argv])
    code = main()
    return code, capsys.readouterr().out


def write(tmp_path: Path, name: str, text: str) -> Path:
    page = tmp_path / name
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(text)
    return page


# --workflow


def test_overview_lists_stages_and_smell_prompts(monkeypatch, capsys):
    code, out = run(monkeypatch, capsys, "--workflow")

    assert code == 0
    for stage in ("draft", "edit", "final"):
        assert f"  {stage}  " in out
    for name in SMELL_PROMPTS:
        assert name in out
    assert "Before saying done: stylint --workflow final PATHS" in out
    assert "Static status now" not in out


@pytest.mark.parametrize("stage", ["draft", "edit", "final"])
def test_stage_without_paths_uses_placeholder(monkeypatch, capsys, stage):
    code, out = run(monkeypatch, capsys, "--workflow", stage)

    assert code == 0
    assert out.startswith(f"Stage: {stage} (no paths given, author: Alexey)")
    assert "PATHS" in out
    assert "Static status now" not in out


def test_final_stage_is_built_from_smell_prompts(monkeypatch, capsys):
    _, out = run(monkeypatch, capsys, "--workflow", "final")

    letters = "abcd"
    for letter, name in zip(letters, SMELL_PROMPTS):
        assert f"     {letter}. stylint --prompt {name}" in out
    assert "in a subagent" in out
    assert "`original -> rewrite`" in out
    assert "2. Re-verify after the rewrites:  stylint PATHS" in out
    assert "4. Run your project's own checks, if any." in out
    assert "5. Done only when 1-4 are all complete." in out


def test_final_stage_with_paths_reports_pass(monkeypatch, capsys, tmp_path):
    page = write(tmp_path, "page.md", CLEAN)

    code, out = run(monkeypatch, capsys, "--workflow", "final", str(page))

    assert code == 0
    assert f"Stage: final ({page}, 1 file, author: Alexey)" in out
    assert "Static status now: PASS (1 file). That covers mechanical rules only." in out
    assert f"stylint --prompt noun-phrase-smell {page}" in out
    assert f"Re-verify after the rewrites:  stylint {page}" in out


def test_final_stage_with_failing_paths_points_at_edit_loop(
    monkeypatch, capsys, tmp_path
):
    page = write(tmp_path, "page.md", BOLD)

    code, out = run(monkeypatch, capsys, "--workflow", "final", str(page))

    assert code == 0
    assert "Static status now: FAIL (1 finding in 1 file)" in out
    assert f"  stylint --workflow edit {page}" in out


def test_draft_stage_substitutes_paths_and_author(monkeypatch, capsys, tmp_path):
    page = write(tmp_path, "page.md", CONTRACTION)

    code, out = run(
        monkeypatch, capsys, "--workflow", "draft", "--author-name", "Valeriia", str(page)
    )

    assert code == 0
    assert "author: Valeriia" in out
    assert f"stylint --fix --author-name Valeriia {page}" in out
    assert f"Static check:            stylint --author-name Valeriia {page}" in out
    assert f"Continue with: stylint --workflow final --author-name Valeriia {page}" in out
    assert out.rstrip().endswith("Static status now: FAIL (1 finding in 1 file)")
    assert "alexey-brief" not in out


def test_draft_stage_alexey_profile_adds_step_zero(monkeypatch, capsys):
    _, out = run(monkeypatch, capsys, "--workflow", "draft", "--profile", "alexey")

    assert "0. Brief, then draft in Alexey's voice:" in out
    assert "stylint --prompt alexey-brief" in out
    assert "stylint --prompt alexey-draft" in out


def test_workflow_accepts_a_path_in_the_stage_slot(monkeypatch, capsys, tmp_path):
    page = write(tmp_path, "docs/page.md", CLEAN)

    code, out = run(monkeypatch, capsys, "--workflow", str(page.parent))

    assert code == 0
    assert out.startswith("stylint workflow - three stages.")
    assert "Static status now: PASS (1 file)" in out


def test_workflow_rejects_unknown_stage(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["stylint", "--workflow", "polish-it"])

    assert main() == 2
    assert "Unknown workflow stage 'polish-it'" in capsys.readouterr().err


# Next-step footer


def test_passing_run_says_not_done(monkeypatch, capsys, tmp_path):
    page = write(tmp_path, "page.md", CLEAN)

    code, out = run(monkeypatch, capsys, str(page))

    assert code == 0
    assert out.startswith("Style check passed (1 file).")
    assert "Not done yet: the static check covers mechanical rules only." in out
    assert f"  {', '.join(SMELL_PROMPTS)}" in out
    assert out.rstrip().endswith(f"stylint --workflow final {page}")


def test_failing_run_with_contractions_suggests_fix(monkeypatch, capsys, tmp_path):
    page = write(tmp_path, "page.md", CONTRACTION)

    code, out = run(monkeypatch, capsys, str(page))

    assert code == 1
    assert "Next: fix the findings above and re-run this check." in out
    assert "1 of them is a contraction, auto-fixable with:" in out
    assert f"  stylint --fix {page}" in out
    assert "After the check passes, the smell passes are still required:" in out
    assert f"  stylint --workflow final {page}" in out


def test_failing_run_without_contractions_has_no_fix_hint(
    monkeypatch, capsys, tmp_path
):
    page = write(tmp_path, "page.md", BOLD)

    code, out = run(monkeypatch, capsys, str(page))

    assert code == 1
    assert "Next: fix the findings above" in out
    assert "--fix" not in out
    assert "smell passes are still required" in out


def test_default_path_footer_names_current_directory(monkeypatch, capsys, tmp_path):
    write(tmp_path, "page.md", CLEAN)

    code, out = run(monkeypatch, capsys)

    assert code == 0
    assert out.rstrip().endswith("stylint --workflow final .")


def test_no_next_flag_suppresses_footer(monkeypatch, capsys, tmp_path):
    page = write(tmp_path, "page.md", CLEAN)

    code, out = run(monkeypatch, capsys, "--no-next", str(page))

    assert code == 0
    assert out == "Style check passed (1 file).\n"


@pytest.mark.parametrize("value", ["1", "true", "yes"])
def test_env_var_suppresses_footer(monkeypatch, capsys, tmp_path, value):
    page = write(tmp_path, "page.md", BOLD)
    monkeypatch.setenv("STYLINT_NO_NEXT", value)

    code, out = run(monkeypatch, capsys, str(page))

    assert code == 1
    assert "Next:" not in out


def test_env_var_zero_keeps_footer(monkeypatch, capsys, tmp_path):
    page = write(tmp_path, "page.md", CLEAN)
    monkeypatch.setenv("STYLINT_NO_NEXT", "0")

    _, out = run(monkeypatch, capsys, str(page))

    assert "Not done yet" in out


# --print-style-guide alias


def test_print_style_guide_alias(monkeypatch, capsys):
    code, out = run(monkeypatch, capsys, "--print-style-guide", "voice")
    _, expected = run(monkeypatch, capsys, "--style-guide", "voice")

    assert code == 0
    assert out == expected
    assert out.startswith("# ")


# Config


REPO_CONFIG = """\
[tool.stylint]
author_name = "Valeriia"
profile = "alexey"
exclude = ["_docs"]

[tool.stylint.workflow]
smell_prompts = ["abstract-subject", "noun-phrase-smell"]
final_steps = [
  "uv run python scripts/check_workshops.py",
  "Walk _docs/05-01-checklist.md",
]
"""


def make_repo(tmp_path: Path, config_name="pyproject.toml", config=REPO_CONFIG):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / config_name).write_text(config)
    write(repo, "content/page.md", CLEAN)
    write(repo, "_docs/process.md", BOLD)
    return repo


def test_config_drives_final_stage(monkeypatch, capsys, tmp_path):
    repo = make_repo(tmp_path)

    code, out = run(monkeypatch, capsys, "--workflow", "final", str(repo))

    assert code == 0
    assert "author: Valeriia, profile: alexey" in out
    assert "a. stylint --prompt abstract-subject" in out
    assert "b. stylint --prompt noun-phrase-smell" in out
    assert "empty-rhetoric" not in out
    assert "4. Repo checks:\n     uv run python scripts/check_workshops.py\n" in out
    assert "     Walk _docs/05-01-checklist.md" in out
    # The configured exclude keeps _docs out, so the status passes.
    assert "Static status now: PASS (1 file)" in out


def test_config_applies_to_static_run(monkeypatch, capsys, tmp_path):
    repo = make_repo(tmp_path)
    write(repo, "content/self.md", "As Valeriia showed, the agent reads the file before it edits anything.\n")

    code, out = run(monkeypatch, capsys, str(repo))

    assert code == 1
    assert "[third-person]" in out
    assert "_docs" not in out.split("Next:")[0]
    assert "Next: fix the findings above" in out


def test_cli_author_overrides_config(monkeypatch, capsys, tmp_path):
    repo = make_repo(tmp_path)

    _, out = run(monkeypatch, capsys, "--workflow", "draft", "--author-name", "Ann", str(repo))

    assert "author: Ann" in out


def test_cli_profile_overrides_config(monkeypatch, capsys, tmp_path):
    repo = make_repo(tmp_path)

    _, out = run(monkeypatch, capsys, "--workflow", "draft", "--profile", "", str(repo))

    assert "alexey-brief" not in out


def test_dedicated_config_file(monkeypatch, capsys, tmp_path):
    config = REPO_CONFIG.replace("[tool.stylint.workflow]", "[workflow]").replace(
        "[tool.stylint]\n", ""
    )
    repo = make_repo(tmp_path, ".stylint.toml", config)

    loaded = load_config(repo / "content" / "page.md")

    assert loaded.author_name == "Valeriia"
    assert loaded.smell_prompts == ["abstract-subject", "noun-phrase-smell"]
    assert loaded.source == repo / ".stylint.toml"


def test_pyproject_without_stylint_table_is_skipped(tmp_path):
    repo = make_repo(tmp_path)
    inner = repo / "pkg"
    inner.mkdir()
    (inner / "pyproject.toml").write_text("[project]\nname = 'x'\n")

    loaded = load_config(inner)

    assert loaded.source == repo / "pyproject.toml"


def test_no_config_uses_defaults(tmp_path):
    loaded = load_config(tmp_path)

    assert loaded.source is None
    assert loaded.smell_prompts == list(SMELL_PROMPTS)
    assert loaded.final_steps == []


def test_unknown_smell_prompt_in_config_is_an_error(monkeypatch, capsys, tmp_path):
    repo = make_repo(
        tmp_path,
        config='[tool.stylint.workflow]\nsmell_prompts = ["vibes"]\n',
    )
    with pytest.raises(ConfigError):
        load_config(repo)

    monkeypatch.setattr(sys, "argv", ["stylint", str(repo)])
    assert main() == 2
    assert "unknown smell prompt(s) vibes" in capsys.readouterr().err


# Prompt files


@pytest.mark.parametrize("name", list(SMELL_PROMPTS))
def test_smell_prompts_say_subagent_and_rerun(monkeypatch, capsys, name):
    _, out = run(monkeypatch, capsys, "--prompt", name)

    assert "Run this prompt in its own subagent" in out
    assert "re-run the static" in out
