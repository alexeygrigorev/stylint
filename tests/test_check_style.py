"""Tests for scripts/check_style.py."""

from pathlib import Path

import pytest

from check_style import (
    check_page,
    count_sentences,
    find_gerund_starts,
)


def make_page(tmp_path: Path, body: str, name: str = "01-page.md") -> tuple[Path, Path]:
    """Create a workshop folder with one markdown page; return (root, page)."""
    folder = tmp_path / "2099-01-01-test"
    folder.mkdir()
    page = folder / name
    page.write_text(body)
    return tmp_path, page


# ---------------------------------------------------------------------------
# Helper-function tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text, expected",
    [
        ("One sentence.", 1),
        ("One. Two. Three.", 3),
        ("Question? Exclaim! Statement.", 3),
        ("", 0),
    ],
)
def test_count_sentences_plain(text, expected):
    assert count_sentences(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Use foo, e.g. bar.", 1),
        ("This is fine, i.e. so on.", 1),
        ("Do x, y, etc. and stop.", 1),
    ],
)
def test_count_sentences_ignores_abbreviations(text, expected):
    assert count_sentences(text) == expected


def test_count_sentences_ignores_periods_in_backticks():
    # Three real sentences; the backticked code has dots that should be ignored.
    text = "Run `a.b.c.d`. Then look. Then stop."
    assert count_sentences(text) == 3


def test_find_gerund_starts_flags_leading_gerund():
    assert find_gerund_starts("Reading through it, I see X") == ["Reading"]


@pytest.mark.parametrize(
    "text",
    [
        "Spring is fine",
        "String parsing is fine",
        "We are running tests",
    ],
)
def test_find_gerund_starts_negative(text):
    assert find_gerund_starts(text) == []


# ---------------------------------------------------------------------------
# Frontmatter blank-line rule
# ---------------------------------------------------------------------------


def test_frontmatter_missing_blank_line(tmp_path):
    body = "---\ntitle: x\ncontent_id: a\n---\nBody starts immediately.\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert any("insert a blank line between frontmatter and body" in e for e in errors)


def test_frontmatter_with_blank_line_is_clean(tmp_path):
    body = "---\ntitle: x\ncontent_id: a\n---\n\nBody after blank line.\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert not any("blank line between frontmatter" in e for e in errors)


# ---------------------------------------------------------------------------
# Banned word
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("word", ["very", "delve", "faithful"])
def test_banned_word_positive(tmp_path, word):
    root, page = make_page(tmp_path, f"This is {word} important.\n")
    errors = check_page(root, page)
    assert any(f"banned word '{word}'" in e for e in errors)


def test_banned_word_negative(tmp_path):
    root, page = make_page(tmp_path, "This is fine prose with no flagged words.\n")
    errors = check_page(root, page)
    assert not any("banned word" in e for e in errors)


# ---------------------------------------------------------------------------
# Banned phrase, single line
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "phrase",
    [
        "at this point",
        "the shape of",
        "on the wire",
        "tight inner loop",
        "reusable principle",
    ],
)
def test_banned_phrase_single_line_positive(tmp_path, phrase):
    root, page = make_page(tmp_path, f"We talk about {phrase} here.\n")
    errors = check_page(root, page)
    assert any(f"banned phrase '{phrase}'" in e for e in errors)


def test_banned_phrase_single_line_negative(tmp_path):
    root, page = make_page(tmp_path, "We talk about the design and move on.\n")
    errors = check_page(root, page)
    assert not any("banned phrase" in e for e in errors)


# ---------------------------------------------------------------------------
# Banned phrase, across lines
# ---------------------------------------------------------------------------


def test_banned_phrase_across_lines(tmp_path):
    body = "We name this a reusable\nprinciple for the team.\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert any(
        "banned phrase 'reusable principle' across lines" in e for e in errors
    )


def test_banned_phrase_across_lines_does_not_double_fire(tmp_path):
    body = "This is a reusable principle for the team.\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert not any("across lines" in e for e in errors)
    assert any("banned phrase 'reusable principle'" in e for e in errors)


# ---------------------------------------------------------------------------
# Line-number accuracy with frontmatter
# ---------------------------------------------------------------------------


def test_line_numbers_account_for_frontmatter(tmp_path):
    body = (
        "---\n"
        "title: Test\n"
        "content_id: abc\n"
        "---\n"
        "\n"
        "First paragraph is fine.\n"
        "\n"
        "Second paragraph has a banned word: delve into this.\n"
    )
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    banned_errors = [e for e in errors if "banned word 'delve'" in e]
    assert len(banned_errors) == 1
    assert ":8:" in banned_errors[0]


def test_line_numbers_across_lines_with_frontmatter(tmp_path):
    body = (
        "---\n"
        "title: Test\n"
        "content_id: abc\n"
        "---\n"
        "\n"
        "First paragraph is fine.\n"
        "\n"
        "We describe the shape of\n"
        "the thing here.\n"
    )
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    phrase_errors = [e for e in errors if "the shape of" in e]
    assert len(phrase_errors) == 1
    assert ":8:" in phrase_errors[0]


