# Adding Rate Limits to a Personal API

I run a small fictional reading API called ShelfIndex for the members of a book club. It exposes search, reading history and private notes through FastAPI. During a June test session, one browser tab retried failed requests so aggressively that the database connection pool filled up.

I wrote this synthetic style exercise for a writing project, so the users, incidents, timings and costs are fictional.

In this post, I'll share:

- how I chose the first quota
- where I enforced the key and quota checks
- how I made failures safe for clients
- how the queue absorbs bursts
- what changed in the API after five weeks

## The First Quota

The API had 34 user keys. A dashboard might send 12 requests when a reader opens it, while an import job might send 400 requests over two minutes. I wanted to protect the database without making normal use feel slow.

I measured traffic for ten days before choosing a number. The 95th percentile user made 2,180 requests per day, while one cron job made 6,400 requests in a short burst. Median latency was 84 milliseconds, and the PostgreSQL pool had 20 connections.

The initial quota was deliberately conservative:

- 300 requests per minute for ordinary keys
- 1,500 requests per minute for the import key
- 20 concurrent requests per key

Those numbers covered 31 of 34 keys on their busiest day. The three exceptions were two import jobs and a backup script that I later gave their own queue.

## Key and Quota Checks

I put a middleware (code that runs before every request handler) in the FastAPI application. It reads the `Authorization` header, looks up the active key in PostgreSQL and rejects unknown or disabled keys before touching the main query.

For quotas, I chose Redis with two sorted sets. One set records request timestamps for each key, while the other records concurrent requests. Using Redis kept the counters consistent when the API ran in two containers, and the extra hop added about 3 milliseconds at the 95th percentile.

The check follows five steps:

- reject a missing or unknown key
- count the current concurrent requests
- count requests in the last minute
- reserve a database connection only after both checks pass
- release the reservation in a request finally block

My first version reserved the database connection before the Redis calls. It passed every local test, but it held scarce resources while Redis was down. The fix moved reservation later and made dependency failure explicit.

## Safe Error Messages

The initial response was a plain 500 status with no headers. A client couldn't distinguish an exhausted quota from a broken query, so it retried and made the situation worse. I replaced it with 429 and structured JSON.

The response body now has these fields:

```json
{
  "error": "rate_limit_exceeded",
  "limit": 300,
  "window_seconds": 60,
  "retry_after_seconds": 23
}
```

I also return headers named `Retry-After`, `X-RateLimit-Limit` and `X-RateLimit-Remaining`. A small header is easier for generic HTTP clients to consume than a JSON body, and the body remains useful for our own frontend.

Unknown keys receive 401 with `WWW-Authenticate: Bearer`. The API returns 403 with a short reason for a disabled key. It logs the key identifier but removes the key value, so support can connect a failed request to an account without storing another secret.

For database failures, the API returns 503 and sends `Retry-After: 30`. It doesn't count those requests against the quota, because the client never received the service it requested.

## Queue Bursts

Three legitimate clients needed to synchronize 2,000 records after a outage. Their first run consumed the import quota, and all three backed off at the same time. Retries then synchronized into waves every 30 seconds.

I added a PostgreSQL-backed job table for bulk synchronization. A client submits one job with the user key, requested year and callback URL. A worker processes ten jobs at a time, emits progress to a stream and returns a compressed JSONL file when it finishes.

Bulk requests now follow this sequence:

- the client submits a synchronization job
- the API returns `202 Accepted` and a job identifier
- the client polls at most once every five seconds
- the worker sends one callback when processing completes

Bulk imports dropped from 5,800 interactive requests per run to one job plus 80 polling requests. The total CPU time was similar, but the queue protected the request path during the next import.

## Monitoring and Tests

The dashboard tracks rejected requests, concurrent reservations, queue age and Redis latency. On 12 July, it showed 429 responses rising from 4 to 410 per hour after a frontend release. The release had ignored `Retry-After` and used a fixed one-second retry.

I loaded the same traffic with k6 and confirmed the result. The API stayed under 180 milliseconds at the 95th percentile, while PostgreSQL stayed below 70% of its connection limit. The frontend team then changed their client to use the retry header and exponential backoff.

The automated tests cover four cases:

- an unknown key receives 401
- a rejected quota request receives 429 and a retry time
- Redis failure returns 503 without consuming quota
- two containers agree on a shared counter

Integration tests run Redis and PostgreSQL in Docker Compose. That makes them slower than unit tests, but it caught a transaction mismatch that mocked tests had hidden.

## Current Limits

Five weeks later, the API served 4.1 million requests without a database saturation incident. It rejected less than 0.4% of daily traffic, and ordinary readers rarely hit 300 requests per minute because bulk clients use the queue.

The API now has two clear limitations. A deleted key leaves its sorted-set entries until the nightly cleanup job runs, so the Redis memory graph has small daily spikes. Per-key limits don't protect a shared neighborhood network behind one IPv4 address because the API trusts the key rather than the network address.

I also have no good response for a user who needs 4,000 requests in one minute as a one-off. The practical answer is still to use the queue and accept a completion time measured in minutes.

## Closing Notes

The quota number was the least important decision. Clear state transitions and retry instructions protected the database more than the exact threshold.

The useful rule is to make limits machine-readable. A client that knows when to return will usually cooperate, especially when the bulk path removes repeated synchronous requests.

I'll write more about the synchronization queue in another article. Subscribe to stay updated.
