"""Keep exploratory calibration separate from holdouts and source edits."""

import hashlib
import json
from pathlib import Path

import pytest

from tools.voice_mine import analyze, main


def experiment(tmp_path: Path):
    sources = []
    articles = []
    folder = tmp_path / 'round-1'
    folder.mkdir()
    for number in range(1, 7):
        split = 'holdout' if number == 6 else 'development'
        source = tmp_path / f'source-{number}.md'
        source.write_text(f'I used library {number} because it worked in the notebook.')
        sources.append({'id': str(number), 'reference_path': str(source), 'split': split})
        output = f'{number}.md'
        phrase = 'This kept the workflow manageable while I worked on the example every morning.'
        if split == 'holdout':
            phrase = 'This secret holdout sentence must stay outside development analysis.'
        (folder / output).write_text(phrase)
        articles.append({'id': str(number), 'source_id': str(number), 'split': split,
                         'mode': 'account', 'output': output})
    manifest = tmp_path / 'manifest.json'
    manifest.write_text(json.dumps({'sources': sources, 'articles': articles}))
    return manifest


def test_mining_excludes_held_out_source_and_drafts(tmp_path):
    manifest = experiment(tmp_path)
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in tmp_path.rglob('*') if p.is_file()}
    report = analyze(manifest, 'round-1', 'development')
    assert report['reference']['documents'] == 5
    assert report['generated']['documents'] == 5
    assert 'secret holdout' not in json.dumps(report)
    assert any(r['phrase'] == 'this kept the' and r['reference_documents'] == 0
               for r in report['enriched_ngrams'])
    assert report['repeated_generated_sentences'][0]['article_ids'] == ['1', '2', '3', '4', '5']
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == digest for p, digest in before.items())


def test_partial_generation_is_explicit(tmp_path):
    manifest = experiment(tmp_path)
    (tmp_path / 'round-1/1.md').unlink()
    with pytest.raises(ValueError, match='missing 1'):
        analyze(manifest, 'round-1', 'development')
    report = analyze(manifest, 'round-1', 'development', allow_partial=True)
    assert report['missing'] == ['1']
    assert report['reference']['documents'] == 4


def test_mining_rejects_output_that_overwrites_an_input(tmp_path, monkeypatch):
    manifest = experiment(tmp_path)
    monkeypatch.setattr('sys.argv', ['voice_mine', '--manifest', str(manifest),
                                    '--round', 'round-1', '--output', str(tmp_path / 'source-1.md')])
    original = (tmp_path / 'source-1.md').read_bytes()
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert (tmp_path / 'source-1.md').read_bytes() == original


def test_source_sentence_overlap_has_evidence(tmp_path):
    manifest = experiment(tmp_path)
    text = 'I used a small library for the course because participants needed search in a single notebook.'
    (tmp_path / 'source-1.md').write_text(text)
    (tmp_path / 'round-1/1.md').write_text(text)
    report = analyze(manifest, 'round-1', 'development')
    assert report['exact_source_overlap'] == [{'id': '1', 'exact_source_sentences': [text]}]
