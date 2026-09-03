# Using Blog Search Queries to Find Missing Articles

This synthetic style exercise describes a fictional blog audit with invented queries and counts. All names, dates and numbers below are fictional, and no real events are reported.

Last March I ran a data blog with 190 published posts and about 24,000 visits per month. Site search handled 1,900 queries monthly, and 340 of them returned zero results. I suspected those dead ends marked articles I should have written.

I first guessed missing topics from comments and email replies. That approach surfaced loud requests from a few readers while missing quiet searches from hundreds, and my next three posts drew below-average traffic. After the third miss I stopped guessing and read the query log directly.

The log produced six article topics in one afternoon. Four of those posts now rank among my 20 most-visited pages, and zero-result searches fell from 340 to 190 per month. The method needs only the log export plus a spreadsheet.

In this post, I'll share:

- how I pull query logs and count zero-result terms
- how I group raw queries into topic clusters
- why my first comment-based guesses missed
- how I pick which gaps to write first
- what the audit changed and what stayed unresolved

## Query Logs And Zero-Result Terms

The blog platform exports one CSV row per search with the query text and the result count. I downloaded the February export on a Monday and found 1,900 rows with timestamps. Each row held the raw query, the result count and the visitor country.

I loaded the export into SQLite and counted exact repeats first. QueryLens, a small Python script that tallies searches, printed the top 50 queries with their result counts. The top 50 covered 720 searches, which is more than a third of the monthly total.

Zero-result terms clustered harder than I expected. The top 20 dead ends accounted for 210 of the 340 empty searches, and most repeated weekly. I exported those 20 terms with counts into a work sheet:

```text
csv merge large files - 34 searches, 0 results
agent eval checklist - 28 searches, 0 results
postgres partition guide - 22 searches, 0 results
```

I keep the raw log for three months so seasonal queries stay visible. February emphasized partitioning and evaluations, while December had emphasized gift-guide style roundups. One month alone would have hidden that rhythm.

## Grouping Raw Queries Into Clusters

Exact counts miss spelling variants, so I grouped queries by shared stems within each week. I lowercased every query, stripped plurals and merged rows sharing two or more content words. A cluster counted when it reached five or more searches in one month.

The clusters exposed six gaps with steady volume across February and March:

- merging large CSV files without memory errors
- checklists for evaluating coding agents
- partitioning guides for small Postgres tables
- reading server logs for daily review
- photo galleries for workshop recaps
- routing feature requests into issues

Three clusters mapped to posts I had planned but never written, and three were new to me. The CSV cluster alone held 61 searches across spelling variants, which exact matching had split into nine separate rows.

I ran the grouping with one command:

```bash
uv run python scripts/cluster_queries.py --input february.csv --min 5
```

The command reads the export, normalizes text and writes one JSON file with clusters and counts. It links three example queries per cluster for manual review. The full run takes about 40 seconds on my laptop.

## Guesswork Before Evidence

My earlier topic picks came from 14 reader emails and 22 comments. Those messages asked for advanced agent research and career advice, so I wrote three posts on those themes. Each drew 300 to 500 views against a site average of 1,100 views per post.

The log showed why those posts missed. Advanced research drew 12 searches total in February, while CSV merging drew 61 searches. I had written for the readers who write emails and ignored the readers who only search.

The rule I took from those misses: emails show intensity, and only logs show breadth.

The April picks tested the rule directly. I wrote the CSV merging guide and the agent eval checklist from the top two clusters. Those posts drew 2,400 and 1,900 views in their first month, which beat all three guesswork posts combined. Evidence replaced inbox sampling from that month on.

## Picking Gaps To Write First

Six gaps exceed my writing capacity for one month, so I score each cluster before drafting. The score adds monthly searches, documentation fit and drafting effort into one number. High searches with low effort come first, and low searches with high effort wait.

I scored the March clusters in a work sheet with one row per gap. The sheet records searches, competing posts and an effort estimate in hours:

```bash
uv run python scripts/score_gaps.py --clusters clusters.json
```

The command prints each cluster with its score and the deciding factor. CSV merging scored first with 61 searches and four estimated hours, while partitioning scored second with 44 searches and five hours. Career topics from email scored last with 12 searches and eight hours.

I publish two gap posts per month and keep the rest queued. The queue holds four clusters now, and I re-score it monthly because search volume shifts. One gallery cluster faded from 30 to 9 searches after a workshop season ended.

## Keeping The Working Parts

The audit now runs in about two hours per month. Export and clustering take 20 minutes, manual review takes an hour and scoring takes the rest. Zero-result searches fell from 340 to 190 monthly, and four gap posts sit among my 20 most-visited pages.

The work taught me a narrower lesson than "listen to readers". Loud readers describe what they want, quiet searches describe what many need and only counts separate the two. I now check the log before approving any new topic.

Gaps remain around ambiguous queries and external search. Short queries like "evals" could mean many things, and Google traffic never reaches my log. My next addition joins the site log against referral data for one quarter.

I'll write about that joined audit in a future post. If you want to follow along, don't forget to subscribe.
