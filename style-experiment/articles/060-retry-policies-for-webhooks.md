# Designing Retry Policies for Webhook-Driven Automations

I wrote this how-to guide as a synthetic style exercise, and the endpoint names, volumes, and incident details are fictional. I use the workflow when I connect an external webhook to an internal automation that changes data or sends messages.

The first version of my invoicing listener processed 4,318 webhooks successfully and then failed badly during a 22-minute provider outage. The listener acknowledged each event, called a billing database that was unavailable, and dropped the payload. Retries at the application layer didn't exist.

In this post, I'll share:

- how to make event processing idempotent
- how I set timeout and retry counts
- how the dead-letter queue works
- how alerts stay useful
- how I test the whole workflow

## Make Processing Idempotent

Idempotency means running the same event twice without changing the result twice. For an invoice webhook, I store the provider's `event_id` before applying any update. If that ID already exists, the listener returns success and skips the work.

The storage must sit in the same transaction as the change. Otherwise, the listener can record the event and then fail to update the invoice, leaving no path to retry the business change. A webhook table alone doesn't solve that problem.

```sql
begin;
insert into processed_events(event_id, received_at)
values ($1, now())
on conflict (event_id) do nothing;

update invoices
set status = $2, paid_at = $3
where invoice_number = $4;
commit;
```

For nontransactional systems, I use a two-step approach. First, write the event to a queue with its unique ID. Second, let a worker apply the change and mark the queue entry complete. If the worker stops, another worker can resume from the queue.

I also record enough source data to reconstruct the action. A provider may allow only three retries, and its replay window may expire in 24 hours. Storing the payload in the local queue makes the automation independent of that window.

## Timeouts and Retries

Every outbound call needs an explicit timeout. My listener allows 2 seconds for database reads, 5 seconds for the invoice update, and 10 seconds for messages sent to Slack. The webhook endpoint acknowledges the provider as soon as the event is safely queued.

I use exponential backoff with jitter. The first retry waits 5 to 10 seconds, the second 30 to 60 seconds, and the third 5 to 10 minutes. Jitter prevents 500 failed events from retrying at exactly the same millisecond.

The current limits are four attempts inside the worker, then a dead-letter entry. Provider retries are enabled separately, with a maximum of three attempts over six hours. I keep the two layers independent because one controls local recovery and the other controls transport.

```yaml
retry:
  max_attempts: 4
  initial_delay_seconds: 5
  max_delay_seconds: 600
  jitter: full
dead_letter_after: final_attempt
```

For read-only events, I reduce retries to two attempts. A failed lookup for an optional audit trail can often wait for the next update. For payment events, I keep four attempts and block the queue from processing newer events for the same invoice until ordering is resolved.

## Dead-Letter Queue

I store the dead-letter queue in a database table rather than a folder of forgotten logs. Each row contains the original payload and headers, together with the provider event ID.

I review the error class first. A validation error needs a different response from a timeout or an expired invoice status.

I keep four broad classes. They distinguish transient problems, validation errors, authorization failures, and unknown errors.

Each business day, a small job groups dead-letter entries by class and provider event type. It sends one summary to a private Slack channel. For a recurring payment class, the summary includes affected invoice numbers and total amounts so I can judge urgency.

Replay is explicit because a command takes dead-letter IDs and copies them back into the active queue.

```bash
billing-worker replay --ids 1841,1842 --reason "dependency outage resolved"
```

During the invented outage, the queue held 237 payment events and 1,105 audit events. I replayed payment events in four batches and let audit events run later. Total recovery took 38 minutes, and no invoice changed twice.

## Useful Alerts

An alert on every failed webhook would be noisy. A single daily digest would be too slow for payment problems. I use three notification levels tied to event type, queue age, and the ratio of failures in the last five minutes.

The urgent alert fires when any payment event reaches the dead-letter queue or when more than 5% of payment events fail in five minutes. It goes to a phone channel and includes the oldest affected event ID.

The warning alert fires when audit events exceed 50 failures in 15 minutes or when the active queue contains more than 500 entries. It goes to a channel I read during work hours.

The daily report covers validation problems, replay counts, dead-letter age, and throughput. I don't page anyone for validation errors, but they're often the first sign that a provider changed its payload schema.

Every alert links to a saved query. That small detail removes the first ten minutes of diagnosis because I can see the error class and affected invoices without assembling a database query.

## Test the Workflow

I test three layers separately. Unit tests cover backoff calculations, while integration tests use a real Postgres database.

A third test replays a recorded outage. It publishes 1,000 events, stops the billing dependency after 300, and restores it after 90 seconds.

```text
events: 1000
dependency failures: 700
retries: 812
dead_letter_after_recovery: 0
duplicate invoice changes: 0
```

I also test the dead-letter path deliberately. A webhook with an unknown invoice number should land there after retries. The test asserts its error class, checks that the original payload remains unchanged, and verifies that replay leaves it in a new active entry.

These tests run on every change to the worker. They aren't a substitute for a staged provider sandbox, but they catch most regressions before I connect the endpoint to real payments.

## Practical Rules

A webhook is a message, not a completed action. Queue it safely, acknowledge the provider, and process it with code that can survive repeated delivery.

Retries need limits, and failures need a destination. Exponential backoff handles temporary dependency problems, while a dead-letter queue and review workflow handle problems that no retry count can solve.

I plan to write about the recovery replay tool in more detail in a future article. Subscribe if you want to see how it handles schema changes.
