# Keeping an Observation Notebook for System Behavior

This synthetic style exercise follows a fictional practitioner with invented numbers and events. Nothing here describes a real project. In April I noticed my side project slowed down every evening around eight.

Response times climbed from 200 milliseconds to nearly two seconds. The slowdown vanished by morning with no deploy in between. I had no record of what else changed at that hour.

I first debugged from memory and gut feeling each night. I restarted the server, cleared a cache, and watched the metrics for ten minutes. The fix never stuck because I never wrote down what I tried.

Three evenings produced three different theories with no notes to compare. I blamed the database on Monday, the job queue on Tuesday, and the hosting plan on Wednesday. Each theory felt certain until the next one arrived.

In this post, I'll share:

- why nightly slowdowns beat my memory
- how I set up a daily observation notebook
- how each entry pairs a hypothesis with a chart
- how I review anomalies and record decisions
- what the notebook costs and where it still falls short

## Nightly Slowdowns Beat Memory

The project serves about 900 requests daily from a single 4 GB virtual machine. Postgres, Redis, and the FastAPI app share that box. Evenings bring a backup job plus a traffic bump from US visitors.

My memory of each incident blurred within a day, and I remembered restarting something without recalling which service I touched. I forgot how long the calm lasted after each restart.

I checked timestamps across three evenings from the host graphs. The slow window ran 19:40 to 21:10 on Monday and Tuesday. Wednesday stretched to 21:40 with the same rough curve.

The rule I took from that week: observations must land in a notebook, and memory alone never counts as data.

## Setting Up the Daily Notebook

I keep the notebook as a folder of dated Markdown files with a chart image each. I write entries in ten minutes at the end of the workday. Missing days stay missing with no backfilling allowed.

I created Notekeeper, a small script for this task, to scaffold each entry. It stamps the date, pulls yesterday's traffic totals, and leaves blank slots for hypothesis and decision. The scaffold keeps entries uniform.

Scaffolding a new entry takes one command:

```bash
uv run python scripts/new_entry.py
```

The command writes `notes/2026-04-14.md` with headers and yesterday's totals. I fill the rest by hand because typing forces me to think.

Every entry follows the same five slots:

- traffic totals and deploy notes
- hypothesis for anything odd
- chart image with a two-line caption
- anomaly verdict after review
- decision with a date for recheck

I borrowed the layout from lab notebooks in experimental physics. The [Python logging guide](https://docs.python.org/3/howto/logging.html) shaped how I timestamp each claim. I prefer fixed slots over free text because review takes four minutes per entry.

## Hypothesis Paired With a Chart

Each entry states a guess before showing any graph. The guess names the suspect and the expected curve in the data. Writing it first stops me from reading stories into noise later.

A typical hypothesis reads like this in the file:

```text
Hypothesis: the backup job steals disk IO around 20:00.
Expect: read latency spikes match the backup window.
```

The chart under it shows request latency with the backup window shaded. I export the image from Grafana at 900 pixels wide, and uniform sizes make week-to-week comparison instant.

The pairing rule stays strict with no exceptions made. A chart without a prior hypothesis gets no verdict that day. Three entries in April hold charts marked as stray observations only.

April 14 gave the first clean confirmation of a guess. Read latency tripled exactly inside the shaded backup window. The app curve and the disk curve rose within the same two minutes.

That entry felt different from the earlier guessing streak. The guess came first, the chart matched, and the decision was obvious. I moved the backup to 03:00 the same night.

## Anomalies Reviewed Into Decisions

Not every odd curve earns action, so Fridays hold a thirty-minute review. I reread the week of entries and mark each anomaly as real or noise. Real ones get a decision with a recheck date attached.

The review covers four questions in the same order:

- did the curve repeat on multiple days
- does a deploy or cron job explain the timing
- did the linked change move the metric
- when do I recheck this decision

Two April anomalies died at the second question. A latency bump on April 9 matched a dependency upgrade I had forgotten. A traffic dip on April 17 matched a public holiday in my largest user country.

One anomaly survived into a real fix with measured results. Evening p95 latency fell from 1.9 seconds to 420 milliseconds after the backup move. Median latency barely changed, which told me the backup hurt tails only.

I keep decisions small and reversible by design. I change one thing, note the date, and recheck after seven days. So far I logged eleven decisions with eight confirmed and three rolled back.

## Lessons From Four Weeks of Notes

Those notes paid off before April ended with the backup fix. Evening slowdowns vanished across nine straight days of graphs. Total effort ran about five hours of writing plus two reviews.

One gap remains around metrics I never captured. Memory pressure has no chart because I export only latency and traffic. A May incident needed memory data I simply didn't have.

I keep three habits from this month for every system I run. I write the guess before exporting the chart. I review weekly with fixed questions and recheck dates. I keep decisions small enough to reverse in minutes.

Five hours of notes replaced roughly twelve hours of repeated guessing. That trade looks fine to me, and I'd start the notebook on day one of the next project.

I'll write more about lightweight observability for single-server side projects in a future post. If you want to follow along, don't forget to subscribe.
