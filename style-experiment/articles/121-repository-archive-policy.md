# Deciding Which Experimental Repositories to Archive

I wrote this synthetic style exercise as an analysis piece. The projects, dates and numbers are fictional. In June 2026 I counted the repositories under `~/git` and found 47 of them, and 19 had seen no commit since 2024.

Three of the dormant projects still ran nightly cron jobs. One of them, `scraper-grid`, a fleet of scraper workers I built in 2023, kept an idle Postgres instance at $9 per month. I had paid that bill for five months without noticing.

My first move that month was blunt. On 12 June I deleted 6 dormant folders outright and lost a set of migration scripts I needed two weeks later. The rule I took from it: an archive step comes before any delete.

In this post, I'll cover:

- what the June audit counted
- why I archive instead of deleting
- the three questions I ask before a move
- what changed in my maintenance load
- where the archive stands today

## 1. What The June Audit Counted

I grouped the 47 repositories into three buckets. The 19 dormant ones had no commit in 18 months. The 11 slow ones got 2 to 3 commits a year. The other 17 were active. The audit was a 20-line shell script that printed the last commit date per folder, and the whole scan took 4 seconds.

Dormant code was cheap on disk, and it still cost me money and attention in three places:

- `scraper-grid` kept an idle Postgres instance at $9 per month
- 6 repos ran GitHub Actions on monthly schedules, about 200 of my 2,000 free CI minutes
- dependabot kept filing alerts for 31 dependencies I had no plans to upgrade

The dollar amount was small, about $27 a month across all three. The attention cost was larger, because those alerts made every dependency sweep look worse than it was. These numbers come from one person's accounts, so treat them as a sample of one. A team with shared runners would count the same costs in dollars instead of minutes.

## 2. Why I Archive Instead Of Delete

GitHub's archive mode made the choice easy. An archived repo turns read-only, keeps its issues and history, and costs nothing.

Deletion throws that history away, and history is where the lessons live. My `scraper-grid` README from 2023 documented a retry queue design that I reused in a 2026 project. Deleting the repo would have deleted the note too.

Locally, archiving means a folder move plus one tar file. I moved 19 folders into `~/git-archive` and added a dated tar of the whole folder to my external drive. The GitHub repos went into archive mode the same afternoon. The whole move took about 90 minutes, including writing the first archive notes.

Archive mode has one drawback: the repo vanishes from search and from my IDE's repo list, so I keep an index file at `~/git-archive/INDEX.md`. The index holds one line per project with its status and its archive date.

## 3. Three Questions Per Repository

Now every dormant candidate answers three questions before the move:

- does any running job still depend on the code
- would resuming cost less than rewriting
- did the project leave a lesson I still cite

The first question checks cron tables, GitHub Actions schedules and webhooks. The second gets a hedged estimate in days, and I write the guess down. The third question keeps the archive honest, so the README gains a short archive note.

The note template fits in six lines:

```text
archive-note: 2026-07-02
status: dormant, archived
running jobs: none since 2026-06-28
resume cost: about 3 days, mostly dependency upgrades
lesson: the retry queue design reappeared in task-queue v2
delete after: 2027-07-01 if nobody asks
```

The delete-after line matters as much as the lesson line. It gives every archived repo a date when the default answer becomes deletion, and so far no date has arrived.

## 4. My Maintenance Load After The Move

The moves happened over two weekends in July 2026, about 6 hours in total. Nightly cron jobs dropped from 7 to 3. GitHub Actions schedules dropped from about 1,900 minutes a month to 400. The free tier absorbed both numbers, so the honest saving is zero dollars and a quieter dashboard.

Dependabot alerts fell from 31 to 8, and the cloud bill fell from $63 to $51 a month. Most of that drop was the idle Postgres instance.

I did archive one repo too eagerly. `ml-monitor`, an experiment from January 2026, came back after 5 weeks when a client asked for its alert diff. Unarchiving took most of an afternoon because dependency upgrades had piled up. The rule I took from it: repos younger than 6 months wait in a review folder for one quarter before they move.

## State Of The Archive Today

As of September 2026, the archive holds 21 repositories and 26 remain active. I use the archive notes most, because 4 posts this year started as archived experiments I reopened for their notes.

What still doesn't work is the resume-cost estimate. Six of the 21 notes are still a single line, and my day-level estimates are guesses. When I unarchive something, I compare the guess with reality and correct the note. Whether the delete-after dates ever arrive is still open, and I'll report when one does.

I'll write about the archive note format in a future post. If you want to follow along, don't forget to subscribe.
