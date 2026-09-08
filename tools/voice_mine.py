#!/usr/bin/env python3
"""Mine repeated generated constructions against author-selected references.

Read-only experiment tooling. It does not decide that a phrase is bad or
automatically add a lint rule. Use source-grouped holdouts for confirmation.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import statistics

from stylint import check_page
from stylint.tags import DEFAULT_OFF_TAGS
if __package__:
    from .voice_compare import features, prose_blocks, sentences
else:
    from voice_compare import features, prose_blocks, sentences


TOKENS = re.compile(r"[a-z]+(?:'[a-z]+)?|\d+", re.I)
FUNCTION_WORDS = frozenset('i we you it this that these those the a an was is were are had have has made kept gave makes keeps gives meant means because so but and then for with to of in on from into as by than enough useful important practical main easier clear same only'.split())
SHAPES = {
    'summary_label': r"\b(?:this|that|it)\s+(?:is|was)\s+(?:the|a)\s+(?:(?:main|useful|important|practical|real|small|simple)\s+)?(?:point|lesson|benefit|difference|change|result|reason)\b",
    'vague_payoff': r"\b(?:made|makes|kept|keeps)\b[^.!?]{0,65}\b(?:easier|simple|clear|manageable|useful|practical|concrete)\b",
    'vague_demonstrative': r"\b(?:this|that)\s+(?:gave|gives|meant|means|made|makes|kept|keeps|helped|helps|mattered|matters)\b",
    'enough_close': r"\b(?:that|this|it)\s+(?:was|is)\s+enough\b",
    'importance_narration': r"\b(?:the|a)\s+(?:important|useful|practical|main|key)\s+(?:part|point|detail|lesson|difference|benefit|change|result)\b",
    'intention_frame': r"\b(?:i|we)\s+(?:kept|keep|wanted|want)\b[^.!?]{0,75}\b(?:deliberately|intentionally|explicit|visible|concrete)\b",
    'scope_disclaimer': r"\b(?:this|the)\s+(?:article|post|account|example|excerpt)\s+(?:doesn't|does not|isn't|is not)\b",
    'comparison_frame': r"\b(?:not just|rather than|instead of|more than|less about)\b",
    'abstract_explanation': r"\b(?:the|this|that|those|these)\s+(?:constraint|constraints|requirement|requirements|decision|decisions|sequence|workflow|setup|choice|choices)\s+(?:made|makes|kept|keeps|meant|means|explains?|gave|gives)\b",
}


def tokenized(text: str) -> list[str]:
    return TOKENS.findall(text.lower().replace('’', "'"))


def document(path: Path) -> dict:
    text = path.read_text(encoding='utf-8')
    blocks = prose_blocks(text)
    parts = [s for p in blocks for s in sentences(p)]
    tokens = [tokenized(s) for s in parts]
    grams: Counter = Counter()
    for words in tokens:
        for size in (3, 4, 5):
            grams.update(' '.join(words[i:i + size]) for i in range(len(words) - size + 1))
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'features': features(text), 'whitespace_words': len(text.split()),
            'sentences': parts, 'grams': grams}


def summarize(docs: list[dict]) -> dict:
    measured = [d['features'] for d in docs if d['features']['words']]
    return {'documents': len(docs), 'prose_words': sum(d['words'] for d in measured),
            'median_per_document': {k: round(statistics.median(d[k] for d in measured), 3)
                                    for k in measured[0]} if measured else {}}


def analyze(manifest_path: Path, round_name: str, split: str, *, allow_partial: bool = False) -> dict:
    manifest = json.loads(manifest_path.read_text())
    root = manifest_path.parent
    assignments = [a for a in manifest['articles'] if split == 'all' or a['split'] == split]
    selected_ids = {a['source_id'] for a in assignments}
    source_rows = [s for s in manifest['sources'] if s['id'] in selected_ids]
    refs = {s['id']: document(Path(s['reference_path'])) for s in source_rows}
    candidates = []
    missing = []
    for assignment in assignments:
        path = root / round_name / assignment['output']
        if not path.is_file():
            missing.append(assignment['id'])
            continue
        row = document(path)
        row.update({'id': assignment['id'], 'source_id': assignment['source_id'], 'mode': assignment['mode']})
        row['lint'] = [{'tag': f.tag.value, 'line': f.line, 'message': f.message}
                       for f in check_page(path.parent, path) if f.tag not in DEFAULT_OFF_TAGS]
        candidates.append(row)
    if missing and not allow_partial:
        raise ValueError(f'missing {len(missing)} assigned articles: {missing}')
    if not candidates:
        raise ValueError('no generated articles to analyze')
    # When a generation batch is incomplete, compare only its actual sources.
    ids_present = {d['source_id'] for d in candidates}
    refs = {k: d for k, d in refs.items() if k in ids_present}
    ref_list = list(refs.values())
    ref_df, gen_df = Counter(), Counter()
    for doc in ref_list:
        ref_df.update(doc['grams'].keys())
    for doc in candidates:
        gen_df.update(doc['grams'].keys())
    ref_words = sum(d['features']['words'] for d in ref_list)
    gen_words = sum(d['features']['words'] for d in candidates)
    enriched = []
    for gram, count in gen_df.items():
        if count < 5 or len(FUNCTION_WORDS.intersection(gram.split())) < 2:
            continue
        reference_count = ref_df[gram]
        rate = count / len(candidates)
        ref_rate = reference_count / len(ref_list)
        if ref_rate > 0.1 or rate < 3 * ref_rate:
            continue
        enriched.append({'phrase': gram, 'generated_documents': count, 'reference_documents': reference_count,
                         'generated_document_pct': round(100 * rate, 2),
                         'reference_document_pct': round(100 * ref_rate, 2),
                         'generated_occurrences_per_10000_words': round(10000 * sum(d['grams'][gram] for d in candidates) / max(1, gen_words), 3),
                         'reference_occurrences_per_10000_words': round(10000 * sum(d['grams'][gram] for d in ref_list) / max(1, ref_words), 3),
                         'example_files': [d['id'] for d in candidates if gram in d['grams']][:8]})
    enriched.sort(key=lambda r: (-r['generated_document_pct'], r['reference_document_pct'], -len(r['phrase'])))
    shapes = {}
    for name, expression in SHAPES.items():
        regex = re.compile(expression, re.I)
        shapes[name] = {}
        for label, docs in [('reference', ref_list), ('generated', candidates)]:
            matches = [{'path': d['path'], 'sentence': sentence}
                       for d in docs for sentence in d['sentences'] if regex.search(sentence.replace('’', "'"))]
            shapes[name][label] = {'documents': len({m['path'] for m in matches}),
                                   'occurrences': len(matches), 'examples': matches[:100]}
    tags = Counter(f['tag'] for d in candidates for f in d['lint'])
    # Sentence copying uses >=12 words. prose_blocks omits blockquotes and
    # fenced code; inline quotations can still match and require review.
    overlaps = []
    sentence_df = defaultdict(set)
    for d in candidates:
        source_sentences = {' '.join(tokenized(s)) for s in refs[d['source_id']]['sentences']}
        copied = [s for s in d['sentences'] if len(tokenized(s)) >= 12 and ' '.join(tokenized(s)) in source_sentences]
        if copied:
            overlaps.append({'id': d['id'], 'exact_source_sentences': copied})
        for s in d['sentences']:
            if len(tokenized(s)) >= 12:
                sentence_df[' '.join(tokenized(s))].add(d['id'])
    repeated = [{'sentence': s, 'article_ids': sorted(ids)} for s, ids in sentence_df.items() if len(ids) >= 3]
    return {'schema_version': 1, 'round': round_name, 'split': split, 'missing': missing,
            'reference': summarize(ref_list), 'generated': summarize(candidates),
            'generated_by_mode': {mode: summarize([d for d in candidates if d['mode'] == mode]) for mode in ('account', 'explanation')},
            'lint': {'findings': sum(tags.values()), 'files_without_findings': sum(not d['lint'] for d in candidates), 'tags': dict(tags)},
            'enriched_ngrams': enriched[:300], 'exploratory_shapes': shapes,
            'exact_source_overlap': overlaps, 'repeated_generated_sentences': repeated,
            'documents': [{k: v for k, v in d.items() if k not in {'sentences', 'grams'}} for d in candidates],
            'method': 'Same-source article-body comparison. Exploratory n-grams and shapes are not approved rules. Two articles per source are correlated. Exact-sentence overlaps require review.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--round', required=True)
    parser.add_argument('--split', choices=['development', 'holdout', 'all'], default='development')
    parser.add_argument('--allow-partial', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text())
        inputs = {args.manifest.resolve()}
        for source in manifest['sources']:
            inputs.add(Path(source['reference_path']).resolve())
            if source.get('original_path'):
                inputs.add(Path(source['original_path']).resolve())
        inputs.update((args.manifest.parent / args.round / row['output']).resolve()
                      for row in manifest['articles'])
        if args.output.resolve() in inputs:
            raise ValueError('output would overwrite an input document')
        report = analyze(args.manifest, args.round, args.split, allow_partial=args.allow_partial)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(f"{report['generated']['documents']} articles; {report['lint']['findings']} findings; "
          f"{len(report['enriched_ngrams'])} exploratory phrases. Saved {args.output}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
