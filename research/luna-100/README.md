# 100 Luna articles and author-style calibration

This experiment extends the [initial archive analysis](../alexey-voice/README.md).
It adds two default stylint checks and revises the drafting prompts using
100 new Luna articles based on Alexey's published Substack archive.

The original drafts and editing rounds remain available for comparison.
This work updates prompts and deterministic checks. It doesn't train model
weights or establish an author-approved voice score.

## Material and method

The archive contains 54 posts. Fifty substantive bodies were selected and
copied into [sources/raw](sources/raw), removing images and common newsletter
backmatter where possible. The original archive stays unchanged. The
[manifest](output/manifest.json) records original and reference hashes.

Luna generated two articles per source: a personal account and a teaching
explanation. The target was 450–750 whitespace-separated words. The 100 accepted
originals are in [round-1](output/round-1), with 100 separate
[fact briefs](output/briefs). Three originals are slightly short at 443,
443 and 448 words. Originals remain unchanged, including those defects.

All accepted drafts used `gpt-5.6-luna`, with high reasoning for IDs 001–034
and low reasoning for 035–100. These runs aren't a controlled model comparison.

The two treatments of each source are related observations, not independent
samples. The published material varies in length and reflects contributions
from the author alongside AI tools and editors. We're approximating the
published voice Alexey selected.

Eighty articles from 40 sources formed the development set. Twenty articles
from 10 other sources were reserved until the rule definitions were frozen.
An early content audit read 069, so its source was moved out of the reserved
set and replaced with previously unread source s17 before evaluation.
The [freeze record](output/reports/rule-freeze.json) preserves this correction
and hashes of the checker code.

A later audit found three source assignment errors. Article 037 used facts
from the earlier Telegram assistant post. Article 048 described website
construction instead of the community launch, and 050 described the FAQ
workflow instead of website construction.

The [corrected briefs](output/briefs-corrected) use the assigned sources,
while the original briefs and drafts remain unchanged. Article 048 was corrected in round 2, and 037 and 050 in round 3.

Those three originals are excluded from the
[source-matched calibration](output/reports/source-aligned-calibration.json).
The remaining development set has 78 articles, and the reserved set has 19.
The reserved mistake used material from a development source. The original
assignment-level reports remain available, but shouldn't be treated as
100 correctly sourced observations.

An initial bulk attempt copied and mechanically rewrapped source text.
Those files were rejected and quarantined in [rejected-bulk](output/rejected-bulk).
They're excluded from every result. Luna generated the accepted articles in
smaller batches. We checked those drafts for source copying and repeated text.

## Rules supported by the experiment

The [calibration report](output/reports/rule-calibration.json) contains every
match, its source group and word-normalized rates.

| Check | Development articles | Reserved articles | Reference articles |
| --- | ---: | ---: | ---: |
| `dense-paragraph-run` | 62/78 | 17/19 | 0/50 |
| `evaluative-framing` | 6/78 | 0/19 | 0/50 |

This table excludes the three source assignment errors. Including them gives
64/80 and 18/20 density matches, with the same six evaluative matches.

`dense-paragraph-run` reports a continuous run of at least four paragraphs,
each containing at least three sentences and 50 words. It reports once per
run. Headings, lists, quotes and other structural blocks end a run. An isolated
long paragraph doesn't trigger this check. The corrective prompt asks the
writer to separate a need, action, observation or decision where the subject
changes, without arbitrary paragraph slicing or decorative headings.

`evaluative-framing` reports narrow sentence openings such as "The useful
part is", "The important part was" and "That was the point". It asks the
writer to state the actual observation or delete a redundant recap. Exact
double-quoted text and inline code are excluded. The check preserves
technical comparisons such as "The main difference is" and source-supported
forms such as "The valuable part is" or "That was enough".

The reserved set confirms the density difference in this generation setup.
It contains no positive evaluative-framing cases, so it doesn't provide
positive confirmation for that lower-frequency rule. Neither check identifies
authorship or establishes that a sentence is universally bad writing.

Broad bans on comparisons or vague demonstratives were rejected. The
references themselves contain comparisons in 30 of 40 development sources and
demonstrative constructions in 22. At the final development size, no n-gram
passed the exploratory enrichment filter. Recurrence alone is insufficient
evidence for a new banned phrase.

## First-draft measurements

The full default checker reported 1,449 findings across 100 articles. The two
new rules contributed 88 findings. Existing checks contributed 1,361, including
contractions, comma-heavy sentences and choppy sequences. All 100 articles
had at least one finding.

These counts use the corrected sentence boundary
for the existing repeated-and check. The former checker reported 1,450. Its reports remain available alongside the corrected measurements.

In the development set, the median per-document sentence length was 14 words
for both references and drafts. The median paragraph contained one sentence
in references and four in drafts. Short-sentence incidence was also fairly
similar: 25.7% in references and 22.7% in drafts. Paragraph grouping showed
a larger difference than sentence length. Some reference captions remain,
so these paragraph medians are approximate.

Account drafts retained more first-person language than explanation drafts.
Combining those modes obscures the distinction, so the JSON reports include
separate measurements. These features are diagnostic and have no combined
voice score.

There were three exact source sentence overlaps of at least 12 words and no
sentence of that length shared by three generated articles. Overlaps require
review because legitimate quotations can match. These checks don't establish
independence or rule out paraphrase copying by themselves.

## Revision approach

The [revision instructions](output/prompts/revision-instructions.md) require
the actual source, fact brief, original draft and updated voice profile.
The source outranks both the brief and plausible details in the draft.
Each revision is checked for facts, edited for voice, run through the full
checker and checked against the source again.

Revisions may contain 400–750 words when cutting repetition leaves a complete
article. This adjustment prevents the original minimum from encouraging
filler. Author motives and uncertainty take precedence over a numerical
length target.

