# Collecting Retrieval Failure Cases as a Team Habit

I wrote this synthetic style exercise as a how-to guide, and all team details are fictional. In January 2026 I watched a support engineer paste the same Postgres question into our Slack bot three times without getting a useful answer. Our demo scores looked strong at 91% recall, yet the bot missed 14 real questions that week.

I had treated retrieval misses as one-off complaints for months. I fixed the prompt, added a document, and moved on without recording what failed. The same miss returned two weeks later with different wording, and I had no record of the fix.

In this post, I'll share:

- how we log a retrieval miss in 60 seconds
- how we label the cause without long meetings
- how we add the miss to a shared test set
- how we review new misses every Friday
- what changed after eight weeks of logging

## Logging A Miss In 60 Seconds

A miss starts with the exact query text and the date. I copy the user question, the top three results, and the correct document link into a form. The form takes about one minute when the links are still open.

Our form lives in a GitHub issue template with four fields. I fill in the query, the returned document titles, the expected document title, and the Slack thread link. I leave longer analysis for later and focus on capturing the facts.

The template looks like this in the repo:

```text
query:
returned:
expected:
thread:
cause: unassigned
```

I file the issue before I investigate the cause. That order matters because details fade fast once I start testing fixes. Last month I filed 22 misses, and 19 of them had complete query text because I logged them the same day.

My mistake was waiting until Friday to log the whole week in one batch. The rule I took from it: a miss log needs facts first and analysis later.

## Labeling The Cause Quickly

We use four cause labels and nothing else. I pick chunking, ranking, coverage, or wording after a five-minute look at the miss. The narrow list keeps labeling fast and stops debates about edge cases.

The labels mean concrete things in our reviews:

- chunking means the answer sat inside a chunk that hid the key sentence
- ranking means the right chunk showed up after position five
- coverage means no document contained the answer
- wording means the query used terms missing from the document

I label the issue with one command after triage:

```bash
gh issue edit 214 --add-label "retrieval:ranking"
```

The command adds the label and moves the issue into the Friday review board. Labeling 22 issues took me 95 minutes in February, including time to open each document and confirm the right answer.

Chunking caused nine misses, ranking caused seven, coverage caused four, and wording caused two. Those counts told us where to spend the next two weeks. I had guessed ranking was the main cause before I saw the numbers.

## Adding The Miss To A Test Set

Every labeled miss becomes one row in a JSONL test file. I store the query, the expected document ID, and the cause label. The file lives at `evals/retrieval-cases.jsonl` and grows by three to five rows per week.

I append new rows with a script that reads the closed issues:

```bash
uv run python scripts/sync_misses.py --since 2026-02-01
```

The script reads issues with a cause label and writes new test rows with query text and expected IDs. It skips issues without an expected document and reports the count it added.

Each row includes enough context for a rerun six months later. I include the query, the expected document, the date, and the reporter name. I don't include scores or model names because those change with every release.

The test set grew from 41 rows in January to 96 rows in March. That growth gave us a stable way to compare chunking changes. A larger chunk size moved recall from 79% to 86% on the miss set while holding steady on the original demo set.

## Friday Review Without Long Meetings

We review new misses for 25 minutes every Friday at 14:00. I bring the five newest issues, the recall numbers, and one proposed fix. The team picks the fix with the strongest evidence and leaves the rest for next week.

The review fits on one slide. I show the miss counts by cause, I show one example query with its returned results, and I propose a change with a rollback plan. The format keeps the focus on decisions rather than discussion.

One Friday review changed our chunk overlap from 80 to 160 characters. The miss set showed six chunking failures where the key sentence sat at a chunk boundary. After the change, four of those six queries returned the right document in the top three.

Another review added eight runbook pages about backup restores. Coverage misses dropped from four per week to one per week after we wrote those pages. I spent six hours writing those pages, and I removed a whole class of misses with that work.

I keep the meeting short by refusing to redesign the pipeline during review. We approve one change, assign one owner, and measure the result before the next Friday. That limit stopped the meeting from drifting into search theory.

## Results After Eight Weeks

The habit changed how the team talks about search quality. We stopped saying the bot feels worse and started citing the miss counts by cause. The Friday board shows 96 logged misses with labels, fixes, and rerun scores.

Recall on the miss set rose from 61% to 84% between January and March. Recall on the original demo set stayed near 90% through the same period. The two numbers together show that fixes for real misses didn't break the cases that already worked.

The cost stayed low enough to keep the habit. Logging takes about one minute per miss, labeling takes about four minutes, and the Friday review takes 25 minutes. I spend roughly 90 minutes per week on the whole flow for a team of six engineers.

The log still misses silent failures where users never report a bad answer. I sample 20 random production queries each month and grade them myself to catch those cases. That sample found five additional misses in March that never became issues.

I'll write about our rerun setup in a future post. If you want to follow along, don't forget to subscribe.
