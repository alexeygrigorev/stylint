# Caching Embeddings for a Small Personal Project

This synthetic style exercise follows a fictional side project with invented numbers and dates. Last June I cached embeddings for 2,140 notes in a local search tool. No detail here describes real events or real user data.

The tool embeds each note section with a small local model on a ThinkPad. I had recomputed vectors on every run and each rebuild took nine minutes.

The request asked for key inputs, storage format, invalidation and size in one build. I wanted those answers without a server or extra services in the loop.

In this post, I'll share:

- how I key cache entries
- how I store vectors on disk
- how I invalidate stale rows
- how I keep size small
- what caching saved in practice

## Cache Keys That Stay Stable

I started with 2,140 sections pulled from June notes with paths kept. Each key combines file path, section title and model name.

I keep keys in SQLite and I hash them with SHA256 for lookup. KeyBox, a small Python class that builds keys from inputs, sits beside the store.

I chose SHA256 because I know it well enough to debug collisions at midnight without extra tools. The downside is long strings, and that trade has stayed manageable for 2,140 rows.

I counted 2,312 vectors early and I grouped them by note age and length. That manual tally took 29 minutes and it forced me to see duplicate sections.

I split the keys across three groups I checked in June:

- unchanged sections with stable hashes
- edited sections with new timestamps
- renamed files with moved paths

I kept all 2,312 keys so the first month stays complete for review.

One key looks like this inside the plain debug file:

```text
sha: 9f2c41aa7d3e
src: notes/garden.md#soil
model: MiniLM-L6-v2
```

I don't trust memory so I reread that debug file before every single run.

## Vector Storage On Local Disk

I store 384 float values per vector in a single SQLite blob column. The writer batches inserts, syncs once per run and keeps a write ahead log.

The full table holds 2,312 rows and it spans 14.6 megabytes on disk. At that size the whole cache fits beside notes without extra mounts.

The next layer holds metadata with timestamps, token counts and file sizes on Linux. Its total came to 1.8 megabytes, which stays tiny without extra tuning.

I chose blobs because I pay nothing for local disk and reads stay under a millisecond. The downside is opaque rows, and I added a small dump command.

The dump command shows four columns I read in June:

- key hash prefix for quick scan
- source path and section title
- model name and vector length
- updated timestamp in UTC

I don't keep duplicate vectors when text hashes match across files.

I write vectors with one short command before every review:

```bash
uv run python scripts/build_cache.py --notes ~/notes --db cache.db
```

That command fills missing rows so I can test search without recomputing all vectors.

## Invalidation Without Full Rebuilds

I mark a row stale when its source mtime moves past the stored timestamp. The old script wiped the table where a single edit forced nine lost minutes.

Both slow rebuilds came from timestamp checks skipped during rapid edits in June. I had ignored the clock skew in review, which turned out to be a mistake.

The rule I took from it: timestamps need checks before any read path serves vectors. I keep the check in Python so I can test logic without touching the database.

I chose mtime checks because I already use them for notes and they run fast. The downside is false misses, and I store content hashes as backup.

The stale rows passed three checks in the June sample:

- edited files flagged within one second
- renamed files flagged by missing path
- deleted files removed from index

I added hash compares for each flag and the line stayed correct.

I prune stale rows with one repeatable pass each night:

```bash
uv run python scripts/prune_cache.py --db cache.db --dry-run
```

That output lists stale counts first so I see scope without deleting data.

## Size Limits I Enforce Monthly

I cap the cache at 50 megabytes and I alert at 40 megabytes by mail. The blobs grew to 14.6 megabytes in June with 2,312 rows stored.

I recorded the growth curve and I kept weekly size photos for reference. A float16 trial cut size in half, yet recall dropped on three test queries.

I watch size and hit rates during reviews with Grafana charts. I skipped the size check once on a Friday run, which turned out to be a mistake.

The rule I took from it: size stays watched before any model change ships. I chose a hard cap because I can explain it in seconds to future me.

The downside is forced trims, and I document each trim in the monthly notes.

The trims target four groups I use in July:

- deleted notes removed from disk
- duplicate sections merged by hash
- old model vectors archived elsewhere
- oversized sections split by heading

I rehearsed the trim flow in staging and the full pass took 61 seconds. The evening run felt calm - the cap removed guesswork under time pressure.

## Lessons From Two Cache Rebuilds

The cache cut rebuilds from nine minutes to 47 seconds and it saved hours. Those numbers matter less than the hash checks that caught three silent edits.

I don't recompute all vectors now and I keep the SQLite file for six weeks. That window caught one late model rename in June logs.

I chose local files because I run the tool alone without server admin help. The downside is manual backups, and that routine has saved two restores.

I'll keep the 50 megabyte cap and I'll refresh hashes with fresh edits each week. I'll write about the next model after one more notes cycle. If you want to follow along, don't forget to subscribe.
