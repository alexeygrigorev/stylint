#!/usr/bin/env python3
"""Reproducible experiment diagnostic, not a factual correctness classifier.

Run from the repository root. Reports lexical source mismatches for manual
review and brief-path mismatches. Never changes drafts or source material.
"""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path('research/luna-100/output')
STOP = set('the a an i we you he she it they me my our your his her their is are was were be been being have has had do does did will would can could should may might to of in on at for from with as by and or but if so than that this these those not no also just'.split())


def tokens(path):
    text = path.read_text().lower()
    text = re.sub(r'https?://\S+', '', text)
    return Counter(t for t in re.findall(r"[a-z][a-z0-9]+", text) if t not in STOP)


def analyze(round_name):
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    sources = {s['id']: s for s in manifest['sources']}
    counts = {s: tokens(Path(row['reference_path'])) for s, row in sources.items()}
    df = Counter(t for c in counts.values() for t in c)

    def vector(c):
        weighted = {t: (1 + math.log(n)) * (1 + math.log((len(sources) + 1) / (df[t] + 1))) for t, n in c.items()}
        norm = math.sqrt(sum(x*x for x in weighted.values())) or 1
        return {t: x / norm for t, x in weighted.items()}

    vectors = {s: vector(c) for s, c in counts.items()}
    rows = []
    for a in manifest['articles']:
        path = ROOT / round_name / a['output']
        if not path.exists():
            continue
        v = vector(tokens(path))
        scores = sorted(((sum(w * v.get(t, 0) for t, w in sv.items()), s) for s, sv in vectors.items()), reverse=True)
        assigned = next(score for score, s in scores if s == a['source_id'])
        brief = json.loads((ROOT / 'briefs' / a['brief']).read_text())
        rows.append({'id': a['id'], 'split': a['split'], 'assigned_source': a['source_id'],
                     'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                     'original_brief_path_matches': brief['source_path'] == a['source_path'],
                     'assigned_similarity': round(assigned, 4), 'nearest_source': scores[0][1],
                     'nearest_similarity': round(scores[0][0], 4),
                     'review_flag': scores[0][1] != a['source_id'] and scores[0][0] - assigned > .07})
    return {'round': round_name, 'documents': len(rows),
            'method': 'TF-IDF cosine against all 50 sources; margin > .07 flags review. A correct nearest match does not prove source fidelity. Original brief mismatches remain recorded even after a correction.',
            'flagged_ids': [r['id'] for r in rows if r['review_flag']],
            'brief_path_mismatches': [r['id'] for r in rows if not r['original_brief_path_matches']],
            'rows': rows}


if __name__ == '__main__':
    round_name = sys.argv[1]
    if round_name not in {'round-1', 'round-2', 'round-3'}:
        raise SystemExit('Expected round-1, round-2 or round-3')
    report = analyze(round_name)
    target = ROOT / 'reports' / (round_name + '-source-alignment.json')
    target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'rows'}))
