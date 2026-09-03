# Reducing Latency in a Writing Assistant

For eight months I've used a Telegram bot that turns rough notes into article
outlines. In March, the median wait was 14.6 seconds, and 11% of requests hit a
90-second timeout. I spent two weeks measuring the delays before changing the
model. I wrote this synthetic style exercise with invented timings, costs, and
project names.

The assistant accepts a voice note or a paragraph of text, retrieves three
related drafts, and returns an outline with evidence links. Users don't mind a
useful 15-second answer. They abandon a silent minute.

In this post, I'll share:

- how I broke the wait into stages,
- how queueing changed perceived speed,
- why streaming helped the most,
- how caching reduced repeated work,
- what I still measure every week.

## Instrument the request path

My first fix attempt was a mistake. I switched to a faster model and median time
fell to 11.8 seconds, but users said the assistant felt slower. It returned a
blank chat for longer before the complete answer appeared.

So I added request IDs and timestamps to each processing stage:

- transcription
- retrieval
- model call
- formatting
- Telegram delivery

The events go into SQLite, and a small script prints percentiles for each stage.

The breakdown explained the contradiction:

- transcription: 2.1 seconds,
- retrieval: 0.4 seconds,
- model call: 8.9 seconds,
- formatting: 0.3 seconds,
- delivery: 0.7 seconds.

The remaining 2 seconds came from queueing during bursts.

I also recorded failure classes. Nine of eleven timeouts came from voice notes
longer than five minutes. One came from a Telegram retry after a network error.
The last one was an actual model timeout.

## Acknowledge and queue

The bot previously processed one request at a time. During a workshop, 14 people
sent notes within 40 seconds. Each person saw nothing while earlier notes moved
through the pipeline.

I added a simple job table to SQLite. When a request enters, the bot sends
`Received - I'll send the outline in about 20 seconds.` and stores the job. A
worker takes jobs in submission order and updates the status.

The estimated wait comes from the median duration and the number of jobs ahead.
It was accurate for 87% of March requests. When a voice note exceeds five
minutes, the estimate now says 40 to 90 seconds.

The perceived speed improved immediately. The support message "it seems stuck"
disappeared from April feedback, even though the median end-to-end time only
improved to 13.9 seconds. Acknowledgment changed the experience more than the
small performance gain.

## Stream the useful part

The biggest win came from changing the output order. The old prompt asked for a
complete JSON response, so formatting could begin only after the model produced
the final brace. The user waited through every word before seeing any text.

I split the response into two processing calls. First, the model streams the
three main claims as plain lines. Second, a shorter call turns each claim into
outline items and attaches source IDs. The first call can start rendering while
the second call runs.

Now the bot edits one Telegram message every 400 milliseconds:

```text
Draft outline
1. State the problem in the reader's workflow
2. Show the first failed attempt
3. Explain the replacement
...
```

First visible text dropped from 11.1 seconds to 2.8 seconds at the median. The
final answer still arrives around 12.5 seconds. Users gain time to decide
whether the direction is wrong, and they can stop the job before it finishes.

The split added a consistency risk. A claim may use one phrase in the preview
and a slightly different phrase in the final outline. I accepted that tradeoff
because the preview is explicitly a draft.

## Cache carefully

The same 20 drafts produced 31% of May requests. Most were minor edits to
punctuation, title length, or bullet order. The retrieval results were already
identical, so the model repeated work.

I added a cache key from three inputs:

- normalized text,
- retrieval result IDs,
- the prompt version.

The normalized text lowercases whitespace differences and strips trailing
punctuation. A cache hit returns the prior outline and marks the message as
cached.

In the first week, 214 of 692 requests hit the cache. Median time for those
requests fell to 0.8 seconds, and model cost fell from $21.40 to $15.10 per
week. Fresh requests cost the same as before.

The cache misses on a prompt change, so I don't serve obsolete instructions.
It also stores only outlines, never raw voice audio. Entries expire after 30
days because old drafts change as the corpus grows.

I don't cache transcription because a person may rerecord a note with the same
length but different words. Transcription is only 2.1 seconds, so saving that
small stage isn't worth the risk of returning the wrong text.

## Watch the weekly numbers

Every Monday, I run a 20-minute review. The report shows median and 90th
percentile latency, cache hit rate, timeout count, and the five slowest request
IDs. Each slow request links to its stage timings.

The current numbers look like this:

- median first visible text: 2.9 seconds,
- median final outline: 12.2 seconds,
- weekly cache hit rate: 27% to 34%,
- timeouts: 4 per 1,000 requests.

The remaining timeouts are mostly 8-minute recordings. I now ask for
confirmation before transcribing anything longer than five minutes. That step
adds friction in a rare case and prevents a minute of wasted work.

I also keep a sample of 25 user-rated answers. Fast answers don't excuse a wrong
outline, so quality remains part of the same review. In June, 21 samples were
acceptable, 3 needed an extra source, and 1 confused two drafts.

## Closing note

Latency is a product decision as much as a systems problem. Splitting the model
call and showing a partial draft did more for the assistant than the model swap.
The queue message made the remaining wait tolerable.

The rule I took from the work: measure each stage before optimizing the whole
path. I plan to apply the same request IDs to the course-question assistant this
summer. Subscribe if you want the follow-up.
