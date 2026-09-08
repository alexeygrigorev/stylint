"""Empirically selected rules must preserve structural and semantic exceptions."""

from pathlib import Path

import pytest

from stylint import Tag, check_page
from stylint.cli import main


DENSE = (
    'I put the search examples in one notebook so participants could run the lesson without setting up a separate server. '
    'They used the same dataset in each exercise and could look at the results immediately after changing their query. '
    'I kept the examples together because installing another service would take time away from the retrieval lesson we were teaching.'
)


def findings(tmp_path: Path, text: str, tag: Tag):
    page = tmp_path / 'article.md'
    page.write_text(text)
    return [finding for finding in check_page(tmp_path, page) if finding.tag == tag]


@pytest.mark.parametrize('text', [
    'The useful part is that I can resume the session.',
    'The important part for me was the saved baseline.',
    'For me, the interesting part is that I can read the implementation.',
    'That was the point of the exercise: save a baseline first.',
    "That's the main lesson I took from the exercise.",
    'I saved the baseline first. The practical part is that I can compare both runs.',
    'The useful part\nis that I can resume the session.',
])
def test_evaluative_framing_positive(tmp_path, text):
    assert len(findings(tmp_path, text, Tag.EVALUATIVE_FRAMING)) == 1


@pytest.mark.parametrize('text', [
    'The main difference is the type of code FDEs write.',
    'The valuable part is what you learn from doing the project.',
    'The important thing is to keep experimenting.',
    'That was enough to start building the web interface.',
    'That was the reason I switched to a persistent index.',
    'I keep an important part of the configuration in this file.',
    '> The useful part is that I can resume the session.',
    '```text\nThe useful part is that I can resume the session.\n```',
    'I rejected "The useful part is that I can resume the session."',
    'I rejected “The useful part is that I can resume the session.”',
    'I searched for `The useful part is` in the draft.',
    '# The useful part is the baseline\n\nI saved the baseline.',
])
def test_evaluative_framing_preserves_contextual_exceptions(tmp_path, text):
    assert not findings(tmp_path, text, Tag.EVALUATIVE_FRAMING)


def test_evaluative_framing_reports_original_line_with_frontmatter(tmp_path):
    text = '---\ntitle: Draft\n---\n\nI saved the baseline.\n\nThe useful part\nis that I can compare the results.\n'
    assert findings(tmp_path, text, Tag.EVALUATIVE_FRAMING)[0].line == 7


def test_dense_paragraph_run_fires_once_for_whole_run(tmp_path):
    matches = findings(tmp_path, '\n\n'.join([DENSE] * 7), Tag.DENSE_PARAGRAPH_RUN)
    assert len(matches) == 1
    assert matches[0].line == 1
    assert '7 consecutive paragraphs' in matches[0].message


@pytest.mark.parametrize('text', [
    '\n\n'.join([DENSE] * 3),
    '\n\n'.join(['I ran it. It worked. I checked again.'] * 6),
    '\n\n'.join([DENSE, DENSE, 'I checked the results before continuing.', DENSE, DENSE]),
    '\n\n'.join([DENSE, DENSE, '## Next stage', DENSE, DENSE]),
    '\n\n'.join([DENSE, DENSE, '- A list item', DENSE, DENSE]),
    '\n\n'.join([DENSE, DENSE, '```python\nprint(1)\n```', DENSE, DENSE]),
    '\n\n'.join([DENSE, DENSE, '> An exact quotation.', DENSE, DENSE]),
    '\n\n'.join([DENSE, DENSE, '<!-- A structural boundary -->', DENSE, DENSE]),
    '```text\n' + '\n\n'.join([DENSE] * 4) + '\n```',
    '\n\n'.join(['> ' + DENSE] * 4),
])
def test_dense_run_respects_short_paragraphs_and_structural_boundaries(tmp_path, text):
    assert not findings(tmp_path, text, Tag.DENSE_PARAGRAPH_RUN)


def test_dense_run_handles_wrapping_and_frontmatter(tmp_path):
    wrapped = DENSE.replace(' They used', '\nThey used').replace(' I kept', '\nI kept')
    text = '---\ntitle: Draft\n---\n\n' + '\n\n'.join([wrapped] * 4)
    match = findings(tmp_path, text, Tag.DENSE_PARAGRAPH_RUN)[0]
    assert match.line == 5
    assert 'lines 5, 9, 13, 17' in match.message


def test_dense_rule_can_report_separate_runs(tmp_path):
    text = '\n\n'.join([DENSE] * 4 + ['I checked the results before continuing.'] + [DENSE] * 4)
    assert len(findings(tmp_path, text, Tag.DENSE_PARAGRAPH_RUN)) == 2


@pytest.mark.parametrize('tag', ['dense-paragraph-run', 'evaluative-framing'])
def test_new_tags_have_cli_explanations(monkeypatch, capsys, tag):
    monkeypatch.setattr('sys.argv', ['stylint', '--explain', tag])
    assert main() == 0
    assert capsys.readouterr().out.startswith(tag)
