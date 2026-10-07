"""Tests for the static tool-as-actor candidate finder."""

import sys
from pathlib import Path

import pytest

from stylint import cli
from stylint.candidates import find_candidates_in_text, tool_names
from stylint.cli import main
from stylint.styleguide import prompt_file


def found(text: str) -> list[tuple[str, tuple[str, ...]]]:
    return [(c.sentence, c.tools) for c in find_candidates_in_text(text, Path("x.md"))]


def tools_of(text: str) -> list[str]:
    return [t for _, tools in found(text) for t in tools]


@pytest.mark.parametrize("text,tool", [
    # Subject
    ("Lovable generates the React frontend.", "Lovable"),
    ("pytest runs the unit tests in CI.", "pytest"),
    ("Then Vercel took over hosting.", "Vercel"),
    ("Claude Code writes the migrations.", "Claude Code"),
    ("Railway will host the worker.", "Railway"),
    ("We wrote the spec and FastAPI runs the backend.", "FastAPI"),
    # List of tools as subject (bare plural verb)
    ("Docker, AWS, and GitHub Actions handle deployment.", "GitHub Actions"),
    ("Supabase and Streamlit cover the data side.", "Streamlit"),
    # Causative
    ("We let Lovable build the onboarding flow.", "Lovable"),
    ("Having Codex review each pull request saved hours.", "Codex"),
    # Passive agent
    ("Deployment is handled by GitHub Actions.", "GitHub Actions"),
    ("The queue is powered by Redis.", "Redis"),
    # Possessive owning a job
    ("Railway's job is hosting the worker.", "Railway"),
    ("Auth is Supabase's job.", "Supabase"),
    # Appositive and relative clause
    ("Supabase, which handles auth, needs two variables.", "Supabase"),
    ("Cloudflare, our CDN layer, sits in front of everything.", "Cloudflare"),
    # Gerund and "with" absolute
    ("With Lovable generating the UI, we focus on the API.", "Lovable"),
    # Object of a layer verb
    ("The frontend comes from Lovable.", "Lovable"),
    ("Our backend runs on FastAPI.", "FastAPI"),
    ("The search layer is built with Qdrant.", "Qdrant"),
    ("The deploy step relies on Terraform.", "Terraform"),
    # Bullet item and table cell starts
    ("- Streamlit for the dashboard", "Streamlit"),
    ("- Frontend: Lovable", "Lovable"),
    ("| Layer | Tool |\n|---|---|\n| UI | Vercel |", "Vercel"),
])
def test_each_form_is_collected(text, tool):
    assert tool in tools_of(text)


def test_pronoun_after_tool_subject():
    result = found("Railway hosts the worker. They also keep the logs.")
    assert result[1] == ("They also keep the logs.", ("Railway (via pronoun)",))


def test_pronoun_after_tool_object():
    result = found("We switched to Vercel. It hosts the site now.")
    assert ("It hosts the site now.", ("Vercel (via pronoun)",)) in result


def test_runtime_sentences_are_still_collected():
    # The finder doesn't judge role vs. runtime; the LLM prompt does.
    assert tools_of("FastAPI generates live documentation at /docs.") == ["FastAPI"]


def test_multi_word_names_win():
    assert tools_of("GitHub Actions runs the tests.") == ["GitHub Actions"]
    assert tools_of("Docker Compose starts the stack.") == ["Docker Compose"]


def test_word_like_names_need_exact_casing():
    assert found("The cursor moves to the next line.") == []
    assert found("A lovable mascot greets users.") == []
    assert found("We render the page and bolt on a footer.") == []
    assert tools_of("Render serves the API.") == ["Render"]


def test_code_blocks_and_inline_code_are_skipped():
    text = (
        "Run `Docker handles deployment` first.\n"
        "\n"
        "```bash\n"
        "Lovable generates the frontend\n"
        "```\n"
    )
    assert found(text) == []


def test_urls_link_targets_and_html_are_skipped():
    text = (
        "See [the docs](https://Lovable.dev/Lovable-generates) for more.\n"
        "\n"
        "Open https://example.com/Docker/runs today.\n"
        "\n"
        '<img alt="Docker runs" src="x.png">\n'
    )
    assert found(text) == []


def test_line_numbers_point_at_the_tool():
    text = "---\ntitle: x\n---\n\nWe planned the app.\nThen Lovable generates\nthe frontend.\n"
    [candidate] = find_candidates_in_text(text, Path("x.md"))
    assert candidate.line == 6
    assert candidate.render() == "x.md:6: [Lovable] Then Lovable generates the frontend."


def test_tool_list_has_no_generic_words():
    names = set(tool_names())
    assert {"Claude Code", "GitHub Actions", "Docker Compose", "AWS Lambda"} <= names
    assert {"Lovable", "Cursor", "Bolt", "Linear", "Render", "Railway", "pytest"} <= names
    assert not names & {"Agent", "Code", "Cloud", "Search", "Memory", "Make", "Tool"}


def write(tmp_path: Path, text: str) -> Path:
    page = tmp_path / "page.md"
    page.write_text(text)
    return page


def test_prompt_with_paths_appends_candidates(monkeypatch, capsys, tmp_path):
    page = write(tmp_path, "Lovable generates the React frontend.\n")
    monkeypatch.setattr(sys, "argv", ["stylint", "--prompt", "noun-phrase-smell", str(page)])

    assert main() == 0

    out = capsys.readouterr().out
    prompt = prompt_file("noun-phrase-smell").read_text(encoding="utf-8")
    assert out.startswith(prompt)
    tail = out[len(prompt):]
    assert "## Candidates found by stylint" in tail
    assert "Classify every candidate below as role or runtime." in tail
    assert "page.md:1: [Lovable] Lovable generates the React frontend." in tail


def test_prompt_without_paths_is_unchanged(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["stylint", "--prompt", "noun-phrase-smell"])

    assert main() == 0

    out = capsys.readouterr().out
    assert out == prompt_file("noun-phrase-smell").read_text(encoding="utf-8")


def run_check(monkeypatch, capsys, page: Path) -> tuple[int, str]:
    monkeypatch.setattr(sys, "argv", ["stylint", str(page)])
    code = main()
    return code, capsys.readouterr().out


@pytest.mark.parametrize("text", [
    "Lovable generates the React frontend.\n",
    "Lovable generates the React frontend. This is **bold**.\n",
])
def test_plain_check_prints_hint_and_keeps_exit_code(monkeypatch, capsys, tmp_path, text):
    page = write(tmp_path, text)
    code, out = run_check(monkeypatch, capsys, page)

    hints = [line for line in out.splitlines() if line.startswith("note:")]
    assert hints == [
        f"note: 1 tool-as-actor candidate; run "
        f"`stylint --prompt noun-phrase-smell {page}` to review them"
    ]

    monkeypatch.setattr(cli, "find_candidates", lambda pages: [])
    code_without, out_without = run_check(monkeypatch, capsys, page)
    assert code == code_without
    assert "note:" not in out_without
    assert out.replace(hints[0] + "\n", "") == out_without
