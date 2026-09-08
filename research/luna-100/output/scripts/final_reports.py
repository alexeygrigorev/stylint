#!/usr/bin/env python3
"""Recompute round comparisons from saved experiment artifacts.

Run from the repository root with uv run python. Original texts are read-only.
"""
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from tools.voice_mine import analyze

ROOT = Path('research/luna-100/output')


def save(name, data):
    (ROOT / 'reports' / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def run():
    summary = {}
    for round_name in ('round-1', 'round-2', 'round-3'):
        for split in ('development', 'holdout'):
            report = analyze(ROOT / 'manifest.json', round_name, split)
            save(f'{round_name}-{split}.json', report)
            summary[f'{round_name}-{split}'] = {k: report[k] for k in (
                'generated', 'reference', 'generated_by_mode', 'lint',
                'exact_source_overlap', 'repeated_generated_sentences')}
        report = analyze(ROOT / 'manifest.json', round_name, 'all')
        save(f'{round_name}-all.json', report)
        summary[round_name] = {k: report[k] for k in (
            'generated', 'reference', 'generated_by_mode', 'lint',
            'exact_source_overlap', 'repeated_generated_sentences')}
        print(round_name, report['generated']['documents'], report['lint']['findings'], flush=True)

    manifest = json.loads((ROOT / 'manifest.json').read_text())
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    revisions = []
    for a in manifest['articles']:
        hashes = {name: sha(ROOT / name / a['output']) for name in ('round-1', 'round-2', 'round-3')}
        revisions.append({'id': a['id'], 'hashes': hashes,
                          'changed_round_2': hashes['round-1'] != hashes['round-2'],
                          'changed_round_3': hashes['round-2'] != hashes['round-3']})
    save('round-comparison.json', summary)
    save('revision-integrity.json', {'documents': revisions,
        'round_2_changed': sum(d['changed_round_2'] for d in revisions),
        'round_3_changed': sum(d['changed_round_3'] for d in revisions)})


if __name__ == '__main__':
    run()
