# Adding Observability to a Writing Bot

On July 2, 2026, a Telegram writing bot I had run for 14 weeks started timing out. Users still saw old replies in their chat history, so their reports disagreed with my server log. I spent most of that evening guessing.

I wrote this as a synthetic style exercise with invented bot traffic and dates. I would still add the observability workflow before deploying a similar bot.

In this post, I'll share:

- what the first incident made visible
- how I added request IDs without changing the user interface
- how I logged latency and failure classes
- what the dashboard showed after two weeks
- which alerts I kept and which ones I removed

## The Guessing Phase

The first version logged errors only. A Python traceback entered the console when an exception reached the top level. Successful requests disappeared after the reply left the process.

During the incident, the log showed 23 exceptions over 90 minutes. User reports suggested at least 60 failed replies. I had no way to connect a chat message to a downstream model call, a database write, or the Telegram delivery step.

I restarted the container at 21:40. The failures stopped for two hours and then returned, which told me the problem could recur under load but little else.

## Request IDs

The next morning I added a request ID at the point where the bot received an update. I used the Telegram update ID as the ID because it arrived with every message and needed no extra generator.

I passed that ID through four stages:

```text
receive update -> normalize text -> call model -> deliver reply
```

Each stage wrote one JSON line to a log file.

A simplified line looked like this:

```json
{"request_id": "982341", "stage": "model", "status": "ok", "latency_ms": 1980}
```

I didn't log the user's message. I stored its length, detected language, and a boolean for attachments, which gave me enough information to group traffic without putting drafts into a log.

The change took about two hours. The important decision was to attach the ID to a context object at entry. The model and delivery functions then received it as an argument instead of reconstructing it.

## Latency and Failure Classes

After a day of stable logging, I wrote a small aggregation script. It read the JSON lines every five minutes and produced one row per request. The row contained the request ID, stage statuses, total latency, and failure class.

I started with these classes:

- validation
- model
- delivery
- storage

Anything unknown went into a fifth class called other. I treated every unknown case as a task to either name the failure or prove that it was harmless.

The first two weeks produced 4,812 requests.

The split looked like this:

- 4,413 requests completed successfully
- 238 failed at the model stage
- 94 failed delivery
- 51 failed validation
- 16 went into other

Median latency was 1.2 seconds, and the 95th percentile reached 4.8 seconds. Averages hid a long tail caused by document uploads, so I stopped looking at averages.

## The Dashboard

I already ran Grafana on the same small server, so I pointed it at the aggregated rows.

The first dashboard had these panels:

- requests per hour
- success rate
- median and 95th-percentile latency
- failures by class

The hourly graph immediately explained the original incident. Traffic peaked around 20:00, and failed requests clustered in that window. The database had reached its connection limit while a nightly backup job held several connections open.

I moved the backup to 03:30 and reduced its connection pool from 12 to 4. The graph made the timing obvious, so the fix took ten minutes. Delivery failures then fell from about 120 per evening to fewer than 8.

The second panel was less useful. Total requests rose and fell with user habits, so a dip on Friday told me people were away but said nothing about quality.

## Alerts and Remaining Gaps

My first alert fired whenever any error appeared. It was noisy and I ignored it after two days. That was my mistake: I configured an alert for an event rather than for user impact.

I replaced it with two rules.

The first tracked failures, and the second tracked latency:

- more than 10 failed requests in 15 minutes
- 95th-percentile latency above 8 seconds for 30 minutes

Both alerts send one message to a private Telegram channel. Since the change, the delivery alert fired twice for real incidents, while the latency alert hasn't fired yet.

I still have two gaps. I don't measure answer quality, and I don't know how many users give up after one failed request. I'll need sampled review and a small follow-up survey to close them.

The log retention policy is still simple. Raw JSON lines stay on the server for 30 days, while the five-minute aggregates stay for 12 months. That keeps enough history for seasonal comparisons without storing drafts for a year.

If I started again, I would add the request ID and failure classes before the first public release. The work took less than a day. The incident cost an evening of guessing and at least one user conversation that could have been shorter.

## Lessons from Two Weeks

Observability didn't make the bot clever, but it made the failure path visible enough to fix.

The request ID was the smallest change with the largest payoff. Failure classes came next because they turned random exceptions into named work. The pretty dashboard came last and mostly helped me see timing.

I plan to add sampled answer review next month. If you want to follow that experiment, subscribe for updates.
