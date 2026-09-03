# Profiling Latency Across an AI Application

I wrote this synthetic style exercise as a build log, and the application and all numbers in it are fictional. DocAnswer, my retrieval bot for a 900-page product documentation set, drew eleven "slow" complaints in the May 2026 feedback form. My only measurement was the average response time, 2.4 seconds, and that average told me nothing useful.

I first optimized the wrong thing. The model call looked expensive, so I switched to a smaller model in early June, and the complaints kept coming. The average had blended a 0.3-second happy path with multi-second tail requests, and I had polished the happy path twice.

The rule I took from that month: look at the tail before you optimize anything.

In this post, I'll share:

- how I split a request into timed stages
- how I pulled percentiles out of plain logs
- which stage owned the tail latency
- which changes moved the numbers
- what the profile still misses

## The Average That Hid The Tail

The app serves one endpoint that takes a question and returns an answer with citations. Between the question and the answer sit an embedding call, a vector search over 40,000 chunks, a rerank step and a generation call. None of them reported timing separately. The four calls ran in sequence, which made the stage boundaries easy to draw.

DocAnswer has served one internal team of about 60 employees since November 2025, so the traffic is modest. Even with modest traffic, the feedback form reaches me, and a slow answer wastes a minute of someone's workday.

In June I added stage timing around each of the four calls. A wrapper records the start and end of every stage, then appends one JSON line per request.

The middleware is about 40 lines:

```python
@app.middleware("http")
async def time_stages(request, call_next):
    stages = StageTimer()
    request.state.stages = stages
    response = await call_next(request)
    stages.write_line(request.state.query_id)
    return response
```

`StageTimer` is a small class that wraps each stage call and collects durations. Every line in `timing.jsonl` holds the query id, the stage name, and the duration in milliseconds. The log rotates weekly and costs about 2 MB of disk per month.

## Percentiles From The Logs

Averages hide tails, so a 30-line pandas script computes percentiles per stage every night. A week of traffic came to about 3,000 requests, which is enough for stable p95 numbers.

The choice of p95 came from the first plot I made. The top 5% of June requests took over three seconds, and those were the people writing feedback.

The first full week of numbers looked like this:

- embed question: 90 ms at p95
- vector search: 120 ms at p95
- rerank: 1,400 ms at p95
- generation: 2,100 ms at p95

The median request took 1.1 seconds end to end, and the p95 request took 3.7 seconds. The reranker, which I had added in February for answer quality, owned nearly 40% of the tail. The per-stage lines also changed how I handle reports. When someone writes in now, I ask for the minute it happened and read that request's line in the log.

## Two Fixes That Moved The Numbers

The first fix targeted the rerank stage. I had been reranking 50 candidate chunks per query, and the reranker's cost grew with that number. Cutting candidates to 20 dropped rerank p95 from 1,400 to 520 ms, and my monthly answer-quality checks stayed flat. The candidate cut needed that quality check, because rerank cost and rerank quality travel together.

The second fix removed repeated embedding work. About 30% of daily questions repeated an earlier question almost word for word, so I added a small cache keyed on the normalized question text. The cache removed about 110 ms from those requests and cost one Redis round trip.

Both fixes shipped a week apart, and each one moved exactly one line in the table. Together they brought p95 latency from 3.7 to 2.2 seconds, and the median barely moved. The August feedback form had two "slow" complaints, down from eleven in May. I also reverted the smaller model from June, since the profile showed generation was never the problem.

## Limits After The Fixes

The profile covers the server and says nothing about the client's network time, which the logs can't see. A client-side timer would close that gap, and it stays on the list for the next iteration. Cold starts still spike past five seconds when the vector index reloads, and those spikes live in the p99 line I now watch daily. The stage wrapper also adds about four milliseconds per request, a cost I accept for the numbers.

Generation p95 sits at 2,100 ms and now dominates the remaining tail. I have ideas about it, and none of them are measured yet.

## One Profile Later

Two months after the first numbers arrived, the app answers p95 requests in 2.2 seconds instead of 3.7. The eleven complaints became two, and every remaining complaint now comes with a stage attached to it.

The deeper change sits in my habits. I read percentiles before features, and every new stage ships with timing from its first commit. The timing middleware graduated from a side experiment to a shared internal library in July. The 2.4-second average I trusted for months is gone from my dashboards entirely.

I'll write about the cold-start spikes in the p99 line in a future post. If you want to follow along, don't forget to subscribe.
