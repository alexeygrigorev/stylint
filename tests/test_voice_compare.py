"""Calibration must keep source text unchanged and avoid markup-driven metrics."""

import json
from pathlib import Path

import pytest

from tools.voice_compare import compare, features, main, prose_blocks, sentences


def test_prose_excludes_markup_but_preserves_inline_content():
    text = '''---
title: Not prose
---
# Not prose

I use `Index` with [course FAQs](https://example.org/a(b)).
This is the same paragraph.

![Image](https://example.org/a(b).png)
[![Image](https://example.org/a.png)](https://example.org)
[Share](https://example.org)
<!-- Ignore this sentence.
And this one. -->

> Someone else's words.

- A roadmap item
  with a continued sentence.

~~~python
print("Ignore this.")
~~~

    print("Indented code.")

| Table | Value |
| --- | --- |

I changed the notebook.
'''
    assert prose_blocks(text) == [
        'I use Index with course FAQs. This is the same paragraph.',
        'I changed the notebook.',
    ]


def test_inner_fence_does_not_end_longer_code_fence():
    assert prose_blocks('````md\n```python\nNot prose.\n```\n````\n\nI wrote it.') == ['I wrote it.']


def test_periods_inside_names_and_numbers_do_not_split_sentences():
    assert sentences('I teach at DataTalks.Club using version 0.1.0. Then I test it.') == [
        'I teach at DataTalks.Club using version 0.1.0.', 'Then I test it.'
    ]


def test_features_rejoin_wrapped_paragraphs_and_count_contractions():
    result = features("I'm using it because\nit works.\n\nI couldn't install Docker.")
    assert result['words'] == 10
    assert result['sentences'] == 2
    assert result['paragraphs'] == 2
    assert result['contractions_per_1000_words'] == 200
    assert result['sentence_words_median'] == 5


def test_compare_lints_only_candidates_without_modifying_sources(tmp_path):
    ref = tmp_path / 'reference.md'
    candidate = tmp_path / 'candidate.md'
    # An intentional reference violation must not appear as a lint result.
    ref.write_text('I **like** this library because it works in my notebook.\n')
    candidate.write_text('I **built** this library to use in a notebook.\n')
    before = {p: p.read_bytes() for p in (ref, candidate)}
    report = compare(ref, candidate)
    assert 'lint' not in report['reference']
    assert 'lint' not in report['reference']['documents'][0]
    assert report['candidate']['lint']['tags']['bold'] == 1
    assert all(p.read_bytes() == data for p, data in before.items())
    assert len(report['reference']['documents'][0]['sha256']) == 64


def test_compare_rejects_overlap_and_empty_prose(tmp_path):
    ref = tmp_path / 'reference.md'
    ref.write_text('I wrote a short article.')
    with pytest.raises(ValueError, match='overlap'):
        compare(ref, ref)
    candidate = tmp_path / 'candidate.md'
    candidate.write_text('# Only a heading\n')
    with pytest.raises(ValueError, match='no measurable'):
        compare(ref, candidate)
    with pytest.raises(ValueError, match='does not exist'):
        compare(tmp_path / 'missing', candidate)


def test_cli_writes_json_and_refuses_to_overwrite_input(tmp_path, monkeypatch):
    ref = tmp_path / 'reference.md'
    candidate = tmp_path / 'candidate.md'
    for path in (ref, candidate):
        path.write_text('I wrote this because it explains what I needed.')
    output = tmp_path / 'report.json'
    argv = ['voice_compare', '--reference', str(ref), '--candidate', str(candidate), '--output']
    monkeypatch.setattr('sys.argv', argv + [str(output)])
    assert main() == 0
    assert json.loads(output.read_text())['reference']['files'] == 1
    monkeypatch.setattr('sys.argv', argv + [str(ref)])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert ref.read_text() == candidate.read_text()
