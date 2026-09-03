# Comparing 250 Generated Articles to a Real Archive

I wrote this synthetic style exercise as a build log, and all corpus numbers are invented but internally consistent. In June 2026 I finished comparing 250 generated article drafts against an archive of 50 newsletter posts by a single author. The comparison took about nine hours across two weeks.

The drafts came out of a generation experiment that ran from March to May. Twelve parallel coding-agent workers each wrote drafts from a shared style brief, and a linter gated every file. My job was to find out which habits of the real author the machine drafts actually kept.

In this post, I'll share:

- the brief that all 250 drafts started from
- how twelve workers produced the corpus
- what the lint gate caught on the first pass
- a reading pass of 40 drafts against 50 posts
- the writing moves that transferred cleanly
- what I would change about the experiment

## Two Corpora And A Shared Brief

The synthetic corpus held 250 drafts, one per topic row in a planning sheet. The comparison corpus was a public newsletter archive of 50 posts by one author, published between December 2025 and August 2026. Both sets were plain markdown, which made the comparison mostly a reading job.

The brief was a 1,400-word style document. It covered voice rules, banned words, opener forms, and a closing template. Every worker read the same brief before writing a word. I expected the brief to matter more than the model, and the reading pass mostly confirmed that guess.

## Twelve Workers And 250 Topics

The 250 topics were split into batches of about 20, and each worker session owned one batch from outline to final file. Workers ran overnight on ordinary hardware, and a full batch took between 40 and 90 minutes depending on article length.

Coordination stayed boring on purpose. A topic sheet assigned ids and titles, and workers never touched another batch. The only shared rule was that every file must pass the linter before it counted as done. Two batches were regenerated from scratch in April after a brief revision, which cost one evening.

## Linting 250 Drafts

The linter knows about 61 checks, from sentence length caps to banned phrases. On the first pass, only 95 of 250 drafts came back clean. That 38 percent pass rate surprises nobody who has read raw model output.

The finding counts were lopsided:

- long sentences over 25 words: 412 findings
- label-colon paragraph openers: 190
- lists without a lead-in sentence: 133
- banned words, led by `very` and `itself`: 88
- em dashes: 41

After one fix round per draft, the pass rate hit 100 percent. The linter caught mechanics, and it caught none of the deeper habits, which is exactly why the corpus needed a reading pass too.

## Reading 40 Drafts Against 50 Posts

Word-frequency tools came first, and they failed fast. Knowing that the word "data" appears 610 times across the corpus says nothing about whether a draft sounds like the author.

My mistake was starting with counts because they were cheap. The rule I took from it: compare writing moves, and read the words yourself.

The real review covered 40 drafts, about 16 percent of the corpus, each scored against a checklist of ten signature moves from the archive. The checklist came straight out of the style reference, one point per move, with a quoted line as evidence. One reading session covered five drafts and took about 40 minutes with the archive open beside it.

The results mixed the expected with the surprising:

- 40 of 40 drafts had the bulleted roadmap
- 36 of 40 opened on a concrete number or a named tool
- 31 of 40 paired a flat failure admission with a one-line rule
- 22 of 40 hedged estimates the way the archive does
- 3 of 40 linked back to an earlier post, a running habit in the archive

## The Moves That Transferred

Three moves transferred almost without effort. The roadmap list after the opener, the flat failure admission followed by an extracted rule, and the number-first opening appeared in most drafts. None of the three needed prompting beyond the brief. These three are also the most mechanical of the ten moves, which fits the linting result.

Restraint transferred much less reliably. Drafts averaged about 1,050 words against an archive median near 1,500 for essays. The compression made many drafts read like notes for a post instead of the post. Two habits barely appeared at all. References to earlier projects turned up in 3 of 40 drafts, and personal-life details turned up in 2.

## Lessons From The Comparison

Nine hours of reading settled a question I had only held opinions about. The mechanical layer of a writing style is easy to enforce with a linter. The judgment layer, knowing when a draft is finished and when it's hiding something, is where the machine drafts fell short.

If I reran the reading pass, I would sample 80 drafts instead of 40. Forty gave me trends, and double that would give me confidence about the middle of the ranking. The corpus now doubles as a test set for brief edits, and every change to the brief runs against 20 fresh drafts before it ships.

I'll write about how the brief evolved during the run in a future post. If you want to follow along, don't forget to subscribe.
