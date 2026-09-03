# Monitoring a Background Job Queue on a Small Server

I wrote this synthetic style exercise as a build log, and the server, dates and numbers are fictional. In April 2026 a queue of 1,214 thumbnail jobs stalled for six hours on my 4.60 EUR per month VPS while I slept. The website looked healthy the whole time, because the queue was invisible from the outside.

A user wrote to me at breakfast about uploads that never finished. The worker had crashed at 02:40, and nothing restarted it. Detection took six hours, and the fix took two minutes.

In this post, I'll share:

- the manual check I outgrew
- four numbers the jobs table already tracks
- the retry schedule and failure counts
- alerts to my phone through cron
- where the queue stands after two months

## The Manual Check

My first check was a SQL query I kept in a notes file and ran when something felt wrong. That morning it showed 1,214 pending jobs, and the oldest had been waiting for 5 hours and 51 minutes. I restarted the worker service, the queue drained in 12 minutes, and I closed the incident with no change to the system.

The same stall could happen again that night, so I built a small watcher instead. The app runs on FastAPI with Postgres, and a worker script drains the `jobs` table between web requests. Every row already has the fields a monitor needs, so the first version took an evening.

The notes file had a second problem. Nothing in it distinguished a slow queue from a dead one, because I only ran the query when an upload already felt slow. Monitoring needed to live outside my memory.

The whole stack runs on one small server, and a separate monitoring service felt heavy for a queue that fits in one Postgres table. Reading the table from a cron job keeps the watcher inside the same 4.60 EUR budget as everything else.

## Four Numbers From The Jobs Table

I called the watcher script `queue-health.py`, and every run records four numbers:

- depth: rows in pending state
- age: minutes since the oldest pending row was created
- failures: rows marked failed in the last hour
- retries: rows waiting for their next attempt

The query behind the first three numbers fits in seven lines:

```sql
select count(*) as depth,
       max(now() - created_at) as age,
       count(*) filter (where status = 'failed'
         and updated_at > now() - interval '1 hour') as failures
from jobs
where status in ('pending', 'failed');
```

Depth and age come from pending rows, while the filter clause counts recent failures separately. Retries are rows whose `attempts` column sits below the limit of five. Each run appends one line to a log, so I can graph the queue after the fact.

The numbers came straight from the schema, and that choice was deliberate. A monitor that needs new columns will drift from the app, and a drifted monitor reports a queue that no longer exists.

## Retries And Failure Counts

The worker allows five attempts per job with a backoff schedule of 2, 8, 30 and 90 minutes. Retries made the queue look healthy while it was dying, and that was the April lesson in one sentence. A job that fails five times moves to failed, and the failures count catches it within the hour.

The backoff schedule lives in one config constant and restarts cleanly between jobs. Nine jobs have exhausted all five attempts since April. All nine were images above the 25 MB upload limit that the client should have rejected earlier.

My first alert fired on depth alone, and it woke me 11 times in one night during a legitimate import of 900 files. The rule I took from it: alert on age and failures, and let depth stay informational.

## Alerts To My Phone

The script posts to ntfy, a small self-hosted service that turns HTTP posts into phone notifications.

The alert rules are two thresholds:

- age above 45 minutes
- failures above 10 in one hour

Cron runs the whole thing every 10 minutes and keeps a log of every check:

```bash
*/10 * * * * /home/deploy/bin/queue-health.py >> /var/log/queue-health.log 2>&1
```

One line goes into the log every ten minutes, and about 144 lines cover a day. An empty log means cron stopped working, and that failure needs a different alert, which I haven't built yet. ntfy also supports a priority field, so an alert arrives with a loud sound instead of a silent badge. I set age alerts to high priority and failure alerts to default, because failures accumulate while age means the queue has stopped.

## The Queue Today

The watcher went live in late April, and it has caught three real stalls since then. Each one surfaced within 20 minutes of the oldest job crossing the age threshold. Two were crashed workers after server reboots, and one was a Postgres restart that left connections dead.

Depth alone stays informational, exactly as the rule demands. The resize step in ImageMagick can still hang without failing, and a hung job sits in running state forever, invisible to all four numbers. A watchdog for running jobs is the next piece, and I'll describe it once it has caught something.

The four numbers cost nothing to collect, and the alerts have earned back their build time twice over. Throughput is the remaining blind spot. A queue draining at one job per hour looks identical to one draining at a hundred, and only the weekly graph shows the difference.

I'll write about that watchdog in a future post. If you want to follow along, don't forget to subscribe.
