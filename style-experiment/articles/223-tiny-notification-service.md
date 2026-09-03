# A Tiny Notification Service for Personal Automations

I wrote this synthetic style exercise as a build log, and all project details are fictional. In February 2026 a failing backup job emailed me 34 times between 01:00 and 09:30. I saw the pile at noon, and a real disk warning sat unopened in the middle of it.

By January 2026 I already ran 11 small automations for myself.

The four loudest ones were:

- a nightly Postgres backup with a checksum pass
- a price watch on three products in a spreadsheet
- deadline checks for two courses I help run
- a scraper that watches a registration page for open seats

Every script emailed me directly through the mailing provider's API, so my inbox was the alert channel. The scripts produced about 40 emails a week, and maybe four of them needed a same-day answer. The average week looked fine, and the bad nights looked like February.

In this post, I'll share:

- what 11 uncoordinated scripts did to my inbox
- why my first webhook attempt drowned a Telegram chat
- how the service separates events from channels
- how dedupe and quiet rules cut the noise
- what the service looks like in July 2026

## A Dozen Scripts, One Inbox

The 11 scripts each had their own send call, their own subject line, and their own idea of urgency. A checksum warning arrived with the same subject weight as a scrape report about a seat nobody wants. When something broke at night, the evidence waited in a pile I read at noon.

## My First Attempt With Group Webhooks

My first fix moved everything into one Telegram group in early February. Each script posted straight into the chat through its own bot, and urgent messages drowned among scrape results within days.

During the February backup flap, the failing job posted 34 messages in under nine hours. The two messages I actually needed came from other scripts. I had traded an inbox I check twice a day for a chat I check twice a week. That trade was a bad one.

A channel without judgment just moves the noise. The rule I took from that night: put a filter between the event and the delivery, and let one piece of software own it.

## Events and Channels

In March I built `notify-gw`, a small FastAPI service that receives events over HTTP and decides what happens to each one. It runs on the $5 VPS that already hosts my dashboards, and it needs no database server beyond SQLite.

The events live in one SQLite table at `/home/me/ops/notify.db`:

```text
create table events (
    key         text,      -- script and type, like backup/failure
    severity    text,      -- error, warn, info
    body        text,
    delivered   int default 0,
    created_at  text
);
```

Scripts post one JSON object per event to a single endpoint:

```bash
curl -s http://localhost:8710/events -d '{"key": "backup/failure", "severity": "error", "text": "pg_dump exited with 1"}'
```

The endpoint checks three fields, writes the row, and answers with 202. A worker loop delivers queued events one second later, so a slow channel never blocks a script.

Delivery currently uses three channels:

- a Telegram bot, for anything with error severity
- a morning digest email, for everything else
- a plain log file at `/home/me/ops/notify.log`

The log channel exists because I don't trust an alert setup I can't grep afterwards.

## Dedupe With a Memory Window

The dedupe rule lives in a config file at `/home/me/ops/notify-rules.yaml`.

Each entry in the file names an event key and a memory window:

```text
- key: backup/failure
  window_minutes: 60
- key: price/watch
  window_minutes: 0
```

An event whose key delivered a message within its window is counted and dropped. The count survives, and the morning digest reports it as "backup/failure: suppressed 33".

The February flap would now produce one Telegram message plus a suppressed count of 33. That single change removed about two thirds of my overnight noise, based on a week of before-and-after counts in April.

Keys with no entry get a default window of 30 minutes, which I picked because most of my jobs run hourly. The window counts wall-clock time, so a job that fails at 02:00 and again at 07:00 produces two messages, and I want both.

## Quiet Rules and Severity

Every event takes a severity of error, warn, or info. Errors go to Telegram immediately, at any hour. Warn and info events wait during quiet hours from 22:00 to 07:30, then join the morning digest.

The digest is plain text, and the head of the April 14 message reads:

```text
Morning digest - 6 events since 22:00
- price/watch: 3 checks, no changes
- deadline-check: 2 events, next deadline in 9 days
- backup/checksum: ok
```

In April the service received 480 events and delivered 61 messages, and 39 of those waited for the digest. That ratio surprised me, because I had expected more errors and fewer scrape reports.

## The Service in July 2026

Four months in, the service does its job with two known gaps. Dedupe counts suppressed repeats but never escalates, so a job that fails 30 times in a day stays a single message. The delivery worker retries three times over five minutes and then drops the event, and the log file is the only record that it tried.

The whole service is about 300 lines of Python plus 40 lines of YAML, and I can read all of it in one sitting. It has one user, and that user sits close enough to the VPS provider's status page to notice an outage.

The arc took three months. January had 11 solo emailers, February drowned a chat, and March got a filter with memory. I read the morning digest with coffee now, and it takes about three minutes.

I'll write about the escalation rule once it exists and has survived a month in production. If you want to follow along, don't forget to subscribe.
