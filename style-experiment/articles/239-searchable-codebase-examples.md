# Indexing Code Examples Across My Repositories

I wrote this synthetic style exercise as a build log, and all project details are fictional. In April 2026 I spent 20 minutes hunting for a DuckDB window function I had written in 2024. The code lived in one of 34 local repositories, and I couldn't remember which one.

That hunt was the third one that month, so that weekend I built a small search index over my own code. It now answers questions about my own examples in seconds, and this post is the build log.

In this post, I'll share:

- why grep stopped working as an example library
- what my first index attempt got wrong
- how the extractor fills a SQLite table
- how tags and queries behave in practice
- how the index stays current

## Grep Hit Its Limits

My repositories held the examples: 34 folders, about 210,000 lines of Python and no shared index. Grep found exact strings fast, and it failed the moment I remembered the idea instead of the name.

A typical hunt meant grepping a half-remembered function name across every folder, then reading dozens of false matches. One hunt in March ended with me rewriting the function from memory instead of finding it. Three hunts in April cost 15 to 20 minutes each, which added up to most of a working day.

Most questions were about reuse: a retry loop with backoff, a Parquet export, a pytest fixture for a fake database. I remembered writing each one, and none of them had an obvious search string.

## First Attempt: A Snippet Folder

My first idea was a folder of snippets. I spent one evening in April copying 40 examples into `~/code-snippets`, each with a one-line comment at the top.

It failed within two weeks. Copies drift from the repos the moment the original code changes, and I never remembered to update the folder. The rule I took from it: an index must point at the real files, and pointing means storing paths, never copies.

The folder also hid the context. A snippet without its imports, tests and config is a puzzle, and half the copies were puzzles.

I deleted the folder on 2 May and kept the idea of an index.

## The Extraction Script

The index lives in SQLite, one table of examples with repo, path, language and tags. A script called `index-examples`, a small Python script that walks my code folders, fills the table.

Extraction uses Python's built-in `ast` module, a parser that reads code without running it.

The script keeps a function or class when it meets three rules:

- it has a docstring of at least one line
- it runs under 50 lines including blanks
- its file is tracked in git and not generated

Each accepted example goes into the table with its repo name, relative path, line range and docstring. The April run found 1,240 examples across 34 repositories in 48 seconds.

Docstrings do double duty in the design. They decide acceptance, and they become the searchable text, so a thin docstring means a thin result.

The rebuild command is one line:

```bash
uv run python index_examples.py ~/code --db ~/index/examples.db
```

A full rebuild takes under a minute, so I never bothered with incremental indexing. The whole corpus fits in one pass, and simple beats clever at this size.

## Tags And Queries

Tags come from folder names and from a manual map in `tag-rules.txt`, with a fallback tag called untagged.

The map covers the domains I reuse most:

- duckdb for anything that queries Parquet or Postgres
- fastapi for service endpoints and auth handlers
- pytest for fixtures and test factories
- airflow for job graphs and retry logic

The DuckDB window function came back with one query:

```bash
sqlite3 ~/index/examples.db "SELECT repo, path FROM examples WHERE tags LIKE '%duckdb%' AND docstring LIKE '%window%'"
```

The query found the function in four seconds, down from 20 minutes in April. Three of these queries now live in a `queries.txt` file next to the database, one per line with a comment. Examples without a tag still show up in repo-scoped queries, which covers most of my daily use.

## Keeping The Index Fresh

Stale indexes lie quietly, so updates run on a schedule. A cron job reindexes every repository at 22:00 each Sunday, and the rebuild costs 48 seconds of CPU on the VPS.

When I delete an example, the full rebuild drops the row without a diff, which keeps the script at 90 lines. The Sunday run also prints a count per repository, and a drop of more than 10% means a path moved. The one gap is code in work repositories, because the cron job runs on my machine and sees only mounted folders.

## Closing Notes

The arc went from 20-minute hunts to a four-second query, mostly by refusing to copy code out of its repository. The index holds 1,240 examples today, and about 15% stay untagged because their folder names say nothing.

Search over docstrings misses intent, so a query for retry-with-backoff still depends on the tag map. Ranking is the next gap, because a common helper drowns out the example I actually want. The build took one weekend of about ten hours, and maintenance costs two minutes per week of attention.

I'll write about ranking the results in a future post. If you want to follow along, don't forget to subscribe.
