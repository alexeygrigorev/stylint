# Making AI drafts sound like Alexey

The most useful intervention was preserving the author's reasons for decisions before asking a model to write. The first Luna drafts were already reasonably direct when their briefs retained those reasons. More voice instructions alone produced small, inconsistent improvements. Stylint helped with contractions, repeated command sentences and paragraph structure, but did not detect missing meaning, unnecessary conclusions or instructions copied into prose.

This is an initial calibration with examples for Alexey to review. It does not train model weights or establish a human preference result.

## What was examined

The read-only scan covered all 54 Markdown posts in `../telegram-writing-assistant/reference/substack`, from December 4, 2025 through September 4, 2026. Close reading focused on selected sections of eight posts spanning personal projects, an incident, teaching and an announcement. Source pages and limitations are in [sources/index.yaml](sources/index.yaml).

The existing experiment describes 250 drafts, but this checkout contains 190 Markdown articles. The current checker reports 236 findings across 32 of them; 158 pass. Its README requires a common structure, a word-count range and a subscribe line, and permits invented project facts. Those drafts are synthetic stress-test material, not positive examples of the author's actual experience.

The published archive is the author-selected target. It is not a corpus of verified unaided human writing: the [phone article](../../../telegram-writing-assistant/reference/substack/2026-05-22-the-system-i-built-to-ship-code-from.md) describes dictation, AI drafting, author feedback and editing by Valeriia. Several archived posts credit her. Newsletter tool blurbs, quoted prompts and publication formatting also differ from the personal narrative.

## What makes the writing recognizable

The recurring connection is between a specific need and a decision:

- In [minsearch](../../../telegram-writing-assistant/reference/substack/2026-05-29-minsearch-the-small-search-library.md), teaching inside a notebook explains avoiding server setup. FAQ fields explain boosting and filtering. Repeated downloads explain packaging. Agent examples explain an appendable index.
- In the [phone account](../../../telegram-writing-assistant/reference/substack/2026-05-22-the-system-i-built-to-ship-code-from.md), school runs and gym breaks explain the need. Disconnects explain tmux, and long commands explain tmuxctl. A tool inventory alone would lose the story.
- In [SQLiteSearch](../../../telegram-writing-assistant/reference/substack/2026-02-20-how-i-built-sqlitesearch-a-lightweight.md), separating ingestion from the RAG agent explains persistence. Familiarity and the ability to debug explain choosing LSH. These are personal reasons, not claims that the architecture is universally best.
- In the [database incident](../../../telegram-writing-assistant/reference/substack/2026-03-06-how-i-dropped-our-production-database.md), the sequence of decisions and changing understanding matters. Removing uncertainty would misrepresent what the author knew at the time.

Ordinary language carries the account: I wanted, I tried, I asked, I use, at first, so, but. The author repeats technical names and qualifies recommendations. An attempt can fail or stop. A result can be sufficient for one person's use without becoming a general lesson.

The profile should preserve that material rather than impose one article shape:

- The [README article](../../../telegram-writing-assistant/reference/substack/2026-07-16-how-to-write-a-good-readme.md) opens with the reader's problem and uses questions as teaching structure.
- The [website experiment](../../../telegram-writing-assistant/reference/substack/2025-12-05-how-i-rebuilt-my-website-in-10-minutes.md) has a short chronological opening without a roadmap list.
- The database article uses a roadmap sentence. The minsearch article uses a roadmap list.
- The [abandoned-projects opening](../../../telegram-writing-assistant/reference/substack/2026-06-26-six-projects-that-didnt-make-it.md) repeats clauses beginning with Some. A claim that the author never repeats sentence templates is too strong.
- The [course launch](../../../telegram-writing-assistant/reference/substack/2026-08-31-ai-dev-tools-zoomcamp-2026-starts.md) starts with the course and date. It does not need to become a personal retrospective.

The archive contains formatting and phrases that the current checker discourages. These are reasons to distinguish historical observation from current drafting preferences, not to rewrite the author's archive or add more blanket bans.

## Descriptive measurements

Each value below is the unweighted median of a document-level measurement. Parsing omits headings, lists, code, quotes, images and standalone links. It retains captions and newsletter backmatter. These are whole newsletters versus synthetic articles, so genre and length are confounds. Counts are approximate, not targets for new prose.

| Measurement | Published archive, 54 posts | Old synthetic corpus, 190 drafts |
| --- | ---: | ---: |
| Median sentence length, words | 14 | 13 |
| 90th-percentile sentence length, words | 24 | 19 |
| Sentences longer than 25 words | 8.33% | 0% |
| Sentences shorter than 10 words | 26.18% | 25.94% |
| Median sentences per paragraph | 1 | 2.5 |
| First-person words per 1,000 words | 25.59 | 34.16 |

The old synthetic corpus approximates short-sentence frequency while compressing the longer end of the sentence distribution. The archive's paragraphs are also less uniform. Increasing first-person frequency would not by itself make a draft more faithful. Full methods, per-file measurements, hashes and lint findings are in [old-corpus.json](output/old-corpus.json).

## Luna experiment

All generations used `gpt-5.6-luna` with low reasoning and separate task contexts. The writing agents received only the specified briefs and prompts, not the original articles or one another's drafts. Their general system instructions still applied. Each first completed draft was retained. The parent reviewed the evidence and made the final corrections.

The pilot used the same two fact-preserving briefs in three conditions. They request 250–400 word excerpts and identify required facts. Keeping the briefs strong makes the baseline a useful control; it is not an intentionally bad AI draft.

