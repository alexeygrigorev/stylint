# A Lab for Comparing Writing Styles on the Same Project Idea

I wrote this synthetic style exercise as a build log, and all project details are fictional. In April 2026 I gave six coding-agent sessions the same 240-word brief. Each session had to write a build log about csv-dedup, a tool that removes duplicate rows from a CSV file.

The six drafts describe the same tool and read like six different writers. My own drafts kept a fixed skeleton, from the concrete opener to the bulleted roadmap and the close with a subscribe line. I wanted to know which parts of that skeleton survive different instructions. So I turned the question into a small lab with one brief, six variants and a scoring rubric.

In this post, I'll share:

- how the lab fixes the project and the brief
- what the fixed brief sets in stone
- how the six variants differ
- which eight checks make up the rubric
- what the first round of scores showed
- where the lab goes next

## One Brief, Six Drafts

My drafts tend to converge on one structure, and I couldn't tell which parts of that structure hold the quality. Reading six descriptions of the same tool removes that doubt. Each pair of drafts differs only in the instructions, so any scoring difference points back to a writing habit.

The lab lives in a folder called `style-lab` with three subfolders for the brief, the drafts and the scores. Each draft is a markdown file from one Claude Code session, and the sessions never saw each other's output. I ran all six sessions on 6 and 7 April 2026.

## The Fixed Brief

The brief fixes the facts that every draft must keep:

```text
Write a build log about csv-dedup, a CLI tool that
removes duplicate rows from a CSV file.

Fixed facts: released in March 2026; 420 lines of Python;
deduplicates a 30 MB file in 4 seconds; 96% exact-match rate.
Invent no further numbers. Keep the tool name exactly.
```

Everything else stays open: the failure story, the section order and the placement of the numbers.

The brief is 96 words and took the longest to write, because every vague line produced a different invention in some draft. My first version said only that the tool was fast, and one session turned that into a fake benchmark table within seconds.

## Six Variants From Six Sessions

The six variants differ in one constraint each:

- A: no instructions beyond the brief
- B: a forced bulleted roadmap after the opener
- C: numbered step headings in the archive style
- D: one required failure story with an extracted rule
- E: a strict cap of 25 words per sentence
- F: all four constraints combined

Each session produced 900 to 1,100 words in about 4 minutes. Two drafts needed a rerun: one ignored the fixed release month, and one wrote 1,600 words before I cut it back. The reruns counted as part of the same variant.

## An Eight-Check Rubric

The rubric has eight checks, one point each:

- the opener states a concrete situation with a number in the first two sentences
- a bulleted roadmap follows the opener
- each section anchors to a month and year
- estimates come with a hedge, such as "about 20 minutes"
- every failure gets a flat statement and a rule
- every result comes with a stated limitation
- the close looks forward and names what's missing
- no hype words appear anywhere

Scoring is manual, and I kept it that way on purpose. I read the draft once, then check the eight items with the file open beside the rubric. The checklist started with 12 items, and a pilot pass on two old drafts cut it to 8. One pass takes about 25 minutes per draft, so the full round cost roughly 2.5 hours.

## Findings From the First Round

The scores ranged from 3 to 8 out of 8. Variant F scored 8 and D scored 7. E scored 6, B and C scored 5 each, and the baseline A scored 3. The forced roadmap in B added 2 points over A on its own, which makes it the strongest single constraint in the round.

Three habits transferred into every draft, including the baseline. All six kept the tool name, all six put a number in the first paragraph, and five of six hedged at least one estimate. The failures clustered in the date anchoring: only D and F dated every section, and A invented no dates at all.

Two drafts added benchmark numbers despite the brief. I now end every brief with a line that says numbers may be reused, never added.

## The Lab's Next Steps

The lab answered its first question: the roadmap and the failure-plus-rule moves account for most of the score, and they survive any instruction set. What it can't measure is whether a draft is pleasant to read. F scored 8 while reading like a form filled in, and no check caught that.

Round two adds three drafts written by human friends with the same brief, plus a second rater for the scores. One rater, one rubric and six drafts make every finding provisional, and I treat the numbers that way.

I'll write about round two, with the human drafts in the mix, in a future post. If you want to follow along, don't forget to subscribe.
