# Adding Freshness Checks to a Retrieval System

Last April, a support assistant answered a return-policy question with a rule that had changed seven months earlier. I had connected it to an internal warehouse handbook. The retrieval system found the correct document, but it had no way to tell me that the document was stale.

I wrote this as a synthetic style exercise with an invented handbook, dataset, and policy history. I would still reuse the freshness workflow.

In this post, I'll share:

- how I recorded source dates before indexing documents
- how I set an expected update cadence per source
- how I added stale flags to retrieval results
- how I tested the system with date-sensitive questions
- what the first month of monitoring showed

## Capture Source Dates

The handbook had 412 markdown pages in a private repository. Most pages included a "last reviewed" line, but three different formats appeared: `Reviewed: 2025-11-14`, `Updated on 2025/11/14`, and a YAML field named `review_date`.

My first indexing script ignored those lines. I changed it to parse YAML front matter, search the body for review headers, and write a normalization warning when it found neither.

The normalized index gained these fields:

- `source_id`
- `source_modified`
- `review_date`
- `expected_update_days`
- `stale_at`

For pages without any date, I used the Git commit time. That was a conservative fallback, because a formatting change could make an untouched policy look new. I marked fallback dates separately, so I could review them before trusting freshness.

## Set Update Cadence

Treating every page the same was the obvious next mistake. A shipping-address page changes more often than a historical appendix, so one global threshold would produce false alarms or miss real staleness.

I asked the handbook owners to assign an expected update interval to each source.

We used these buckets:

- 30 days for prices and return deadlines
- 90 days for operating procedures
- 180 days for software setup instructions
- 365 days for historical background

The owners marked 54 pages as high-churn, 181 as normal, 122 as stable, and 55 as archival. I wrote those intervals into `sources.yaml` next to each path. The mapping stayed in version control, so a cadence change showed up in a reviewable diff.

The indexer calculated `stale_at` by adding the interval to `review_date`. If the field was missing, it used the Git fallback and reduced the interval by 20% to account for extra uncertainty.

## Flag Stale Results

Next, I changed the retrieval layer. After retrieving ten candidates, it compared today's date with `stale_at` and added a `freshness` field to each result.

The field had these values:

- fresh
- aging
- stale

The API response then looked like this:

```json
{
  "answer": "Returns are accepted within 45 days.",
  "source_id": "returns-policy",
  "source_date": "2025-08-19",
  "freshness": "stale",
  "expected_update_days": 30
}
```

I deliberately left stale answers visible in the first version. In an internal tool, hiding the answer could block someone who needed the surrounding context. The visible flag let a person decide.

For answers assembled from multiple chunks, I used the oldest non-archival source date. That was stricter than an average date and matched the way people treat conflicting rules.

## Test Date-Sensitive Questions

Before turning on monitoring, I built 36 date-sensitive questions from the handbook. Each question had a known policy before the change, the current policy, and the page that stored both versions.

The test runner fixed the system clock and checked three behaviors:

- retrieval returned the governing page
- the API exposed the correct source date
- freshness moved to stale after the cutoff

The first run passed only 21 of 36 cases. Nine failures came from pages that included their policy history inline, so retrieval returned the old paragraph rather than the current summary. The remaining six had missing or malformed dates.

I didn't change the model prompt first. I fixed the source pages by moving old rules into a "History" subsection and putting the current rule at the top. After that, 34 of 36 cases passed.

## Monitor for a Month

The monitoring job ran nightly and produced two reports. The first listed sources that had passed `stale_at`, while the second listed queries whose retrieved context contained stale or aging chunks.

During May 2026, the system handled 1,184 questions.

Freshness flags appeared on 88 answers:

- 61 answers used aging sources
- 27 answers used stale sources
- 19 of the 27 were return-deadline questions

The return-policy page drove most of the risk. Its review date had lagged the actual change by 22 days, and the 30-day cadence started from the review date. We moved policy updates into a pull request template with a required review date, reducing that lag to two days in the next update.

The monthly report also revealed 12 archived pages that were still being retrieved. We added an `archived: true` field and excluded those pages unless the user explicitly searched history.

## Final State

I now store freshness checks with source metadata, retrieval results, and nightly monitoring. The assistant can still answer from an old page, but it can no longer do so invisibly.

I could add a date to the response in a few hours. After that, I had to decide which sources require freshness. I also had to decide who owns that decision and what the system should do when the date is missing.

I plan to describe the nightly report format in a future post. Subscribe for the update.
