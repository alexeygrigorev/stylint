# parsing and Reusing Personal Data Exports

I wrote this synthetic style exercise as a build log, and the app, dates and numbers are fictional. On 12 January 2026 I requested a full export from Daybook, a journaling app I've kept since 2023. Three days later a 3.1 GB zip arrived with 214 JSON files - and no index of any kind.

I wanted my entries in a local database so I could query my own writing. The export had other plans, and the plans changed twice more before April.

In this post, I'll share:

- the two schemas hiding inside one export
- how the parser normalizes entries into SQLite
- the cleanup passes that fixed dates and duplicates
- how I trimmed the data for privacy before reuse
- the queries I now run every month
- where the pipeline stands after a schema change

## The Export And Its Two Schemas

I first opened the files with `jq`, a command-line JSON tool, expecting one uniform format. The export mixed two schemas instead. Entries before March 2025 stored timestamps as Unix milliseconds in a `created_ms` field, while newer entries used ISO strings in `created_at`.

One folder also held 117 duplicate entries that appeared in both a monthly file and a yearly file. A quick count showed 4,318 entries in total, and I had no way to tell which copy was newer. Reading files by hand stopped being an option at that size.

Documentation amounted to a single README with three sentences. Neither schema appeared in it, and the field names never matched the app's own UI wording. I learned the real schema by printing keys from 20 sample files and writing down the differences.

## The Parser

So I wrote `parse_export.py`, a Python script that reads every JSON file and writes one SQLite database called `daybook.db`. The script detects the schema per entry and converts both timestamp styles to proper UTC datetimes. A full run over 4,318 entries takes about 40 seconds.

The whole pipeline is two commands:

```bash
python parse_export.py exports/daybook-2026-01.zip --out daybook.db
```

The script prints one summary line per source file and a final count of skipped entries. In January it skipped 23 entries with unparseable dates, and I fixed those by hand.

The normalizing step also fills a `word_count` column at parse time. Recomputing it during queries worked, but six queries then repeated the same length calculation, so the column earned its place within a week.

My first version copied every field into one table, including a telemetry blob I couldn't explain. The rule I took from it: parse only the fields whose meaning I can name in one sentence.

## Cleanup Passes

Three cleanup passes run before I trust the numbers. The dedupe pass removes the 117 cross-file duplicates by entry ID. The timezone pass fixes 62 entries recorded with a +09:00 offset from a trip to Japan, which plain string storage had mangled.

The empties pass drops entries with a body shorter than 20 characters, about 210 fragments that said things like 'gone running'. After all three passes the table holds 3,971 usable entries. I re-run the passes on every fresh export, because each new zip reintroduces the same noise.

Each pass writes its count to a small `cleanup_log` table. When a number looks wrong months later, I can trace which pass changed it and by how much.

## Trimming For Privacy

The export contained more than my own words. A `shared_with` field named two friends in plain text, and 340 entries had GPS coordinates from the phone client. The working copy now drops all three.

Names become salted hashes, coordinates are removed at parse time, and only the trimmed database reaches my working folder. The original zip stays in an encrypted volume, and it has stayed closed since January. My future self can still rebuild the full database from it if a field turns out to matter.

## Queries I Run Now

Twelve saved queries sit in a `queries/` folder, and I run the monthly one most often.

That query aggregates entries and word counts per month:

```sql
select substr(created_at, 1, 7) as month,
       count(*) as entries,
       sum(word_count) as words
from entries
group by month
order by month desc;
```

The March result showed 3,971 entries and 96,400 words, which matched the app's own stats page within half a percent. That match was the real acceptance test for the parser.

A second query counts entries per weekday, and it confirmed a suspicion about Sundays: 19 entries in three months, against 140 on a typical weekday. The database makes such checks cheap, and cheap checks actually get run.

## The Pipeline Today

The arc since January: a 3.1 GB opaque zip became a 6 MB SQLite file I query every week. The vendor shipped a third schema in April with a new `mood_v2` array field. The parser now reads a version marker first, so it fails loudly instead of guessing.

Two limits remain, and both came from the vendor's export choices. The export includes the trash folder, so deleted entries reappear in each new zip. I filter them with a `deleted_at` column, which costs one extra join in two queries.

A full refresh still costs about 45 minutes of attention, most of it spent reading the summary lines rather than fixing anything.

I'll write about the saved query set in a future post. If you want to follow along, don't forget to subscribe.
