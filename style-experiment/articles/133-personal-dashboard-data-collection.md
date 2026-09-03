# Collecting Data for a Personal Dashboard Without Creeping on Myself

In January I caught myself keeping three time-tracking apps, two note exports and a browser history file for a dashboard I never opened. The files described a fictional studio business called `homeline`, but the instinct to keep everything felt real. I had more raw data than useful answers, and I couldn't explain half of it to myself six weeks later.

I wrote this piece as a synthetic style exercise. Every project, device, event, cost and usage number it contains is fictional.

That mess made my design goal clear: I didn't need more collection. I needed events that answered actual questions, retention rules I could defend, and controls that kept sensitive details off a shared screen.

In this post, I'll share:

- how I chose the dashboard's questions
- how I defined events instead of copying whole databases
- how I set retention rules before the first write
- how I aggregated data without losing useful detail
- how I controlled access to the interface
- what the dashboard shows after eight weeks

## Start With the Questions

I listed what I actually wanted to decide each week.

The list came down to four questions:

- which project consumed the most focused time
- which recurring tasks returned every week
- when my energy was highest for hard work
- which subscriptions produced no recorded use

These questions excluded several tempting sources. Locations, messages, browser history and microphone data couldn't answer any of them, so I didn't collect those things. I also skipped keyboard-level activity tracking because it felt invasive even on my own machine.

The hardest decision involved energy. A number from 1 to 5 seemed simple, but it depended on sleep, workload and mood. I decided to use only two labels: focused work and shallow work. Those labels were easier to apply consistently.

## Define Events, Not Streams

The first version tried to import full calendar files and all task records. That gave me 14,300 rows in one test load, and most rows repeated information I already knew. It also copied client names into a tool that only I needed to use.

We replaced that import with a small event table. Each event records an action, a project label, a duration in minutes and a privacy class.

The table uses these fields:

```text
event_id
occurred_at
action: focused_work | shallow_work | subscription_use
project: invoice_app | course_notes | studio_admin
minutes: integer
privacy: private | work
```

The project labels hide client names. A separate encrypted note can hold the original task, but the dashboard reads only the general project. This makes it easy to share a screenshot without explaining a confidential engagement.

For subscriptions, I record one monthly event with the service, cost and whether I opened it in the prior 30 days. I don't ingest login logs or page views. The decision only needs that coarser fact.

## Set Retention Before the First Write

Retention was easier to negotiate with myself before any data existed. After two weeks, every old event started to feel like evidence I should keep.

The current policy lives in `homeline/config/retention.toml`:

```toml
[events]
work = 365
private = 30

[aggregates]
weekly_project_hours = 730
subscription_history = 1095
```

A nightly job deletes expired raw events and runs `VACUUM`. The private class covers calendar titles and personal tasks, while work events remain available for invoices and quarterly planning.

I also added a restore test. Every month I delete a fabricated event that's 31 days old, rerun the aggregation queries and verify that weekly totals stay stable. That test caught one query reading the wrong timestamp field before the first real deletion.

## Aggregate Early

Raw events answer "what happened on Tuesday". Weekly aggregates answer the questions I actually bring to planning. I now store both, but the dashboard's default view uses only aggregates.

The nightly job builds three tables:

- weekly focused and shallow hours by project
- recurring tasks with their median duration
- subscription use and cost by month

For example, `homeline` reported 21.5 hours of focused work during the first week of March. Course notes used 9.0 hours, the invoice app used 8.5 hours, and studio administration used 4.0 hours. Those numbers are enough to decide the next week's plan.

When I need a finer view, I query raw work events directly. I deliberately didn't build a drill-down interface. The extra click gives me time to ask whether I need that detail and whether the retention period still covers it.

Aggregation also improves honesty because a dashboard filled with minute-level activity looked busy. A table with six weekly numbers makes an empty project obvious.

## Control Access to the Interface

The first version ran on a small server with a public URL and a 12-character password. I turned that off after one evening. It exposed project rhythms and subscription costs to an internet scanner for a small convenience gain.

The dashboard now runs on my office machine and listens only on `127.0.0.1:8712`. To use it remotely, I connect through Tailscale, a mesh VPN that creates a private connection between my devices. There's no public port.

I divided access into two views. The private view shows personal events and unmasked notes, while the work view excludes those rows and caches only aggregate tables. A shared screen starts on the work view, so an accidental audience sees only project hours and subscriptions.

The server writes an access log with the view, source address and query time. It doesn't record the selected project or date range. Those details could expose more than the dashboard does.

Every quarter, I rotate the database backup key and review the access log. In April, that review found only three connections, all from my laptop.

## Status After Eight Weeks

After eight weeks, the system has 1,180 raw events, 112 weekly aggregate rows and 24 subscription records. The database uses 8.2 MB. The full pipeline runs in 40 seconds each night and costs nothing beyond the existing office server.

The useful outcome is quieter. I can answer the original four questions in one screen. Two subscriptions were cancelled in February, which saves EUR 19 per month. One project had 41 hours of shallow work and only 6 hours of focused work, so I moved its remaining tasks to a contractor.

Some limits remain:

- energy labels still depend on my consistency
- recurring tasks rely on clean names
- offline work requires a manual evening entry
- contractor invoices don't yet connect to project hours

I don't plan to add automatic browser tracking or location data. The dashboard works because it answers a small set of questions and forgets most details on schedule.

I plan to add a quarterly report that compares planned project hours with actual focused hours. I'll write about it after it survives one full quarter. If you want to follow along, don't forget to subscribe.