# ---------------------------------------------------------------------------
# Banned opener
# ---------------------------------------------------------------------------


def test_banned_opener_positive(tmp_path):
    root, page = make_page(tmp_path, "Additionally, we wire up the handler.\n")
    errors = check_page(root, page)
    assert any("banned opener 'Additionally'" in e for e in errors)


def test_banned_opener_negative(tmp_path):
    root, page = make_page(tmp_path, "We wire up the handler.\n")
    errors = check_page(root, page)
    assert not any("banned opener" in e for e in errors)


# ---------------------------------------------------------------------------
# Question-word heading
# ---------------------------------------------------------------------------


def test_question_word_heading_positive(tmp_path):
    root, page = make_page(tmp_path, "## Why this matters\n\nSome prose here.\n")
    errors = check_page(root, page)
    assert any("avoid question-word headings" in e for e in errors)


def test_question_word_heading_negative(tmp_path):
    root, page = make_page(tmp_path, "## Reasons this matters\n\nSome prose here.\n")
    errors = check_page(root, page)
    assert not any("avoid question-word headings" in e for e in errors)


# ---------------------------------------------------------------------------
# Heading depth (### or deeper)
# ---------------------------------------------------------------------------


def test_heading_depth_positive(tmp_path):
    body = "## Section\n\nLead-in.\n\n### subsection\n\nMore prose here.\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert any("heading depth ### or deeper not allowed" in e for e in errors)


def test_heading_depth_negative(tmp_path):
    body = "## Section\n\nLead-in.\n\n## Another section\n\nMore prose here.\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert not any("heading depth" in e for e in errors)


# ---------------------------------------------------------------------------
# Code block missing language tag
# ---------------------------------------------------------------------------


def test_code_block_missing_language_positive(tmp_path):
    body = "Lead-in prose.\n\n```\nprint('hi')\n```\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert any("code block missing language tag" in e for e in errors)


def test_code_block_with_language_negative(tmp_path):
    body = "Lead-in prose.\n\n```python\nprint('hi')\n```\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert not any("missing language tag" in e for e in errors)


# ---------------------------------------------------------------------------
# Code block longer than 40 lines
# ---------------------------------------------------------------------------


def test_code_block_too_long_positive(tmp_path):
    code_lines = "\n".join(f"line_{i} = {i}" for i in range(45))
    body = f"Lead-in prose.\n\n```python\n{code_lines}\n```\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert any("code block has 45 lines" in e for e in errors)


def test_code_block_short_negative(tmp_path):
    body = "Lead-in prose.\n\n```python\nprint('hi')\n```\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert not any("code block has" in e for e in errors)


# ---------------------------------------------------------------------------
# Code block needs lead-in after heading
# ---------------------------------------------------------------------------


def test_code_block_lead_in_required_positive(tmp_path):
    body = "## Section\n\n```python\nprint('hi')\n```\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert any("code block needs a lead-in sentence" in e for e in errors)


def test_code_block_lead_in_required_negative(tmp_path):
    body = "## Section\n\nLead-in prose for the code below.\n\n```python\nprint('hi')\n```\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert not any("code block needs a lead-in" in e for e in errors)


# ---------------------------------------------------------------------------
# List needs lead-in after heading
# ---------------------------------------------------------------------------


def test_list_lead_in_required_positive(tmp_path):
    body = "## Section\n\n- first item\n- second item\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert any("list needs a lead-in sentence" in e for e in errors)


def test_list_lead_in_required_negative(tmp_path):
    body = "## Section\n\nThe list below covers the main steps.\n\n- first item\n- second item\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert not any("list needs a lead-in" in e for e in errors)


# ---------------------------------------------------------------------------
# Consecutive code blocks
# ---------------------------------------------------------------------------


def test_consecutive_code_blocks_positive(tmp_path):
    body = (
        "Lead-in prose.\n\n"
        "```python\nprint('a')\n```\n\n"
        "```python\nprint('b')\n```\n"
    )
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert any("consecutive code blocks need prose between them" in e for e in errors)


def test_consecutive_code_blocks_negative(tmp_path):
    body = (
        "Lead-in prose.\n\n"
        "```python\nprint('a')\n```\n\n"
        "Bridge prose between blocks.\n\n"
        "```python\nprint('b')\n```\n"
    )
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert not any("consecutive code blocks" in e for e in errors)


# ---------------------------------------------------------------------------
# Bold / italic / smart quotes / em dash / table row
# ---------------------------------------------------------------------------


def test_bold_markdown_flagged(tmp_path):
    root, page = make_page(tmp_path, "This is **bold** text.\n")
    errors = check_page(root, page)
    assert any("bold markdown is not used" in e for e in errors)


