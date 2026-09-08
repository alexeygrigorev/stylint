# Implementation guideline

## Current behavior and evidence

The live repository has mechanical Markdown checks, optional NLP checks, bundled guides and two review prompts. `style-experiment/README.md` requires 250 synthetic drafts to follow one template and allows invented details. That corpus is useful for stress-testing rules but cannot validate author voice or factual fidelity.

The archive contains 54 Markdown posts. Selected primary texts and limitations are indexed in sources/index.yaml. Voice inferences are in wiki/synthesis.md. The phone article explicitly describes AI drafting and human/editor revision.

## Desired behavior and acceptance criteria

Make a reusable, source-grounded author profile, a drafting prompt and a correction prompt available through existing stylint interfaces. Run Luna expansions from fact-preserving summaries, record untouched baseline drafts, compare prompt-only drafts, and demonstrate corrected drafts with full stylint checks. Preserve failure findings and uncertainty. Add a reproducible, read-only comparison tool for descriptive text metrics and generated-draft lint findings.

## Design and alternatives

Add an optional alexey guide and alexey-draft/alexey-rewrite prompts. Keep existing generic rules and defaults compatible. Use positive voice guidance before the existing judgment prompts. Do not add regex bans from a small synthetic sample or force the archive to pass the checker. Reject a single human-likeness score: overlap with a corpus metric is not evidence of preference. Reject fixed length, compulsory anecdotes, invented numbers, compulsory roadmaps and compulsory subscribe lines.

## Interfaces, data and dependencies

Extend stylint/styleguide.py registries and CLI help; Markdown package data already includes new guides. Add tools/voice_compare.py using the standard library plus the installed stylint API. Save source paths and SHA-256 hashes, cleaning policy, per-file features and aggregate summaries. Lint candidates only. Keep reference sources unchanged. No external service or API dependency beyond the explicitly requested built-in Luna agents.

## Compatibility and migration

All changes are additive. Existing CLI lint behavior and public check_page signature stay unchanged. No migration, release, publishing or adjacent-repository changes. Rollback removes added guide/prompt registrations and the standalone tool.

## Failure modes and observability

Markdown and sentence parsing is approximate: omit frontmatter, images, code, quotes and standalone links; separate visible prose from lists/headings; report counts and per-file rows. Describe whole-newsletter contamination and short-excerpt/long-article differences. Reject empty corpora and reference/candidate overlap. Preserve factual ledgers and source locations to detect inventions and missing caveats independently of lint. Do not infer model training or human approval from generated examples.

## Ordered tasks and verification

1. Measure reference and old synthetic distributions; add corpus-parser tests for markup and empty inputs.
2. Draft profile and prompts from selected sources, with supported examples and exceptions.
3. Run separate Luna contexts on identical briefs: neutral baseline and guided expansion. Reserve a new topic for a later smoke test after prompt revision.
4. Review differences, revise prompts if needed, preserve raw drafts and save correction examples with reasons and factual checks.
5. Run full stylint on corrected AI prose without ignored tags. Explain any unresolved conflict instead of deleting facts to obtain zero.
6. Test registry and CLI discovery, run the repository test suite, compare archive hashes, and write a concise report and commands.

## Documentation

Add a README workflow with the new prompt commands and link to the experiment report. Keep research files internal. Preserve synthetic status and generation provenance in experiment metadata, outside article bodies.

## Blocking questions

None for implementation. The author must judge preference before these examples can be called human-validated training data.
