# Writing Smoke Tests for Semantic Search

I wrote this guide as a synthetic style exercise, and all product details are fictional. In April 2026, I added smoke tests to Fieldnotes, a fictional documentation-search service. The tests came after a model upgrade returned confident answers from the wrong product.

The index held 18,400 documents. Search looked fine in casual use, and that was the problem.

In this post, I'll share:

- why manual queries missed the failure
- how I choose canary queries
- how I define expected neighbors
- how I set a latency budget
- how the tests run in CI

## Manual Queries Missed It

The failure appeared during a routine upgrade from embedding model version 4 to version 5. A query for "delete a member" retrieved a marketing page about adding members before the actual permission guide.

The ranking was plausible because both pages used similar words, and the marketing page had a strong title. A human skimming five results could easily accept the first answer.

My first review used ten favorite queries. Nine looked acceptable, so I nearly shipped the new index. The tenth exposed the failure only because a support ticket had mentioned the exact permission name.

I sampled where search already worked, and that was my mistake. The rule I took from it says semantic search needs fixed tests for known regressions, just like an API.

Manual browsing remains useful for tone and relevance. It can't prove that an upgrade preserved the behavior your support team depends on.

## Choose Canary Queries

The test set starts with support tickets, onboarding questions, and old search queries. I now pick 40 canary queries from four sources.

Ten come from the ten most frequent support questions. Ten come from exact feature names that must retrieve the reference documentation. Ten are paraphrases written by two support engineers. The last ten are known confusing cases collected during development.

Each canary has a stable ID, query text, expected document IDs, and a pass rule. The metadata lives in `tests/search/canaries.yaml`.

For Fieldnotes, one entry looks like this:

```yaml
- id: perm-delete-member-001
  query: remove someone from workspace
  must_include: [permissions/delete-member]
  may_include: [workspaces/invite-members]
  pass: first
```

The first rule says `permissions/delete-member` has to appear first. The may-include entry allows a related invite page in the top five, because users often compare the two operations.

I avoid a test set made entirely from obvious titles. Eleven canaries intentionally contain typos, abbreviations, product synonyms, or two-language fragments. Three contain negations such as "without connecting a database".

## Define Expected Neighbors

Every query needs a concrete pass rule because "results look relevant" isn't a test.

For 28 canaries, one document must rank first. For 8 multi-intent queries, two documents must appear in the top three. For 4 navigation queries, any page inside a section is acceptable because the index contains several equivalent pages.

The scorer reports these three numbers:

- first-result accuracy
- top-five recall
- the mean rank of the first required document

The command prints the three aggregates in this format:

```text
first_result_accuracy: 0.925
top5_recall: 0.975
mean_first_required_rank: 1.38
```

Those aggregate numbers are useful, but the test fails on individual canaries. A service can average well and still ruin one support workflow.

Neighbor assertions also protect against accidental duplication. In Fieldnotes, two deployment guides had 94% overlapping text, and the test required the current guide to outrank the archived guide for every deployment query. That exposed stale documents the content team had forgotten.

I keep expected IDs in version control next to the service. When a document intentionally moves, the same pull request updates the canary and explains why.

## Set a Latency Budget

A relevant result that arrives after a user leaves is still a failure, so each smoke run measures latency against the production index.

The service has a p50 target of 180 milliseconds and a p95 target of 450 milliseconds for the complete query path. The smoke test reports the embedding call, the vector search, and the re-ranking step separately.

A recent run looked like this:

```text
embed: p50 61ms, p95 143ms
search: p50 22ms, p95 78ms
rerank: p50 49ms, p95 151ms
total: p50 138ms, p95 417ms
```

The test fails when p95 crosses 500 milliseconds over two consecutive runs. One slow run stays visible but doesn't block the release, because shared hardware produces occasional noise.

Latency also participates in model choice. Version 5 improved first-result accuracy from 88% to 93%, but its embedding call added 47 milliseconds at p95. We accepted the slower embedding call after testing it against the budget.

## Run in CI

The smoke suite runs on every pull request that changes the embedding model, retrieval code, or the index. A full rebuild takes 14 minutes, so ordinary content edits run a 12-query subset.

The workflow has four steps, and it never writes to production:

- build a temporary index
- run canaries
- compare scores with the current release
- upload a JSON report

The report lists each failed query, the returned ranks, the expected IDs, and the embedding model versions. Reviewers can see whether one document changed or the entire ordering drifted.

```bash
pytest tests/search --canary-set full --report artifacts/search-report.json
```

When the test fails, the report becomes the review artifact. In the model-upgrade incident, 3 of 40 canaries failed. Two had the same cause: the permission guide had lost its exact phrase "delete member" during a rewrite.

We made an editorial change instead of changing the algorithm. After the phrase returned, the full suite passed and the aggregate score improved by 4 percentage points.

The suite isn't a full evaluation. It doesn't prove user satisfaction, and 40 canaries can't cover 18,400 documents. It does catch the regressions most likely to reach support.

## Lessons

Semantic search behaves like any other interface once you name the expected outcome. Choosing queries that represent real tasks takes the most work, and each query needs a definition of "correct".

My current rule is to add a canary whenever a support ticket reveals a confusing result. The test set then grows from failures rather than from invented examples.

I plan to write more about the JSON report and the document-overlap audit. Subscribe if you want the next article in this search-testing series.
