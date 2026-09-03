# Controlling the Cost of a Small Vector Search Service

I wrote this synthetic style exercise as a build log. The project, dates and measurements are fictional. In April my vector search demo burned 38 dollars in API embedding charges in a single week.

The demo served 400 queries a day against 60,000 support articles. Each query embedded its text remotely, each new article embedded on arrival, and nobody watched the meter until the invoice arrived.

In this post, I'll share:

- where the embedding budget went
- how I cache query vectors
- how I batch document ingestion
- how I set retention rules for stale vectors
- what the service costs today

## Thirty-Eight Dollars For A Demo

The April setup embedded everything through a paid API at 13 cents per thousand tokens. Support articles averaged 900 tokens each, and the initial backfill alone processed 54 million tokens.

Query traffic added a steady daily charge on top. Each of the 400 daily queries embedded 40 tokens of input, and the weekly query total reached a cost I had never estimated.

The rule I took from April is simple. I measure embedding spend per thousand queries before I optimize anything, and I keep that number visible in the repo README.

## The First Version

My first fix switched the embedding model to a cheaper tier without changing anything else. The per-token price dropped by half, and the weekly bill dropped from 38 to 21 dollars.

That saving felt good for exactly one invoice cycle. Traffic doubled in May when two teammates demoed the service in workshops, and the bill climbed past the April number on the cheaper tier.

Cheaper unit prices never fix unbounded usage. The service embedded every query fresh, re-embedded unchanged articles nightly, and stored vectors nobody ever retrieved.

I kept the cheaper tier and attacked the volume instead. Three changes cut usage by 90 percent while traffic kept growing.

## Caching Query Vectors

Workshop demos repeat the same questions, so I cache query embeddings by normalized text. The cache key lowercases the query, strips punctuation and collapses whitespace before hashing.

The cache lives in Redis with a 30-day expiry:

```bash
redis-cli --raw hget query_vectors "what is the refund window"
```

That lookup takes 2 milliseconds against 400 milliseconds for a fresh embedding call. The May hit rate reached 61 percent, since demos and tests repeat a small question set.

Cache misses still call the API, and I log every miss with its cost. The miss log showed that 15 long-tail questions caused half the remaining spend, so those answers moved into a static FAQ file.

## Batching Document Ingestion

New articles arrived one at a time through a webhook, and each arrival triggered its own embedding call. The per-call overhead exceeded the token cost for short articles under 200 tokens.

I replaced the webhook handler with a queue and a ten-minute batch timer. The timer collects arrivals, concatenates them into one request and splits the returned vectors back to articles.

The batching worker runs as one script:

```python
def flush_queue(queue):
    texts = [item.text for item in queue]
    vectors = embed_batch(texts)
    return dict(zip(queue, vectors))
```

That change cut ingestion calls from 900 per week to 90. The ten-minute delay never mattered, since the search UI refreshes its index on the same schedule.

I also stopped re-embedding unchanged articles entirely. The nightly job now compares content hashes first, and it skips every article whose hash matches the stored vector.

## Retention Rules For Stale Vectors

The index had grown to 60,000 vectors including three years of outdated articles. Each stored vector costs a fraction of a cent monthly, and the fractions added up to nine dollars of the April bill.

I wrote retention rules with the support team in one sitting. Articles older than 18 months without a single retrieval leave the index, and seasonal articles leave after their quarter ends.

The cleanup script runs monthly and reports before deleting:

```bash
uv run python scripts/prune_vectors.py --older-than 540 --dry-run
```

That script flagged 19,000 vectors in June, and the support lead approved 17,000 deletions. The index shrank by 28 percent with zero complaints over the following month.

I keep deleted vectors restorable for 90 days from a cold archive. I have restored exactly four articles since June, and each restore took one command and two minutes.

## Four Dollars A Week

The service now costs about four dollars weekly at triple the April traffic. Caching removed the repeated query spend, batching removed the ingestion overhead, and retention removed the storage drift. The index now grows only with content that earns retrievals.

I pull the cost dashboard daily from the provider invoice API. I review it on Mondays with the other infra numbers, and I investigate any week above six dollars. Workshop demos pushed one June week to nine dollars, and I traced the overrun to uncached demo questions within an hour.

Two habits keep the number flat as usage grows:

- every new feature estimates its embedding cost before merging
- the monthly prune runs on the first Monday without fail

New teammates learn the budget from the README badge first. I publish last week's spend per thousand queries as a README badge with a link to the dashboard.

I'll cover the cache-invalidation rules in detail in a future post. If you want to follow along, don't forget to subscribe.
