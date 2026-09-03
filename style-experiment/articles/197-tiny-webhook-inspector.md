# Building a Webhook Inspector for Debugging Integrations

I wrote this synthetic style exercise as a build log, and all project details are fictional. In February 2026 I lost an evening to a webhook integration that failed without any error. The sending service kept only the last delivery of each event. The next morning I started hook-catch, a small local service that records every delivery.

The integration belongs to a small print shop that sells my photos, and its payment provider announces orders and refunds through webhooks. During development the shop ran on my laptop, so the provider reached it through a tunnel. When an order stalled, I had no way to see what the provider had actually sent.

In this post, I'll share:

- why logging payloads to the console failed
- how the receiver stores every delivery
- why the signature gets checked before redaction
- how replay and comparison work
- what still breaks after a month of use

## The Console Attempt

My first receiver was a 30-line FastAPI app that printed each request body to the terminal. I ran it behind the tunnel, watched the output scroll past, and copied interesting payloads into files by hand. That worked for one calm afternoon of testing.

It failed as soon as the shop met real traffic. The terminal buffer held only the last 200 lines, and one busy afternoon produced 60 deliveries. The provider signs each payload, and the signature sat in a header my print statement ignored. Restarting the app to add a field wiped every record, so I rebuilt the same bug twice.

The mistake was treating deliveries as disposable output. The rule I took from it: a webhook you didn't store is a webhook you can't debug.

## Receiving And Storing Deliveries

The replacement keeps the same FastAPI entry point and adds storage. Every POST to `/hook/{name}` becomes one row in SQLite, in a database file named `deliveries.db`. During development a tunnel forwards the provider's calls to `127.0.0.1:8800`, and the receiver never sees the difference.

The whole schema fits in one small block:

```text
deliveries
  id            integer primary key
  source        text        -- hook name, like "payments"
  received_at   text        -- UTC timestamp
  headers       text        -- full headers as JSON
  body          text        -- raw payload as JSON
  signature_ok  integer     -- 1 when the HMAC check passed
```

Storing the raw body before parsing anything was the decision that made the rest easy. Redaction, replay, and comparison all read from the same row, and nothing depends on code that runs at receive time. The tool uses about 3 MB of disk per hundred deliveries, so storage is a non-issue at my volume.

## Verification Before Redaction

The provider signs each delivery with a shared secret, so hook-catch verifies the HMAC before touching the body. The check happens once at receive time, and the result goes into the `signature_ok` column. Only then does the redactor run.

The redactor visits every key in the stored JSON and replaces values whose names appear on a deny list.

The deny list starts with six key names:

```python
REDACT_KEYS = {
    "authorization", "token", "secret",
    "card", "cvv", "email",
}
```

The redactor writes the string `***` in place of each value and records how many fields it touched. On a real order payload of 38 fields, it replaces between 2 and 6 of them, so the payload's structure stays visible. A redacted record is useless for debugging if it hides the structure too, and that trade decides every redaction rule I write.

I learned the ordering the hard way. An early version redacted first, and every signature check failed for an hour before I reread the provider's docs.

## Replay And Compare

Two commands cover most debugging sessions.

Replay resends a stored delivery to any URL I name:

```bash
uv run hook-catch replay 412 --to http://localhost:8000/hook/payments
```

The command rebuilds the stored body, refreshes the timestamp header, and posts it again with httpx, a small HTTP client library. With `--edit` it opens the body in my editor and resends whatever I save. That's how I test whether the shop survives a duplicated event.

Compare answers the question the provider's dashboard never could.

I point it at two row ids of the same event:

```bash
uv run hook-catch diff 412 415
```

The command prints one line per changed key:

```text
order.status:      "paid"    ->  "refunded"
order.updated_at:  10:14:02  ->  10:14:29
```

The output is deliberately narrow. Full payload dumps sit one command away, but the diff view is what I read 90 percent of the time. In March this comparison found the bug that started the project. The provider had sent a refund event before the matching payment event, and the shop processed both in arrival order. The fix took one ordering queue of about 20 lines and an afternoon of tests.

## Limits After One Month

The tool has recorded 214 deliveries since 2 March 2026 and needs about 10 minutes of attention a month. Three limits remain after that month of use. Replay rebuilds headers from a template, so header-level bugs still need the tunnel and a real sender.

Bodies over 64 KB get dropped, which has cost me 2 deliveries so far. The local port has no auth, so it stays bound to 127.0.0.1. A watch mode that tails new deliveries in the terminal is half-built, and I use it maybe once a week.

The arc of the project is short: store first, judge later. Console output answered what a delivery looked like, and the stored rows answer what actually happened. I'll write about replaying whole event chains in a future post. If you want to follow along, don't forget to subscribe.