The first editing audit caught invented laptop requirements and a missing
deployment process in 005. The correction restores development-environment
testing and production deployment while removing claims about typing and
screen size. The paired 006 explanation deletes its closing phone/laptop
recap because the preceding paragraphs already explain that distinction.

Agent review sidecars record edits and fact checks. They're evidence of
the editing process, not human approval or an independent factual guarantee.

The later pass also corrected invented causal links in 069. The draft made
warm-up support depend on bodyweight exercise tracking, although the source
listed them as separate requirements. It also made CodeHive's size cause
the adoption of Termius. The revision keeps the two reasons for abandoning
the interface separate. Article 070 now uses the author's supported first
person instead of calling him "the author".

Reviewers produced useful suggestions and false findings. For example, a
reviewer claimed 014 said "first two weeks" although the draft already said
"final two weeks". Another review missed the significance of "probably" in
a quoted comparison. Those comments were checked against the files.

The
[audit reviews](output/audit-reviews) preserve this imperfect feedback. They
cover selected claims and should be read as sampled checks.

A final [Luna high review](output/final-audit-high) examined four revisions
written by the parent, checking eight quoted claims in each. We verified all
32 source and draft quotations against their recorded file hashes. Those
reviews requested no further corrections.

## Fresh prompt check

After updating the prompts, Luna wrote four additional first drafts from two
sources without lint feedback. These are separate from the requested 100.
The existing agent retained task context, so this was a practical check
rather than a blind model benchmark.

The [raw probe report](output/reports/prompt-probe-raw.json) records 29 findings,
compared with 70 across the four original drafts from those sources. None of
the probe drafts triggered the two new checks. Existing issues remained,
including expanded contractions, comma-heavy sentences and flat definitions.
Prompt instructions reduced some problems but still required an editing pass.

All four [revised probe articles](output/prompt-probe/revised) pass the full
checker after source review and contextual edits. Their originals remain
unchanged in [prompt-probe/raw](output/prompt-probe/raw).

## Completed rounds

All 100 drafts changed in [round 2](output/round-2). Luna revised 73 of them,
and the parent revised 27. The [final round](output/round-3) contains another
11 targeted edits, with the other 89 files retained byte-for-byte from
round 2. These are three saved corpus states, rather than a claim that all
articles were rewritten three times.

The [comparison report](output/reports/round-comparison.json) records the
results using the full default checker, without ignored tags:

| Measurement | Original 100 | Round 2 | Final 100 |
| --- | ---: | ---: | ---: |
| Total findings | 1,449 | 1 | 1 |
| Articles with no findings | 0 | 99 | 99 |
| Dense paragraph runs | 82 | 0 | 0 |
| Evaluative lead-ins | 6 | 0 | 0 |
| Exact source sentence overlaps of at least 12 words | 3 | 2 | 0 |

The existing generic ban on `foster` flags participant Miki Foster's surname
in [099](output/round-3/099-account.md). We preserved the correct attribution
and recorded the finding as a source conflict without suppressing the tag.

The final median paragraph has three sentences, down from four, compared
with one in the reference bodies. Median sentence length changed from
14 to 13 words, compared with 14 in the references. Contractions rose from
zero to 5.2 per 1,000 words, closer to the reference median of 6.2.

First-person language needs separate treatment by form. Account drafts rose
from 26.8 to 35.9 instances per 1,000 words, while explanations rose from zero
to 6.6. Combining the forms gives 17.3, compared with 22.7 in the references.
Accounts may now overuse first person, and explanations remain less personal.
No further phrase ban follows from these aggregate numbers.

Paragraphs remain denser and long sentences occur less often than in the
references. The prompts preserve supported motivations and remove
repeated verdicts, but the existing checker favors shorter clauses. These
remaining differences matter when judging voice beyond a lint count.

The final phrase scan found ordinary technical language and phrases such as
"I keep the". Those are poor candidates for additional bans. The source
alignment diagnostic has no remaining large lexical mismatch, but it can't
prove factual correctness. The stopping decision rests on completed revisions,
resolved concrete review findings and the absence of another well-supported
construction to ban. It doesn't imply human preference approval.

Validation includes 419 passing tests and a wheel check against all 35
packaged Python and Markdown files. The original 54-post archive and all
100 accepted first drafts retain their recorded hashes. The
[verification record](output/reports/verification.json) links the checks and
records the single retained surname finding.

## Reproduce the analysis

Run the checked-in tool from the repository root:

```bash
uv run python tools/voice_mine.py \
  --manifest research/luna-100/output/manifest.json \
  --round round-1 --split development \
  --output /tmp/luna-development.json

uv run python tools/voice_mine.py \
  --manifest research/luna-100/output/manifest.json \
  --round round-1 --split holdout \
  --output /tmp/luna-holdout.json

uv run stylint --explain dense-paragraph-run
uv run stylint --explain evaluative-framing

uv run python research/luna-100/output/scripts/source_alignment.py round-1
uv run python research/luna-100/output/scripts/source_alignment.py round-3
uv run python research/luna-100/output/scripts/final_reports.py
```

The [development](output/reports/round-1-development.json) and
[reserved](output/reports/round-1-holdout.json) reports preserve the original
measurements for comparison with later rounds using the same source groups.

## Limits

These are shorter reconstructions of historical articles, not new reports
of current product behavior. No external fact updates were introduced.
Revising the same corpus repeatedly can lead to overfitting. Grouping by source helps
with rule selection but doesn't make subsequent edited drafts a fresh test.

The two checks are calibrated for this published style and generation setup.
Other writers may prefer denser paragraphs or evaluative lead-ins.
The final voice assessment still needs Alexey's preference labels before
any example can be described as approved.
