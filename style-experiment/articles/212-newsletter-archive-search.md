# Making My Newsletter Archive Searchable

I wrote this synthetic style exercise as a build log, and the newsletter, numbers and dates are fictional. My newsletter published its sixtieth issue in March 2026. That same week, a reader asked where I had compared embedding costs, and I couldn't find my own post for 25 minutes.

The post existed in an issue from the previous October, under a title about evaluation budgets. The platform search matches titles only, and I remembered the wrong month and the wrong title.

So in April 2026 I spent two evenings making the archive searchable on my own laptop. The setup costs nothing per month and answers questions about my own back catalog in seconds.

In this post, I'll share:

- why the platform search failed me
- how I clean the export into plain markdown
- how the SQLite index gets rebuilt each week
- how related posts get picked for new issues
- where the setup still falls short

## Sixty Issues And One Missing Post

The export button on the newsletter platform produces a zip of HTML files, one file for every issue. Each file includes the full post plus subscription boxes, footers, and navigation markup. Sixty issues came to 41 MB uncompressed, and I estimated about 90% of that was boilerplate.

My first attempt was a grep for "embedding" across the HTML. It returned 400 matches, and most sat inside JavaScript from the shared footer. The rule I took from that hour: clean the text before you search it.

## Cleaning The Export

I wrote `strip-html`, a small Python script that keeps the post body and drops the rest. It walks the export folder, extracts the article element from each file, and writes one markdown file per issue.

The whole cleanup runs with one command:

```bash
uv run python tools/strip_html.py exports/archive/ --out clean/
```

The script processed 60 files in about four seconds and produced 3.1 MB of clean markdown. Each output file keeps the title, the publish date, and the body text. One issue lost an image caption to the extractor, and I restored that caption by hand.

The date field mattered more than I expected. Posts now keep their publish date as metadata, so a result can say "October 2025" instead of a bare filename. That detail makes old hits feel trustworthy at a glance.

## Building The Index With SQLite

The clean files go into SQLite with FTS5, the full-text search extension that ships with SQLite. I picked it because the index lives in one file I can copy between machines. Postgres with its own full-text engine was the alternative, and I skipped it. The archive changes weekly at most, so one extra running service for 3 MB of text made no sense.

Creating the table takes three lines:

```python
db.execute(
    "CREATE VIRTUAL TABLE posts USING fts5("
    "title, published, body, tokenize='porter')"
)
```

Indexing 60 posts takes under a second, so I never built anything incremental. A cron job rebuilds the whole index every Monday at 02:00 from the export folder.

The search command takes a query and prints the five best posts with scores:

```bash
uv run python tools/search_archive.py "embedding cost comparison"
```

The porter tokenizer folds word variants together, so a search for "tests" also matches "testing". That one choice fixed half of my early misses. On the October post, the correct file now comes back as the top hit in about 30 milliseconds. The whole tool folder holds about 260 lines of Python, and the index file weighs 2.2 MB.

## Related Posts From Shared Terms

The second job grew out of the first. When I finish a draft, I want a short list of older issues to link at the bottom. I wrote `suggest-related`, a second script that scores every published post by the content words it shares with the draft.

The scoring stays deliberately plain. Stopwords drop out, each shared word counts once per post, and longer posts get no bonus. The top three posts become the suggestions.

The script needed one guard I didn't expect. A draft that quotes an older issue shares many words with that issue, so quoted passages once dominated the suggestions. I now subtract words inside quotation marks before scoring.

For my evals issue in May, the script suggested two posts from October that I had completely forgotten. I pasted both links in and dropped a third that only shared the word "testing". Reviewing the suggestions takes about five minutes per issue. The links also get more clicks than the ones I picked myself, at least judging by the last month of analytics.

## Limits After Two Months

The setup has answered about a dozen questions since April, and half of them were mine. Full-text search over 60 posts is a small tool, and it removed a recurring frustration from my writing week.

It knows nothing about synonyms, so a search for "RAG" misses posts that only say "retrieval". Updates also depend on me running the export by hand. In May I forgot one export, and the cron job quietly indexed nothing for two weeks.

That gap produced a second rule: check the index date before you trust a "no results" answer. The public-facing side also stays out of scope for now, because the index contains paid-issue text I shouldn't republish.

I'll write about a reader-facing search page for the free issues in a future post. If you want to follow along, don't forget to subscribe.
