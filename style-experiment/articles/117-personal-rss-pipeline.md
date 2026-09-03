# A Personal RSS Pipeline That Survives a Busy Week

I wrote this synthetic style exercise as a build log. The feeds, counts, dates and service names are fictional.

In February my RSS reader had a 412-entry unread backlog after nine days away. It mixed long essays, release notes and some newsletters. I marked everything read and immediately lost two posts I needed for a workshop.

My reading problem came from volume. Some feeds publish 20 short notices each day, while useful essays arrive three to five times each week. I needed a system that could filter without deciding for me.

In this post, I'll share:

- how I split capture from reading
- how I reduced 71 feeds to 12 priority feeds
- how I built a small summarizer for long articles
- how the weekly review works
- what I changed after the first month

## Capture First, Judgment Later

The first version used one folder and one rule: read everything on Sunday.

That process lasted two weeks. A 412-item backlog made me skim titles, and useful essays disappeared under changelog entries.

I changed the setup instead of my discipline. Each fetched item gets one of three states in an SQLite table called `reading`.

- `new` for anything just fetched
- `queue` for anything I might read
- `archive` for anything processed

The fetcher inserts an item and leaves it in the `new` state. Nothing is marked read automatically. Every Sunday I review the items that reached `queue`, while short announcements stay in that initial state for only 14 days.

The database is deliberately simple. Its fields identify the feed and store the title, URL and publication date. Other fields hold state, score and summary.

A decision field and a `decided_at` timestamp show when I moved an entry, so the system can show whether my queue drains.

## Choosing Priority Feeds

I exported my OPML file and counted the last 180 days of entries per feed. Then I used my reader history from January and February. For each feed, I recorded how many items I had opened and how many I had saved.

The first measurement made me uncomfortable:

- 12 feeds produced 38 opened items from 96 published
- 23 feeds produced one or two opened items each
- 36 feeds had zero opens in 60 days

Those 36 feeds stayed in the fetcher for another month. I didn't delete them immediately, because a low open rate can mean a busy month. I moved them to a `low` priority and set their queue capacity to three items per feed.

After four weeks, only five of those feeds produced something I queued, so the other 31 became archived feeds. Their old items remained searchable, but they no longer entered the Sunday review.

The change reduced Sunday's input from about 430 items to 88. I kept the specialized feeds for machine-learning releases and local-government notices because they publish rarely, and each saved item had earned its place.

## Summarize Long Items

I chose a deterministic preprocessor and a local model rather than a coding agent.

The pipeline runs on a fictional home server named `atlas`:

```bash
rss-fetch --opml feeds.opml --database reading.db
rss-score --database reading.db --min-words 800
rss-summarize --database reading.db --model qwen3:8b
```

The fetcher stores the original HTML. The scorer extracts text, counts words and gives a priority score to items longer than 800 words. The summarizer runs only on those items, so a typical week involves 20 to 30 model calls rather than 430.

The summary prompt asks for the claim, the evidence and why the author thinks it matters. It also asks for one sentence saying when the article would be irrelevant. Each summary is capped at 220 words and stored beside the original URL.

I tested this on 62 saved essays from January. For 47, the summary was enough to decide whether to keep or archive the item. For nine, I read the full article anyway. Six summaries were misleading because the essays depended on code or charts.

The summarizer didn't replace reading. It moved the first decision earlier and made the queue shorter.

## The Sunday Review

The weekly review takes 25 to 40 minutes.

I start with a generated list rather than a reader inbox:

- five to eight priority items, sorted by feed score and age
- three low-priority items at most
- all items waiting longer than 21 days

For each item, I choose `read now`, `queue for later`, `save to notes` or `archive`. Choosing is fast because the summary sits above the link. I read only after I decide an item deserves the time.

At the end of the session, the report showed that 88 entered review. It sent 12 to the reading queue, saved 9 to notes and archived 54. The remaining 13 stayed another week because I hadn't opened their short notices yet.

I cap the reading queue at 15 entries. When it's full, adding another removes the oldest one and returns it to the `new` state. That constraint sounds harsh, but it keeps the queue a commitment instead of a second inbox.

## Results From the First Month

That month produced 428 processed outputs. I queued 71, saved 19 to notes and read 38 to the end. Average time from publication to decision fell from 19 days to 6.

The unopened backlog stayed between 30 and 52 titles rather than growing past 400.

I corrected the scoring after that month. It had relied only on length, so it promoted every long interview. The revised score added source priority and a keyword list for data engineering and local policy.

Second, summaries consumed 1.9 GB of model context over the month because I forgot to truncate extracted HTML before processing. The fixed extractor reduced that use to 320 MB.

I also removed automatic tweet-style highlights because they didn't help me decide whether to read. The useful summary was the evidence sentence, especially when it named a dataset, method and result.

## Lessons From the Pipeline

The pipeline works because capture, filtering and reading have separate steps. The fetcher never judges, the scorer ranks, the summarizer prepares a decision and I make the final call.

The queue is now small enough to be honest. If I can't fit an item into 15 slots, that's a real decision about my week. I still miss essays, but the report makes the misses visible.

Next I'll audit feed priorities monthly and write about the result in a future post. If you want to follow along, don't forget to subscribe.