def test_italic_markdown_flagged(tmp_path):
    root, page = make_page(tmp_path, "This is *italic* text.\n")
    errors = check_page(root, page)
    assert any("italic markdown is not used" in e for e in errors)


def test_smart_quote_flagged(tmp_path):
    root, page = make_page(tmp_path, "He said “hello” there.\n")
    errors = check_page(root, page)
    assert any("smart double quote" in e for e in errors)


def test_em_dash_flagged(tmp_path):
    root, page = make_page(tmp_path, "We use this — sometimes.\n")
    errors = check_page(root, page)
    assert any("use a hyphen instead of an em dash" in e for e in errors)


def test_table_row_flagged(tmp_path):
    body = "Lead-in.\n\n| col1 | col2 |\n"
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert any("markdown tables are not used" in e for e in errors)


def test_clean_prose_no_format_flags(tmp_path):
    root, page = make_page(tmp_path, "Plain prose with no special formatting.\n")
    errors = check_page(root, page)
    for needle in (
        "bold markdown",
        "italic markdown",
        "smart double quote",
        "em dash",
        "markdown tables",
    ):
        assert not any(needle in e for e in errors)


# ---------------------------------------------------------------------------
# Bare URL in prose
# ---------------------------------------------------------------------------


def test_bare_url_positive(tmp_path):
    root, page = make_page(tmp_path, "Read more at https://example.com here.\n")
    errors = check_page(root, page)
    assert any("bare URL in prose" in e for e in errors)


def test_bare_url_negative_with_named_link(tmp_path):
    root, page = make_page(tmp_path, "Read more at [the docs](https://example.com).\n")
    errors = check_page(root, page)
    assert not any("bare URL" in e for e in errors)


# ---------------------------------------------------------------------------
# Backticks inside link text
# ---------------------------------------------------------------------------


def test_backticks_in_link_text_positive(tmp_path):
    root, page = make_page(tmp_path, "See [`module`](https://example.com) for details.\n")
    errors = check_page(root, page)
    assert any("backticks inside link text" in e for e in errors)


def test_backticks_in_link_text_negative(tmp_path):
    root, page = make_page(tmp_path, "See [the module](https://example.com) for details.\n")
    errors = check_page(root, page)
    assert not any("backticks inside link text" in e for e in errors)


# ---------------------------------------------------------------------------
# Alexey mention
# ---------------------------------------------------------------------------


def test_alexey_mention_positive(tmp_path):
    root, page = make_page(tmp_path, "Then Alexey opens the file.\n")
    errors = check_page(root, page)
    assert any("third-person presenter references" in e for e in errors)


def test_alexey_mention_negative(tmp_path):
    root, page = make_page(tmp_path, "Then we open the file.\n")
    errors = check_page(root, page)
    assert not any("third-person presenter references" in e for e in errors)


# ---------------------------------------------------------------------------
# Paragraph longer than 5 sentences
# ---------------------------------------------------------------------------


def test_paragraph_too_long_positive(tmp_path):
    paragraph = " ".join(f"Sentence number {i}." for i in range(1, 7))
    root, page = make_page(tmp_path, paragraph + "\n")
    errors = check_page(root, page)
    assert any("paragraph has 6 sentences" in e for e in errors)


def test_paragraph_short_enough_negative(tmp_path):
    paragraph = "One. Two. Three."
    root, page = make_page(tmp_path, paragraph + "\n")
    errors = check_page(root, page)
    assert not any("paragraph has" in e for e in errors)


# ---------------------------------------------------------------------------
# Gerund-leading sentence
# ---------------------------------------------------------------------------


def test_gerund_leading_sentence_positive(tmp_path):
    root, page = make_page(tmp_path, "Reading through it, I see the bug.\n")
    errors = check_page(root, page)
    assert any("sentence opens with '-ing' word 'Reading'" in e for e in errors)


def test_gerund_leading_sentence_negative(tmp_path):
    root, page = make_page(tmp_path, "Spring loaded values appear here.\n")
    errors = check_page(root, page)
    assert not any("sentence opens with '-ing'" in e for e in errors)


# ---------------------------------------------------------------------------
# Smoke test: clean known-good page
# ---------------------------------------------------------------------------


def test_clean_page_has_no_errors(tmp_path):
    body = (
        "---\n"
        "title: Sample\n"
        "content_id: sample\n"
        "---\n"
        "\n"
        "This is the opening paragraph that introduces the page.\n"
        "\n"
        "## Section\n"
        "\n"
        "The list below names the steps we take.\n"
        "\n"
        "- first step\n"
        "- second step\n"
        "\n"
        "Then we run the command.\n"
        "\n"
        "```python\n"
        "print('ok')\n"
        "```\n"
    )
    root, page = make_page(tmp_path, body)
    errors = check_page(root, page)
    assert errors == []
