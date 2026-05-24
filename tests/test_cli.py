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
