"""Tests for the stylint package import surface."""

from stylint import (
    Finding,
    Tag,
    check_page,
    count_sentences,
    find_gerund_starts,
    style_guide_file,
    style_guide_files,
    style_guide_path,
)
from stylint.discovery import iter_markdown_pages


def test_package_exports_public_api():
    assert Tag.BOLD.value == "bold"
    assert Finding.__name__ == "Finding"
    assert check_page.__name__ == "check_page"
    assert count_sentences("One. Two.") == 2
    assert find_gerund_starts("Reading this, we see the point.") == ["Reading"]


def test_package_exposes_discovery_helpers():
    assert iter_markdown_pages([]) == []


def test_package_exposes_bundled_style_guide():
    guide_path = style_guide_path()
    files = style_guide_files()

    assert guide_path.is_dir()
    assert set(files) == {"voice", "formatting", "code-style", "polish"}
    for path in files.values():
        assert path.is_file()
        assert path.parent == guide_path


def test_package_exposes_one_style_guide_doc():
    path = style_guide_file("voice")
    assert path.name == "voice.md"
    assert path.read_text(encoding="utf-8").startswith("# ")

    same_path = style_guide_file("voice.md")
    assert same_path == path
