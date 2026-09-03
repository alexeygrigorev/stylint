# Summarizing Server Logs into Daily Highlights

I wrote this synthetic style exercise as a build log, and all project details are fictional. In February 2026 my recipe box API on a 5-euro VPS produced about 80 MB of logs per day. I read them in a terminal pager and still missed the lines that mattered.

The service has about 200 daily users. Nginx writes access logs, the app writes structured lines to journald, and a Postgres container adds its own stream. Scanning all three took me 30 minutes on a bad day. My review notes were guesses more often than facts.

In this post, I'll share:

- why plain reading stopped working
- how my first attempt with a coding agent failed
- how the digest script parses and groups the logs
- which anomaly flags made the cut
- how the report reaches me at 08:00
- which limits the digest still has

## Log Volume In March

The volume grew with the user count. In January the three sources wrote about 35 MB per day, and by late February the number passed 80 MB. My habit of scrolling through a pager broke somewhere around 40,000 lines per day.

I tried two quick fixes first. I grepped for ERROR and I tailed the last 500 lines. Both approaches only moved my attention to whatever happened latest, so a failure from 09:00 could hide behind a quiet noon.

## First Attempt With An Agent

My first real attempt was to give a full day of logs to a coding agent. I pasted a 12 MB sample into Claude Code and asked for a summary of anything unusual. The session burned about 90,000 tokens in two minutes and returned five generic sentences.

One sentence claimed the service was healthy. The same sample contained 38 timeout errors, so the summary was worse than useless for my morning review.

My mistake was feeding raw volume to a model that reads tokens. The rule I took from it: reduce the logs to counts before any model sees them.

## Parsing And Grouping

So I built `digest.py`, a small Python script that turns the three log streams into one page of counts. The script reads the nginx access log, the journald stream from the app and the Postgres container log.

Each line becomes a small record with a timestamp, a route, a status code and a duration. The grouping step buckets records by route and hour. A spike at 15:00 then stays visible instead of dissolving into the daily total.

Rebuilding any day's digest takes one command:

```bash
uv run python digest.py --date 2026-03-11 --sources nginx,app,postgres
```

The run takes about 9 seconds on the VPS and writes `reports/2026-03-11.md` next to the logs. The file is plain markdown, so I can read it on my phone.

## Anomaly Flags

The counts alone were still a wall of numbers to me each morning. They needed a verdict attached before they could save any time.

The script fires a flag in four situations:

- the 5xx share of a route passes 1% for the day
- the 5xx count for one hour doubles the same hour from the previous day
- p95 latency on a route passes 2 seconds for three hours in a row
- request volume drops by half against the same weekday average

The latency check has the shortest code, and the other checks follow the same form:

```python
def slow_hours(records, limit=2.0):
    hours = group_by_hour(records)
    flagged = [h for h in hours if p95(h) > limit]
    return len(flagged) >= 3
```

Three hours in a row keeps one slow request from raising a flag. The threshold of 2 seconds comes from my p95 baseline of 700 milliseconds on the read routes.

The first week produced 4 flags per day, and 3 of them were noise from a cron job that imports recipes at 02:00. I excluded the import route from the volume flag, and the count fell under one flag per day.

## Delivery Each Morning

A flag list only helps when it arrives on its own. A cron entry runs the digest at 07:45, and a small webhook drops the text into my Telegram saved messages.

The cron line looks like this:

```bash
45 7 * * * cd /srv/digest && uv run python digest.py --date today --deliver telegram
```

The message runs about 25 lines, and reading it takes under two minutes with coffee. Delivery failures appear in the next digest, because the script writes a line to journald when the webhook returns anything other than 200.

## Limits After One Month

After one month of daily digests, the routine holds. Counts replace scrolling, flags give the morning a starting point, and the full review takes two minutes.

The digest still misses causes. It told me on 6 March that 5xx responses on /search had doubled, and the reason, a bad synonym config, took another hour to find. Counts start the investigation, and they never finish it.

The flag set is also narrow. Anything without a number, like a confusing error message that users screenshot, never reaches the page. I still read the app log by hand about once a week.

The project stayed small on purpose. One script, one cron entry and one Telegram message replaced 30 minutes of scrolling, and the VPS still costs 5 euros per month.

I'll write about threshold tuning with a full quarter of data in a future post. If you want to follow along, don't forget to subscribe.
