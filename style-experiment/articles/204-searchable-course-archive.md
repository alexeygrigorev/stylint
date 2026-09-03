# Making a Course Archive Searchable for Alumni

I wrote this synthetic style exercise as a build log, and all project details are fictional. I ran a small SQL course for three cohorts between 2023 and 2025, and its chat archive holds 41,000 messages from 214 alumni. In January 2026 two alumni asked where the week 4 exercise lived. The honest answer was that nobody could find anything in a 1.2 GB export.

The archive lived as a chat export of JSON files, images, and a folder structure only I understood. Alumni asked questions at midnight in every time zone, and I answered the same five questions about once a month. Over three weekends in February 2026 I built alumni-search, a small search site over that export.

In this post, I'll share:

- the shared folder attempt and why it failed
- how the import script loads the export
- what normalization removed from the messages
- how the SQLite index works
- how the archive gets its monthly update
- how access stays alumni-only

## A Folder Nobody Could Search

The naive attempt was to share the raw export. I zipped the 1.2 GB archive, put it in a cloud folder, and posted the link in the alumni chat in November 2025. The folder's search matched filenames, and the message text sat inside JSON files it never opened.

Four alumni downloaded the zip in two months, and one described the unzipped result as a wall of files. Sharing the archive was easy, and finding anything inside it was the actual problem.

My mistake was shipping the raw export and calling it an archive. The rule I took from it: an archive nobody can search is a box of backups.

## The Import Script

The import script, archive-import, is about 200 lines of Python that reads the export and writes one SQLite database. It goes through the export folder and parses each JSON file. It inserts one row per message with its cohort, channel, timestamp, and text.

The first run took 25 minutes and produced a database of 380 MB. Messages without text, such as image-only posts, still get a row with their caption and attachment path. The import is repeatable by design: I wipe the tables and rerun, because 25 minutes is cheap and incremental logic isn't.

## Cleaning The Messages

The raw text had escaped HTML characters like `&amp;` throughout, so the script unescapes them. Mention markers became plain names, code blocks lost their language tags, and 40 MB of base64 image data moved out to files on disk.

Names raised the harder question. The course chat used first names, and alumni signed with whatever they preferred that day. The script keeps a mapping table of 61 display names, each with one canonical spelling. It also drops six messages entirely, where a student shared personal details I had promised to keep out of any index.

The rule I took from the cleanup: normalize for the reader, and record every transformation, because a surprising result should explain where it came from.

## The Search Index

The searchable core is SQLite FTS5, the full-text extension that ships with SQLite. Building the index over 41,000 messages took 8 seconds on my laptop, and the whole database with the index is 410 MB. A query returns in under 20 milliseconds, which makes the site feel instant even on the 5 EUR per month VPS that hosts it.

One search query shows the whole setup:

```sql
select message_text
from messages_fts
where messages_fts match 'window function*'
order by bm25(messages_fts) limit 20;
```

The match string supports prefix search through the asterisk, and bm25 orders the results by relevance. Exact phrases get a boost through a second column query, because alumni often search for error text they half remember. I wrote the site as a 150-line FastAPI app with one search box and a result list.

## Monthly Updates

The course still runs, so the archive grows by a few hundred messages per cohort. On the 3rd of each month I export the chat and copy the file to the VPS. The import runs with a `--since` flag that loads only new messages. A cron job reminds me, and the whole update takes about 15 minutes including reading the log.

Ideally a GitHub Action would run the export for me. The chat service's API makes that awkward, so a cron reminder plus a manual run remains the honest solution for now.

## Keeping It Alumni-Only

The archive is private by agreement, so the site checks access before it returns a single row. Login is a magic link. A member enters an address, and the site checks it against an allowlist of 214 course addresses. The link expires in 20 minutes. Search queries get logged with a truncated timestamp, so I can see what people hunt for without keeping a full history.

Public visitors see something different. Without a session the site shows the message count and nothing else. The search API returns an empty result set instead of an error, so the endpoint reveals no rows to probe.

Two months in, the site answers the midnight questions, and the alumni chat gets about one search-related message a week instead of five. Six messages stay unindexed by agreement, attachments are searchable by filename only, and the monthly update is still manual. Those limits feel acceptable for a course of this size.

I'll write about the query log analysis in a future post. If you want to follow along, don't forget to subscribe.