| Condition | Minsearch findings | Phone findings | What happened |
| --- | ---: | ---: | --- |
| Neutral expansion | 2 | 9 | Most facts and reasons survived; phone has repeated command sentences and redundant closing claims. |
| Voice draft prompt v1, no lint | 2 | 8 | Phone is only 236 whitespace-separated words and repeats an editorial scope exclusion. Minsearch implies an unsupported sequence of early features. |
| Rewrite prompt v2, no lint | 2 | 8 | Some empty claims disappear, but ordinary contractions and the command list still need correction. The phone ending repeats the benefit of Makefiles. |
| Parent correction plus full stylint | 0 | 0 | Required facts checked, repeated conclusions cut, causal explanations restored, commands formatted as a list. |

Originals and corrections are preserved side by side:

| Topic | Baseline | Prompt-only draft | Prompt-only rewrite | Final correction |
| --- | --- | --- | --- | --- |
| Minsearch | [read](output/experiment/baseline/minsearch.md) | [read](output/experiment/guided/minsearch.md) | [read](output/experiment/rewritten/minsearch.md) | [read](output/experiment/corrected/minsearch.md) |
| Phone | [read](output/experiment/baseline/phone.md) | [read](output/experiment/guided/phone.md) | [read](output/experiment/rewritten/phone.md) | [read](output/experiment/corrected/phone.md) |

The third topic, SQLiteSearch, was reserved until after the draft prompt revision. Its first v2 draft had four findings and converted the instruction not to infer the fastest method into an unnecessary disclaimer. The same prompt with that instruction moved out of the fact list produced one finding and omitted the disclaimer. This follow-up used a fresh Luna context, but is one resample on the same topic, not an independent confirmation or a statistically controlled effect.

See the [first draft](output/experiment/holdout/sqlitesearch-raw.md), [separated-brief draft](output/experiment/holdout/sqlitesearch-clean-brief.md), and [final correction](output/experiment/corrected/sqlitesearch.md). The final version removes a repeated explanation, formats `plan.md`, and passes the full checker. All three final excerpts retain the required ledger facts and fit the requested length range by whitespace word count.

## Corrections worth retaining

The following judgments are the parent's proposed edits, not human-approved labels:

| Draft wording or behavior | Correction | Why |
| --- | --- | --- |
| “The course FAQ made the next requirements clear.” | Explain weighting question matches and filtering by course, then say the first version included both. | Names the actual requirements and avoids implying an unsupported development sequence. |
| “Those needs explain the field boosting and keyword filtering in minsearch.” | “So the first version already had field boosting and keyword filtering.” | Connects the stated need to a concrete implementation without an analytical summary label. |
| “The work remains accessible even when the phone connection does not.” | Delete after the paragraph already explains tmux and reconnection. | Rephrasing the same point adds no information. |
| Three sentences starting with “The command…” | Introduce a list containing the three exact commands and their behavior. | These are genuine parallel reference items. |
| “It does not cover deployment permissions, port forwarding or voice transcription.” | Delete from the article and keep the instruction in the brief. | Assignment scope is not publishable evidence. |
| “I wasn't claiming that LSH was the fastest or best method.” | Keep the supported reason for choosing LSH; omit the disclaimer. | The brief's prohibition became an unprompted claim about what the author was not claiming. |
| “This was how I handed the design over…” | Delete after the preceding sentences already describe saving the plan and asking Claude to implement it. | The meaning is already present; the checker also catches the metaphor. |

The resulting reusable change is a briefing prompt as well as drafting and rewriting prompts. Facts, decision reasons and editorial instructions belong in separate sections. Negative instructions embedded inside a fact are easy to copy into article prose.

## Using it

The new resources are bundled in the package:

```bash
uv run stylint --style-guide alexey
uv run stylint --prompt alexey-brief
uv run stylint --prompt alexey-draft
uv run stylint --prompt alexey-rewrite
```

Use the first prompt to prepare notes, the second with the resulting brief to draft, and the third with the brief and AI draft to revise. These commands print instructions; they do not call a model. Apply the existing judgment prompts and run full stylint on the resulting article. Check facts again after editing. Do not pad, invent details or remove a necessary qualification to clear a lint finding.

Generate a read-only comparison report:

```bash
uv run python tools/voice_compare.py \
  --reference ../telegram-writing-assistant/reference/substack \
  --candidate research/alexey-voice/output/experiment/corrected \
  --output /tmp/alexey-voice-comparison.json
```

Recheck the finished samples:

```bash
uv run stylint research/alexey-voice/output/experiment/corrected
```

## Evidence and limits

[manifest.json](output/experiment/manifest.json) records sources, file hashes, prompts, generations and lineage. [fidelity-review.json](output/experiment/fidelity-review.json) records the parent's fact checks and judgments. [human-review.json](output/experiment/human-review.json) leaves preferences and replacement wording blank for Alexey's review.

The guide's briefing prompt was distilled from the observed failure; the cleaned brief used in the follow-up was prepared by the parent, not generated by that new prompt. There is one generation per condition and topic, no blinded human ratings, and no claim that the final edits improve a model's underlying ability. The parent both designed the prompts and judged the drafts. The held-out topic was in the aggregate archive scan, although it was not used for close-reading guidance or examples before the draft-prompt revision. Future testing should use new author notes and preferred/rejected pairs.

The existing default lint rules are unchanged. No package release or publication was performed. The author archive was not edited. Test and verification details are recorded in [verification.json](output/verification.json).
