# Implementation guideline

## Current behavior

The initial pilot added three prompts and a profile but no new rules. The current linter combines line, paragraph and file checks with explainable tags. Existing generic bans can already flag author archive text. The new work explicitly authorizes diagnostic comparison with author writing to calibrate new rules; no reference text will be edited.

## Desired behavior and acceptance

Generate exactly 100 original Luna drafts, two different treatments of each of 50 substantive archive sources. Each draft should be a standalone 450–750 word article grounded in the source, with a separate fact brief. Preserve originals. Reserve both drafts from ten sources (20 drafts) for held-out evaluation. Add multiple new deterministic checks supported by recurring development examples and low author-reference incidence. Include positive and negative regression tests and explanations.

Iterate prompts and all drafts, preserving each round. Stop when the full corpus passes mechanical checks or specific unavoidable source conflicts are documented, required facts remain covered on audit, new-rule rates drop substantially on the held-out cases, and a fresh review finds no new recurring high-confidence AI construction worth turning into a rule. If review finds another recurring defect, perform another targeted round. Record distribution shifts and residual limitations instead of claiming a universal human-likeness score.

## Chosen design

Use built-in Luna agents in three file-owned batches for generation and revision. The parent handles corpus analysis, implementation and verification. Mine repeated n-grams and sentence shapes on the 80 development drafts before opening held-out text. A candidate should normally occur in at least five development drafts and at most 5% of reference documents, with a substantially higher normalized generated rate. Inspect all reference matches and development examples. Lower-support checks require explicit reasoning and should not be sold as empirically common. Do not ban words the author commonly uses just because synthetic drafts also use them.

## Interfaces and compatibility

Use existing patterns/rules, Tag and explanations APIs. Add paragraph or file context where line regexes would miss wrapping or cause false positives. Keep public APIs compatible. No new runtime dependency. Add reusable experiment analysis scripts and JSON reports. Preserve original source hashes and all prior changes. No publication or package release.

## Failure modes

Sources include collaborative editing and some historical claims. Preserve historical context and attribution; do not invent personal experiences or new results. Multiple drafts per source are correlated, so report source-grouped counts and do not call them independent observations. Shared generation instructions affect baselines. Keyword metrics are diagnostic, not a preference classifier. Rule-specific checks on reference texts are read-only calibration authorized by this request.

## Implementation sequence

1. Freeze source selection, grouped split, prompt snapshots and agent assignments.
2. Generate the 100 drafts with supporting briefs; verify count, length, attribution and duplicate text.
3. Analyze development versus reference prevalence; inspect candidate examples and reject overbroad rules.
4. Implement checks, negative examples and explain output; freeze rules before evaluating held-out drafts.
5. Revise drafts with source briefs, updated prompts and full stylint; preserve each round and record edits.
6. Repeat targeted review/correction if findings or recurring defects remain. Review final factual coverage and copying from references.
7. Run full tests, packaged-resource checks as needed, archive hash verification and provenance lint. Write the final report and before/after measurements.

## Rejected alternatives

Do not reuse the old synthetic corpus as the 100 requested Luna articles. Do not use template generation, arbitrary new bans, a single voice score, or only parent rewrites. Do not alter raw drafts after generation or test rules only on their motivating examples.

## Documentation and open questions

Update guide prompts with observed positive alternatives and describe new tags through --explain. Preserve missing human preference validation as a limitation, not a blocker to the authorized iteration.

## Recorded execution adjustments

Preserve three undersized originals and three source-mismatched originals as generated. Exclude source mismatches from source-aligned baseline analysis, use corrected briefs for revisions, and retain assignment-level reports. Accept complete revisions at 400–750 words to avoid filler. All 100 originals receive revisions; another eleven targeted changes form the final state. Four extra prompt probes check whether the updated instructions help before lint feedback. Keep the correct surname in article 099 despite the existing generic word-ban finding. These adjustments and residual distribution differences are documented in the final report.
