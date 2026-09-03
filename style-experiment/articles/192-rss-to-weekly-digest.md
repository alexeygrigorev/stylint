# Turning an RSS Queue into a Weekly Digest

I wrote this synthetic style exercise as a build log, and all project details are fictional. In February 2026 my feed reader held 2,740 unread items across 87 subscriptions, and the oldest unread item was from August 2024. I had stopped opening the reader altogether, because the queue punished every visit.

The subscriptions were still good. The blogs I followed in 2023 still published about 12 posts per week in total, and I still wanted most of them. I faced one endless list with no filter, no grouping and no ending.

In this post, I'll share:

- why the read-later folder failed first
- how the daily filter picks about 40 items
- how the survivors get grouped into five topics
- how the summaries keep a number in the first line
- how the links stay close to the claims
- what eight issues changed

## The Queue That Only Grew

My first attempt was a read-later folder inside the same reader. I marked 30 or 40 items per week as saved-for-Sunday, and for three Sundays I actually read them. By the fourth Sunday the folder held 130 items, and I marked all of them read without opening one.

My mistake was building a second queue with the same structure as the first. The rule I took from it: a reading list needs an ending, and a folder that only grows never reaches one.

## Filtering The Feed

In March I wrote `digest_weekly.py` with `feedparser`, a small Python library for reading RSS and Atom. The script pulls every feed once per day and checks each item against the filter.

The filter keeps an item when it matches a tracked keyword or when a trusted author wrote it. I track 14 keywords and 9 author names, and everything else gets a one-line entry in a skipped log.

A full week across 87 feeds produces about 260 items, and the filter keeps 35 to 45 of them.

The keyword list includes Postgres, cron and pricing, which sounds random until you know that I choose tools for a small team. Rescues stayed rare: twice in eight weeks, and both times the feed had changed its focus.

The weekly run is one command on the home server:

```bash
uv run python digest_weekly.py --week 2026-W23
```

The run writes `digest/2026-W23.md` and takes about 40 seconds, most of it spent waiting on slow feeds.

## Grouping What Survived

The survivors go into one of five fixed groups that haven't changed since March. The names are databases, agents, pricing, writing and tools. A group assignment comes from the same keyword lists that filtered the item, so grouping costs no extra model calls. The five group names double as H2 lines in the digest file, so a reader can jump straight to a topic.

Items that match two groups go to the more specific one. About two items per week match nothing cleanly, and they go into a sixth overflow group that I sort manually before publishing.

## Summaries With A Number

Each kept item gets a two-sentence summary written by Claude with a fixed prompt. The prompt enforces the rule that changed everything: the first sentence must contain a number taken from the item. Numbers force each summary to include a fact I can check.

A summary without a number gets regenerated once. If it still fails, it goes into the digest with a guess flag beside it. About one item per issue ends up in that state.

The prompt starts with one fixed line:

```text
Summarize the item in two sentences.
The first sentence must contain a number from the item.
If the item has no number, write "no number given" and summarize the claim.
```

One summary costs about 40 tokens of output, so eight issues cost about $1.20 in API spend.

## Links You Can Check

Every summary line ends with the link, and I place it right after the claim it supports.

The digest format stayed deliberately plain:

```text
## Databases
- Postgres adaptive skips cut a reporting query from 9.4s to 1.1s (link)
- A cron migration retired 340 lines of glue on our home server (link)
```

The link sits one click from the claim, so a wrong summary gets caught by whoever cares enough to click. The digest has two readers, me and one colleague, and we clicked through 61 times across eight issues and reported two bad summaries. When a summary needs a correction, I fix the line and re-send the issue with a short note at the top.

## Results From Eight Issues

The first issue went out on 12 April, and the weekly run has continued through early June. The Monday reading pass now takes about 25 minutes, down from a two-hour scrolling session that rarely happened. The reader queue holds fewer than 15 unread items, because everything older than the newest digest gets archived. I also search the eight back issues when I need a link I half-remember.

The digest still flattens long essays. Posts over 6,000 words got trimmed to one number each, and two of those summaries reported a side detail instead of the main claim. The skipped log now keeps the full text of long items, and I read those on their own before they enter a digest.

I'll write about how the keyword list gets maintained in a future post. If you want to follow along, don't forget to subscribe.
