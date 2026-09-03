# A Private Dashboard for My Publishing Workflow

I wrote this build log as a synthetic style exercise, and every dashboard metric, date, and project name is fictional. In the invented setup, I connected 236 article drafts, 97 published posts, and 14 newsletter sources into one private view during August 2026.

I didn't want public analytics. I wanted to see where drafts waited, which sources produced usable ideas, and how long a fact check took after writing ended. Existing tools each held one piece of that picture, so I built a small dashboard with SQLite, FastAPI, and Chart.js.

In this post, I'll share:

- the event types I recorded
- how the importer handles different sources
- the four dashboard views I kept
- the first month's numbers
- what I deliberately left out

## Events to Record

The first version tried to track everything. After two days, I reduced it to five event types that cover draft creation and updates as well as review completion and publication.

Each event has an event ID, article ID, timestamp, and source. The importer also stores optional duration.

I also added two attributes used for grouping. I took topic from a folder name and assigned each article one working state.

The storage is deliberately boring:

```sql
create table events (
  id text primary key,
  article_id text,
  event_type text,
  occurred_at text,
  source text,
  duration_seconds integer,
  topic text,
  working_state text
);
```

A single SQLite database now contains 6,812 events and uses 2.3 MB. For a personal workflow, that removes the need for a database server and makes backup a file copy.

## Importing Sources

The importer reads four source kinds. Markdown drafts come from a Git repository, and published post metadata comes from an RSS file.

```bash
python import_dashboard.py --source markdown --path ~/writing/drafts
python import_dashboard.py --source rss --path exports/published.xml
```

Each source has its own parser, but all parsers call the same validation function. The function rejects duplicate event IDs, timestamps in the future, unknown event types, and article IDs that don't match the project slug.

The RSS importer needed the most cleanup. It imported 97 published posts, but publication timestamps used the feed update time for 12 posts. I corrected those manually from post frontmatter and stored a `source_note` explaining each change.

I also added a dry-run mode. It reports how many new events each parser would create and lists the first five conflicts. That preview caught 38 duplicate events on the first RSS import, because the feed contained both full and summary entries.

## Dashboard Views

The final interface has four views. "Pipeline" shows counts by working state, while "Ages" shows how long articles have remained in drafting or review.

Each view has a date range selector and one filter for topic. I removed global filters after the first week because one broad filter combination produced an empty chart and invited pointless investigation.

I check the ages view most often. It sorts articles by days since the last update, and I can archive, resume, or delete the 20 oldest.

The review view uses median rather than mean. One article waited 71 days because I postponed a legal question, and it pulled the mean from 4.2 days to 7.9. The median of 3.1 days better described ordinary work.

## First Month

During August, I created 31 drafts and published 7 posts. Six drafts moved from idea to drafting within a week, and 11 remained in the idea state for the full month.

Median drafting time was 6.4 days from creation to review request. Median review latency was 2.8 days. Median total time from first draft event to publication was 16.2 days, though one product-release post took only 34 hours.

Source data changed how I planned. Community questions produced 9 drafts, of which 4 became published posts. Personal project notes produced 11 drafts, but only 2 reached publication. Old course notes produced 6 drafts and no published posts during the month.

That result matched my experience, but seeing it reduced the appeal of "I should turn these notes into something". I archived 18 old course notes instead of importing them into the drafting queue.

Fact checks were slower than I expected. They added a median of 1.9 days after drafting, mostly because I checked tool versions and release dates. That measurement led to a new rule: collect version numbers during drafting, while the relevant documentation is already open.

## Deliberate Exclusions

I left out reader analytics on purpose. Public views, clicks, and follower counts answer different questions, and mixing them with production metrics would make every decision drift toward popularity.

I also left out automated scoring. A number claiming "draft quality" would hide the judgment I actually need from a human reviewer. The dashboard can show that a draft waited. It can't say whether the draft deserves waiting for.

Collaborative state was another exclusion. Only I write these drafts, so a shared board would add authentication and synchronization for no current benefit. The local JSON log remains enough for review requests.

## Lessons

The dashboard works because it tracks a small number of durable events. Five event types, four sources, and four views answer the questions I ask weekly without making the system another project to maintain.

The best metric was source-to-publication. It doesn't judge an idea's quality, but it shows whether a source tends to produce finished work. That distinction is enough to decide what enters the drafting queue.

I plan to write about the importer validations and event schema in a future article. Subscribe if you want to see how the dashboard behaves after a full quarter.
