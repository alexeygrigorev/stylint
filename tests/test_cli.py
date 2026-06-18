"""Tests for the command-line interface."""

import sys

from stylint.cli import main


def test_cli_lists_style_guide_paths(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["stylint", "--style-guide"])

    assert main() == 0

    output = capsys.readouterr().out
    assert "voice:" in output
    assert "polish:" in output


def test_cli_prints_one_style_guide(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["stylint", "--style-guide", "voice"])

    assert main() == 0

    output = capsys.readouterr().out
    assert output.startswith("# ")


def test_cli_rejects_unknown_style_guide(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["stylint", "--style-guide", "missing"])

    assert main() == 2

    err = capsys.readouterr().err
    assert "Unknown style guide" in err
    assert "voice, formatting, code-style, polish" in err


def test_cli_prints_agents_checklist(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["stylint", "--agents"])

    assert main() == 0

    output = capsys.readouterr().out
    assert output.startswith("Use this before and after editing technical text.")
    assert "stylint --style-guide voice" in output
    assert "stylint --prompt abstract-subject" in output


def test_cli_lists_review_prompts(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["stylint", "--prompt"])

    assert main() == 0

    output = capsys.readouterr().out
    assert "abstract-subject" in output


def test_cli_prints_one_review_prompt(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["stylint", "--prompt", "abstract-subject"])

    assert main() == 0

    output = capsys.readouterr().out
    assert output.startswith("# Review prompt: abstract noun as the subject")


def test_cli_rejects_unknown_review_prompt(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["stylint", "--prompt", "missing"])

    assert main() == 2

    err = capsys.readouterr().err
    assert "Unknown review prompt" in err
    assert "abstract-subject" in err


def test_cli_help_points_agents_to_checklist(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["stylint", "--help"])

    try:
        main()
    except SystemExit as exc:
        assert exc.code == 0

    output = capsys.readouterr().out
    assert "Agent workflow" in output
    assert "stylint --agents" in output


def _write_backticks_in_link_page(tmp_path):
    folder = tmp_path / "2099-01-01-test"
    folder.mkdir()
    page = folder / "01-page.md"
    page.write_text("See [`module`](https://example.com) for details.\n")
    return folder


def test_cli_backticks_in_link_off_by_default(tmp_path, monkeypatch, capsys):
    folder = _write_backticks_in_link_page(tmp_path)
    monkeypatch.setattr(sys, "argv", ["stylint", str(folder)])

    assert main() == 0

    output = capsys.readouterr().out
    assert "backticks-in-link" not in output


def test_cli_backticks_in_link_enabled_with_flag(tmp_path, monkeypatch, capsys):
    folder = _write_backticks_in_link_page(tmp_path)
    monkeypatch.setattr(
        sys, "argv", ["stylint", str(folder), "--enable", "backticks-in-link"]
    )

    assert main() == 1

    output = capsys.readouterr().out
    assert "backticks-in-link" in output


def test_cli_rejects_unknown_enable_tag(tmp_path, monkeypatch, capsys):
    folder = _write_backticks_in_link_page(tmp_path)
    monkeypatch.setattr(
        sys, "argv", ["stylint", str(folder), "--enable", "does-not-exist"]
    )

    assert main() == 2

    err = capsys.readouterr().err
    assert "Unknown tag(s) for --enable" in err


def _write_passive_page(tmp_path):
    folder = tmp_path / "2099-01-01-passive"
    folder.mkdir()
    page = folder / "01-page.md"
    page.write_text(
        "The script deletes the file every night.\n"
        "\n"
        "The file was deleted by the script.\n"
    )
    return folder


def test_cli_passive_off_without_nlp_flag(tmp_path, monkeypatch, capsys):
    folder = _write_passive_page(tmp_path)
    monkeypatch.setattr(sys, "argv", ["stylint", str(folder)])

    assert main() == 0

    output = capsys.readouterr().out
    assert "passive-voice" not in output


def test_cli_passive_flagged_with_nlp_flag(tmp_path, monkeypatch, capsys):
    folder = _write_passive_page(tmp_path)
    monkeypatch.setattr(sys, "argv", ["stylint", str(folder), "--nlp"])

    assert main() == 1

    output = capsys.readouterr().out
    assert "passive-voice" in output
    # Passive on line 3, active (line 1) not flagged.
    assert "3:" in output
    assert output.count("passive-voice") == 1


def test_cli_passive_suppressed_with_ignore(tmp_path, monkeypatch, capsys):
    folder = _write_passive_page(tmp_path)
    monkeypatch.setattr(
        sys, "argv", ["stylint", str(folder), "--nlp", "--ignore", "passive-voice"]
    )

    assert main() == 0

    output = capsys.readouterr().out
    assert "passive-voice" not in output


def test_cli_list_tags_includes_passive_voice(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["stylint", "--list-tags"])

    assert main() == 0

    output = capsys.readouterr().out
    assert "passive-voice" in output.split()


def test_default_import_does_not_load_nltk():
    """Importing the linter's hot path must not pull in nltk, so default
    runs stay fast and the dependency stays optional."""
    import subprocess

    code = (
        "import sys, stylint.cli, stylint.lint;"
        "assert 'nltk' not in sys.modules, 'nltk imported on default path';"
        "print('ok')"
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "ok" in result.stdout
