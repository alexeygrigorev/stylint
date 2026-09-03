# Ranking My Own Search Results by Recency and Usefulness

I wrote this synthetic style exercise as a build log, and all project details are fictional. My notes folder passed 3,200 markdown files in February 2026, and my search script kept returning stale results. It put the note I needed about Postgres backup rules in 34th place, behind scratch files from 2021.

Text match was the whole score in the first version of note-find, a tiny script that searches that folder. A note I edited that morning ranked the same as an abandoned draft from 2021 with similar wording. I worked around it by retyping queries until the right note appeared, and that habit cost me about 15 minutes a week.

In this post, I'll share:

- why pure text match ranked stale notes first
- the score I settled on and its three weights
- how the script shows a reason for every result
- the two false alarms I hit in April 2026
- where the ranking still misfires

## Text Match Alone

The first version of note-find counted query words inside each note and sorted by that count. A note mentioning Postgres five times beat a note mentioning it twice, and nothing else counted. That kept the code short and the results stubborn.

My backup checklist from January 2026 sat in 34th place under a scratch file of Postgres links from 2021. The scratch file mentioned backups four times inside a link dump, so it outscored the checklist. I retyped the query with extra words until the checklist appeared, then forgot the whole episode by Friday.

The mistake was treating ranking as a word-counting job. The rule I took from it: a result I never open is a wrong result, whatever the counts say.

## The Score And Its Weights

I rewrote the scoring on the weekend of 14 March 2026, and the script now computes three features per note:

```python
score = 0.6 * text_match + 0.3 * recency + 0.1 * opens
recency = max(0.0, 1.0 - days_since_edit / 180)
opens = min(opens_90d, 10) / 10
```

Text match still gets the largest weight, because a ranking that ignores the query would just sort by date. Recency fades over 180 days, so a note edited last week scores high and a note from 2024 needs stronger wording. The open count comes from a small click log that note-find appends to whenever I open a result.

The first weights were 0.6 for text, 0.2 for recency, and 0.2 for opens. Across 20 saved queries, raising recency to 0.3 fixed 6 searches and broke none. The current weights are 0.6, 0.3, and 0.1. I tuned them by hand instead of building a benchmark, and I expect to keep adjusting them.

## A Reason Next To Every Result

A score with hidden arithmetic kept me guessing, so the script prints one line per result:

```text
0.84  backup-checklist.md     match 0.61  recency 0.96  opens 0.90
0.55  postgres-links-2021.md  match 0.58  recency 0.00  opens 0.10
```

The first line explains the win. The checklist matches the query, I edited it two days ago, and I had opened it nine times in 90 days. The second line explains the loss. The 2021 file scores zero on recency because nothing touched it for 480 days.

When a result surprises me now, I read the line instead of blaming the weights. A bad ranking arrives with numbers attached, and I can tell which weight misbehaved. Before March I just retyped queries and hoped.

## Two False Alarms

The recency term caused the first alarm. In April 2026 I looked for a migration plan I wrote in October 2025, and fresh notes from a conference talk outranked it. The talk matched two query words and picked up the full recency bonus, while the plan had decayed to 0.15.

I tagged about 40 notes as reference in their frontmatter, and the script adds 0.1 before sorting. The migration plan returned to first place, and the talk notes dropped to fourth. I made the tag decision once, and the breakdown line shows the bonus.

The second alarm was my own testing. I opened the same note 12 times in a row while checking the click log, and that note topped every query for a week. Clicks count as evidence only when they come from real work, so the script ignores a click within 5 seconds of the previous one.

The rule I took from the pair: a usage feature measures behavior, and debugging is also behavior.

## Known Limits

Notes that matter but never get opened still sink. An emergency-contacts note from 2023 ranks low because nobody clicks it, and I only find it when I remember its filename. A keep flag for notes I always want visible would fix this, and I haven't built it.

My judging is also informal. I replay maybe 10 saved queries a month and read the results by hand. That means a weight change can quietly break a query I forgot about, and an offline test set would catch it.

## Two Months Later

The ranking holds up on the queries I actually run. Text match says what a note contains, and recency and open counts say what I rely on. The surprise was the reasons column, because visible arithmetic changed how much I trust the tool more than the weight tuning did.

The keep flag and the offline test set remain the two gaps, and both are small enough for one evening. I'll write about the offline test set in a future post. If you want to follow along, don't forget to subscribe.
