# Choosing an Article Title with a Simple Decision Record

I wrote this synthetic style exercise as a build log, and all project details are fictional. In February 2026 I finished a 1,600-word draft about backing up a small Postgres server, and I spent two hours picking the title. Twelve candidates went into a notes file, and the one that sounded cleverest won.

That post opened about 30 percent below my average for the month. Two readers said they skipped it because the title sounded like a rant. My mistake was rewarding wordplay instead of information. The rule I took from it: a title either states the promise or hides it.

In this post, I'll share:

- why clever titles kept winning my drafts
- the decision record I now keep per draft
- how I score four candidates against the text
- the search intent check with real queries
- eight posts later, where the record helps and stalls

## Titles That Drifted

For two years I picked titles in the last ten minutes before publishing. The shortlist lived in my head, and the winner was usually the candidate with a joke in it. In January a post about log rotation opened 40 percent below my average, and the comments asked about a shortcut the draft never mentioned.

Renaming after publish never worked either. I tried it twice in 2025, and both renamed posts kept their old traffic for weeks because existing links used the old wording. The February Postgres draft deserved a better process, so I built one around a plain text file. The file forces every title through candidates, checks, and a written decision with reasons.

## The Decision Record

Every draft folder now gets a file called `title-decision.md`. The record has six fields, and filling it takes about 15 minutes per post.

One filled record from February shows the whole file:

```text
date: 2026-02-14
draft: postgres-backup-rotate.md
promise: one command, verified restore, under ten minutes
candidates: four lines, one per title
search queries: three taken from my site analytics
decision: Postgres Backups With a Verified Restore
rejected: two vague, one off-promise, one too long
```

The rejected line matters most, because it stops me from recycling a losing candidate three drafts later. The record stays next to the draft, so the reasoning survives even after the post goes out.

Filling the record before asking for candidates changed the order of work. I now write the promise field first, in one sentence, and the draft gets checked against it before any title exists. Two drafts since February died at this stage because the promise described a post I hadn't written.

## Scoring Four Candidates

I ask Claude Code, a coding assistant, for four candidate titles per draft. The prompt names the promise from the record and bans puns outright. It also asks for one boring title and one search-style title in every batch. A run then produces a spread instead of four variations of the same joke.

Each candidate then goes through the same three checks:

- clarity: a stranger can state the topic after one reading
- promise: the title names something the reader can do afterwards
- fit: the promise appears in the draft's first 300 words

A candidate needs all three checks to survive the cut. In the February run, two of four died on fit because the draft buried the restore step in section five. I moved that section up, and the surviving titles got honest again. The boring title won four of the eight times, which older me would have found disappointing.

## The Search Intent Check

My site analytics list the top 20 search queries per month, and I read the ones that touch the draft topic. In February the list had 'postgres backup cron' and 'verify postgres restore', so the winning title took its phrase from the second query. That alignment costs nothing and takes about ten minutes.

For the log rotation post I skipped this check, and the title never matched anything people actually typed. I can still fix a mismatch before publishing, which makes this the cheapest check I own. Query data comes from my own analytics dashboard, refreshed once a month, so a brand-new topic starts with zero useful rows.

Titles also need to survive truncation, so the record logs a character count:

```bash
printf '%s' "Postgres Backups With a Verified Restore" | wc -c
```

The command prints 40, comfortably under the 60 characters where search results start cutting titles off. A candidate that needs 70 characters gets shortened before it can win, not after.

## Eight Posts Later

Since February I've written eight posts with a decision record, and title time fell from two hours to about 20 to 30 minutes. Four of the eight titles came straight from search queries, and none of the posts has needed a renaming after publish. The arc from that February evening is simple: the title choice moved from taste into a file, and the file made the choice boring.

The record still can't measure opens before publishing, so a title that passes every check can underperform anyway. Search queries also describe past readers, and a genuinely new topic has no queries yet. For those posts the record keeps the process honest, and the market check happens after release. I accept that lag as the price of publishing on a small site without paid traffic data.

I'll write about drafting opening paragraphs in a future post. If you want to follow along, don't forget to subscribe.
