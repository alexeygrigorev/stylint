# Creating a Private Benchmark Set for My Own Tools

For this synthetic style exercise, the projects, files, and measurements are invented. In January 2026 I built three small search utilities and liked each one. Then I tried to explain which one a friend should use, and I had no evidence beyond my impression. That conversation became a private benchmark of 82 everyday queries.

In this post, I'll share:

- where the queries came from
- how I labeled results without turning it into a research project
- why every tool got the same plain baseline
- what the first run actually showed
- how I keep the set from going stale

## Collecting real queries

I started with a text file and captured searches during normal work. The first 20 entries came from notes about teaching. Other searches covered travel, invoices, AWS credentials and course exercises. I kept the original wording, including fragments such as "lambda temporary credentials sdk".

After two weeks I had 82 queries. Forty-one came from my own notes, 23 from my course forum archive, and 18 from a second browser profile dedicated to side projects. I discarded 14 candidates because they depended on a file that no longer existed or asked about a one-time event.

The point was representativeness, not size. Each query had to resemble something I would type again, so notes and forum searches dominated the pool.

I stored one JSONL record for every query:

```json
{"id": "aws-lambda-credentials-01", "query": "lambda temporary credentials sdk", "answer_paths": ["notes/aws/lambda.md"], "source": "own-notes"}
```

The identifier made it easy to compare runs without exposing the corpus. The `answer_paths` field accepted one path or several, and `source` recorded where the query originated. That structure was dull on purpose, and it stayed readable with only a text editor.

## Labels and pass rules

For every query I selected a small answer pool. Most had a single correct file, while some had three acceptable files. When I searched for a course deadline, the syllabus and an announcement could both help, so I marked those cases as "any of the following".

I used two simple metrics. Hit rate meant at least one acceptable item appeared in the top five. Mean reciprocal rank meant the best item got a score based on its position. I also wrote a note whenever no result should have matched.

The labels were my judgments, so they aren't universal truth. They're acceptable for a personal benchmark. Its job is to compare tools on my material and surface regressions before I switch.

## The baseline

Every candidate competed against a 70-line keyword baseline built with Python's standard library. It lowercased text, split on nonword characters, removed a tiny stopword list, and added a small boost when all query terms appeared in a title.

This baseline showed whether a new method beat a boring implementation enough to justify extra dependencies. It also served as an executable specification. When an embedding index performed badly, I could usually trace the failure to a query that used different words from the document.

I kept the baseline in the repository next to the benchmark set. Each tool read the same JSONL corpus and emitted the same JSON result format.

## First results

The first complete run surprised me. A local embedding index won the hit-rate comparison with 90%, while keyword search reached 78%. Mean reciprocal rank told the opposite story: keyword search scored 0.71 and embeddings scored 0.66.

The first run produced two headline measurements:

- embedding index: 90% hit rate, 0.66 MRR, 14 ms median latency
- keyword baseline: 78% hit rate, 0.71 MRR, 2 ms median latency

I inspected the top five for every miss. The embedding system often placed a correct neighbor in position six or seven, while keyword search either hit the right title or missed completely. A tiny reranker that combined cosine similarity with title overlap moved the embedding score to 0.78 and kept the hit rate at 90%.

The improvement looked good until I measured latency. Median query time rose from 14 milliseconds to 180 milliseconds because the reranker called a local cross-encoder. That was still acceptable on a laptop, but it changed the deployment choice for a small Raspberry Pi.

The cost also stayed simple. The embeddings had been created once for $0.18, and the local reranker cost nothing but electricity and patience.

## Refresh policy

A private benchmark can quietly become a museum. My notes mention projects from 2019, and my tools should still find them, but they shouldn't dominate the measurement. I added three rules to the repository README.

Every quarter, I replace at least ten queries that haven't been used in six months. Any fix to a tool adds a query that reproduces the bug. Every six months, I review labels for items whose meaning changed, especially files I renamed or split.

The set is private because it includes file names, project names, and fragments of my schedule. I keep the corpus in an encrypted local checkout and don't publish scores tied to individual documents. A public version would need separate labels and a corpus without those details.

## Benchmark status

The benchmark lives in one repository with 82 queries, labels, a baseline, and four adapters. A run takes about 35 seconds and produces a small markdown report. It has already caught two regressions caused by changes to filename normalization.

The adapters follow one small Python protocol with a `search(query, limit=5)` method. That made it easy to add the reranker without changing the runner. It also kept each system's dependencies in an optional extra, so the baseline could still run on a machine with no embedding libraries installed.

It still doesn't measure subjective usefulness. A result can rank highly and still show the wrong section of a long note. I plan to add section-level highlights to the next version.

## Lessons Learned

An impression can choose a tool for today. A small local benchmark makes the next change easier to defend.

I don't need a leaderboard or a large test suite. I need queries I actually ask, labels I trust, and a baseline ordinary enough to keep me honest.

I'll describe the section-level evaluation in a future post, and you can subscribe to follow that experiment.
