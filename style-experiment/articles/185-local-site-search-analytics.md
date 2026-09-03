# Adding Privacy-Preserving Search Analytics to a Blog

This synthetic style exercise follows a fictional blog project with invented numbers and dates. Last May I added search analytics to a static blog with 1,240 posts. No detail here describes real events or real visitor data.

The blog serves 8,400 searches per month through a small FastAPI endpoint. I had stored no queries before May and I knew nothing about dead ends.

The request asked for events, aggregation, retention and zero-result reports in one build. I wanted those answers without cookies or personal identifiers in storage.

In this post, I'll share:

- how I log search events safely
- how I aggregate counts each day
- how I enforce retention limits
- how I surface zero-result queries
- what thirty days of data showed

## Events I Collect Without Cookies

I started with three fields pulled from each request with IP addresses dropped. Each event keeps a timestamp, the query text and the result count.

I keep events in SQLite and I append them from the FastAPI handler. CountKit, a small Python module that batches event writes, sits beside the app.

I chose SQLite because I know it well enough to query at midnight without extra tools. The downside is manual vacuuming, and that trade has stayed manageable for 8,400 rows.

I counted 276 searches per day early and I grouped them by length and result count. That manual tally took 38 minutes and it forced me to see empty queries.

I split the traffic across three groups I checked in May:

- queries with one or two words
- queries with three or more words
- empty submits from misclicks

I kept all 8,400 events so the first month stays complete for review.

One event looks like this inside the plain log file:

```text
ts: 2026-05-04T10:12:44
q: celery retry delay
hits: 6
```

I don't trust memory so I reread that log before every single deploy.

## Daily Aggregation Keeps Counts Small

I roll 276 daily events into 40 summary rows with a small midnight script. The job counts queries, groups near duplicates and stores medians.

The top 20 queries cover setup, deploy steps and beta config for the blog. At full size those rows fill 18 kilobytes with indexes included.

The next group holds long tail queries seen once or twice on Linux guides. Its total came to 620 rows per month, which stays tiny without extra servers.

I chose midnight runs because I pay for a small VPS and idle time costs little. The downside is late dashboards, and I accepted a six hour delay.

The midnight job writes four summaries I read in May:

- top queries by count and hits
- zero-result queries sorted by frequency
- median latency by hour block
- error counts by endpoint path

I don't store raw queries after aggregation trims personal fragments.

I run aggregation with one short command before every review:

```bash
uv run python scripts/rollup_search.py --db blog.db --date 2026-05-04
```

That command writes summary rows so I can read trends without scanning raw events.

## Retention Rules Delete Old Rows

I set a 30 day limit on raw events and I keep summaries for twelve months. The old drafts kept everything where disk use grew without bound.

Both disk scares came from log files kept past 90 days with no purge job. I had ignored the cron error in review, which turned out to be a mistake.

The rule I took from it: deletes need scheduled runs before any storage promise. I keep the purge log in Git so I can confirm old rows disappear on time.

I chose cron because I already use it for backups and it runs reliably. The downside is silent failures, and I send output to a monitored mailbox.

The 30 day window passed three checks in the May sample:

- raw events older than limit removed
- summaries kept with monthly totals intact
- disk use flat across four weeks

I added size alerts for each table and the line stayed flat.

I purge old rows with one repeatable pass each night:

```bash
uv run python scripts/purge_search.py --db blog.db --keep-days 30
```

That output lists deleted counts first so I see scope without opening the database.

## Zero Result Reports Guide Fixes

I tried to fix 34 zero-result queries from the first two weeks of May. The phrases had typos, the index lacked synonyms and four posts missed tags.

I recorded the fixes and I kept before photos of each search page for reference. A synonym map fixed eleven cases, yet nine still needed new redirects.

I watch miss rates and click paths during reviews with Grafana charts. I skipped the synonym test once on a Friday deploy, which turned out to be a mistake.

The rule I took from it: misses stay reviewed before any index tuning pass. I chose manual review because I can judge intent in seconds from query text.

The downside is slow triage, and I document each decision in the weekly notes.

The remaining nine share four traits I use in June:

- model names typed without version numbers
- error strings pasted with extra punctuation
- posts tagged with narrow labels only
- queries mixing two topics in one query

I rehearsed the fix flow in staging and the full pass took 74 seconds. The evening run felt calm - the report removed guesswork under time pressure.

## Lessons From Thirty Days Live

The month logged 8,412 searches and it flagged 214 zero-result phrases. Those numbers matter less than the 34 fixes that cut misses by half.

I don't log full addresses now and I keep raw text for thirty days only. That limit caught one late privacy review question in May logs.

I chose short retention because I run the blog alone without legal review help. The downside is thinner history, and that limit has saved two disclosure scares.

I'll keep the daily rollup and I'll refresh synonyms with fresh misses each week. I'll write about the next month after one more index rebuild. If you want to follow along, don't forget to subscribe.
