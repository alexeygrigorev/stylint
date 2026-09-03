# Automating the Boring Parts of My Weekly Review

I wrote this synthetic style exercise as a build log. The project, dates and measurements are fictional. Every Friday I spent 90 minutes assembling my weekly review from commit logs, calendar events and half-remembered numbers.

The assembly bored me enough that I skipped three reviews in April. Each skipped review cost me the thread of two ongoing projects, and Monday planning turned into archaeology twice.

In this post, I'll share:

- what the manual review collected
- how I automated metric collection
- how I draft highlights without fabricating
- which choices I kept manual
- where the Friday routine stands now

## Ninety Minutes Of Assembly

The manual review pulled numbers from four places. I opened the git log for commit counts and the calendar for meeting hours. Then I checked the time tracker for project splits and my notes folder for open loops.

Copying those numbers into one document took most of the 90 minutes. The actual reflection took 15 minutes, and it often got squeezed out when the assembly ran long.

The rule I took from April is simple. I automate the collection completely, I draft the summary mechanically, and I reserve my own attention for judgments.

## The First Version

My first script generated the entire review including conclusions. It counted commits, converted the counts into productivity claims, and wrote sentences about focus that the data never supported.

The output read smoothly and said nothing I trusted. One Friday it praised my "deep focus on the API migration" during a week I had spent mostly in hiring interviews.

Automation that invents judgments destroys the review, so I deleted the conclusions the same evening. I kept only the collection half of the script.

## Collecting Metrics Automatically

The keeper script runs every Friday at 4 PM and writes a metrics file. It reads local sources only, and it finishes in under a minute on my laptop.

The collection command runs from cron:

```bash
uv run python scripts/weekly_metrics.py --week 2026-06-08
```

That script counts commits per repo, sums calendar hours by category, and totals tracked time per project. It writes the results to `reviews/2026-06-08-metrics.json` with one record per source.

The JSON file holds 40 to 60 numbers in a typical week. I read that file before writing anything, and the numbers anchor the review against my faulty memory of the week. My memory of hours worked runs 20 percent optimistic in busy weeks, and the file corrects it without argument.

## Drafting Highlights Mechanically

The second script turns the metrics file into a draft with blank judgment slots. It writes the numbers into sentences and leaves explicit markers where I add interpretation.

A generated draft looks like this:

```text
Commits: 23 across 3 repos (peak: API migration).
Meetings: 9.5 hours, hiring took 40 percent.
Open loops: 7 open, 3 closed.
Judgment: [FILL IN]
Next week: [FILL IN]
```

I fill the two marked slots by hand every Friday. The script refuses to finalize the review while either marker remains, and that refusal gates the whole review.

The draft never invents causes or praise. When commits drop by half, it prints the count without explaining why, and I supply the reason from memory.

## Choices I Kept Manual

Three decisions stay with me no matter how smooth the automation gets. I judge whether the week served the quarter goals, I choose the three priorities for next week, and I close or defer each open loop.

Those choices take about 20 minutes with the draft in front of me. The metrics answer what happened, and I answer whether it mattered, since no script knows my goals. That division took three weeks to trust, and the first trusted review convinced me the format holds.

I also kept the archive format manual at the edges. I save the finalized review as a markdown file I can read in two years. I write its closing paragraph as full sentences rather than slots.

My manual checklist fits on three lines:

- the two judgment slots hold my own words
- next week's priorities number exactly three
- each deferred loop names its review date

That last line prevents silent deferral. A loop that survives three weeks without progress gets a decision: schedule it, shrink it or drop it.

## Fridays In Half The Time

The Friday routine now takes 35 to 40 minutes against 90 before. Collection takes one minute, the draft takes another minute, and my 20 minutes of judgment plus filing take the rest.

Review skipping stopped completely since May. Eleven consecutive Fridays produced eleven reviews, and Monday planning reads the latest file instead of reconstructing the month.

The reviews also improved as records. Each file holds the same metrics in the same order, so comparing June against March takes minutes rather than a re-read of scattered notes. I compared my Q2 project splits in one sitting before the July planning call. The numbers settled a debate about where my hours actually went.

The automation works because it respects the boundary between counting and judging. I let the scripts count everything, and I kept the two slots that require a human with goals. That boundary held for four months without exception.

I'll cover the metrics schema in detail in a future post. If you want to follow along, don't forget to subscribe.
