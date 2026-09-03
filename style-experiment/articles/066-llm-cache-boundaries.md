# Caching LLM Responses Without Creating Stale Answers

In February, a fictional documentation bot served 3,410 answers in one week, and its cache saved $61 in model costs. That looked good until a customer received a policy answer written before a February 18 price change. I spent the next two days deciding what should be cached and what should always be fresh.

The traffic, costs, and policy change are invented for a synthetic style exercise. The design problem is ordinary: caching deterministic work is useful, while answers tied to changing source documents need a visible freshness rule.

In this post, I'll explain the boundaries I set:

- why the first whole-response cache failed
- how I grouped requests by stable inputs
- where caching retrieval results stayed safe
- how freshness metadata reaches the response
- how I validate the cache and monitor misses

## The whole-response cache failed

The first implementation treated the user question plus model name as the cache key. That was easy to add, and it produced a 38 percent hit rate during the first week. It also hid two distinct problems.

First, two questions with different intentions could use nearly identical wording. A cached answer about "current plans" was reused for a question about legacy plans. Second, retrieved source chunks changed when the documentation changed, so the old answer no longer had a source.

I reviewed 80 sampled cache hits and found 9 misleading answers. Six were outdated, while 2 mixed contexts from different pages and 1 repeated a customer's account phrase from an earlier prompt. The rule I took from that review is to avoid full-response caching unless every changing input is part of the key. It's also important to record why an answer became stale.

## Key on stable inputs

I replaced the simple key with four fields:

- normalized user question
- model name and model settings
- retrieval index version
- source document version

Normalization removes greetings, obvious duplicates, and extra punctuation, but it doesn't remove dates or plan names. The cache stores a hash of those fields in `cache/responses.sqlite`, alongside the answer and the source IDs used to generate it.

The index version matters more than the model name in this application. When the retrieval index rebuilds, old cached answers may still describe deleted pages. A new index version makes those answers unreachable without deleting them immediately.

I also separated user-specific data from public documentation. Public questions can share cache entries, while account questions include a customer ID in the key. They still skip the cache for billing details, and the extra cost is easier to accept than a wrong private answer. The extra cost is easier to accept than a wrong private answer.

## Cache retrieval separately

The next version cached intermediate retrieval results rather than complete responses. A retrieval cache key contains the query, index version, filter set, and top-k setting. This is safer because the model still sees the current prompt instructions and can produce a response from those retrieved chunks.

The hit rate dropped to 24 percent, while the misleading samples dropped to one in 80. That one case used a page whose title stayed the same after the content changed. Adding the document version to the retrieval key fixed it.

Retrieval caching saves latency as much as money. In the fictional measurements, a cached lookup returned in 18 milliseconds, while a fresh lookup averaged 140 milliseconds. A model response still dominated total latency, but faster retrieval made retries and evaluation runs cheaper.

I kept one exception for pages under active review. If a document has a `review_until` field in the future, retrieval skips the cache and reads the current source. Editors can therefore push a correction without waiting for cache expiry.

## Expose freshness

Every response now includes a small metadata object, and the UI renders its freshness field rather than hiding the date in logs:

```json
{
  "answer_id": "a-88231",
  "cache": "retrieval-hit",
  "source_versions": ["pricing@2026-02-18", "faq@2026-02-20"],
  "freshness": "2026-02-20"
}
```

I set the freshness date to the newest version date among the cited sources. If the sources disagree, the response says so and shows both dates. That sounds noisy, but it gives a reviewer an immediate reason to distrust an old answer.

For cached whole responses, the UI adds a stronger label. It shows the date the answer was generated and offers a "check current sources" action. That action bypasses the cache and records the fact that a user needed a fresh result.

I don't expose raw cache keys because they include account IDs. The metadata only shows whether the answer came from a retrieval hit, a response hit, or a fresh model call.

## Validate and monitor

The cache has its own test set of 60 fictional question-and-source pairs in `tests/cache_cases.yaml`. For each case, the expected behavior names whether a retrieval hit is valid, a response hit is valid, or a fresh call is required.

These cases cover the boundaries:

- identical wording with different plan names
- a source update without a title change
- a user-specific account question
- a future review window
- a request after an index rebuild

The suite runs after each cache change and before deployment, and it caught three regressions during this exercise. One regression removed the phrase "legacy plan" because normalization treated the word "plan" as a stop term.

Monitoring tracks retrieval hit, response hit, cache bypass, and user-requested refresh rates. When the refresh rate rises above 2 percent, I review those questions and their source versions. Rising refreshes usually mean the content is stale before the cache is wrong.

## Current boundary

Caching is safe when the input and source versions fully determine the output, and visible when users need to know the answer's age. It becomes unsafe when a hidden input changes or when the cache makes a source disappear from view.

The current split costs more than the first version. Weekly savings fell from $61 to $38, while misleading answers in the sample fell from 9 to zero. For this fictional support bot, that tradeoff is easy to justify.

The design rule is also useful beyond caching. Make every input that can affect an answer explicit, then decide which of those inputs can be reused safely. If I continue this exercise, I'll add versioned prompts to the same cache key model. Subscribe if you want that follow-up.
