# Benchmarking Two Local Search Options on My Own Notes

This synthetic style exercise follows a fictional practitioner. The notes, queries, and measurements are fictional and illustrate a local search comparison. Last March I managed 842 Markdown notes in a private Git repository and struggled to locate older decisions.

I had relied on `ripgrep` for two years. The tool found exact strings in milliseconds, and I trusted it for identifiers and error messages. It failed when my query words differed from the words I had written months earlier.

In this post, I'll share:

- the note collection and query sample I used
- how the keyword baseline performed
- how a small embedding index performed
- the timed comparison and deployment costs
- what I kept for daily use

## The Note Collection I Tested

My fictional notes cover ML experiments, deployment checklists, and reading summaries from 2023 through 2026. I keep 842 files and around 310,000 words in the repository. Most files contain a heading, a command block, and a short decision record.

I selected 30 queries from questions I had asked during February. Each query came from a real task, such as restoring a table or tuning a queue. I wrote the queries before running either system, so neither option had an advantage.

I labeled each query with the file I expected. A result counted as a hit when the expected file appeared in the first five entries. I also recorded latency with a simple timer around each call.

The labeling took about 90 minutes. I reviewed the expected files, removed three ambiguous queries, and replaced them with clearer tasks. That left 30 queries I could defend during review.

## The Keyword Baseline

The baseline used `ripgrep` through a five-line Python wrapper. The script searched file contents, ranked files by match count, and printed the first five paths. It ran locally with no model and no index build.

The setup command was direct:

```bash
uv run python scripts/keyword_search.py --query "celery rate limit" --top 5
```

The command prints five file paths with line numbers and match counts. I copied the output into a log file after each query. The median latency was 38 milliseconds on my ThinkPad.

The baseline scored 17 hits from 30 queries. It excelled at identifiers, config keys, and exact error strings. It missed paraphrased questions because it needed shared vocabulary between query and note.

The rule I took from that round: keyword search remains the right default for exact tokens, and it needs help when wording drifts. I kept that lesson while building the second option.

## The Embedding Index Build

The second option used `sentence-transformers` with the `all-MiniLM-L6-v2` model and SQLite for storage. I call the script `note-index`, a 210-line Python program that chunks notes by section. It stores the file path, heading, text, and vector for each chunk.

I built the index with one command:

```bash
uv run python scripts/build_note_index.py --source ~/notes --db notes.db
```

The build processed 842 files into 2,140 chunks in 96 seconds. The database file reached 18.4 MB, while the model download added about 90 MB. Search ran locally with no network calls after setup.

The query path embeds the question and returns the closest chunks.

I wrote a second command for that step:

```bash
uv run python scripts/vector_search.py --query "celery rate limit" --top 5
```

The command prints the heading, file path, date, and eight lines around each match. Median latency was 110 milliseconds after warm-up, which felt instant during manual use.

## Timed Comparison And Deployment Costs

I ran all 30 queries through both options on the same evening. The keyword baseline found 17 expected files in the top five. The embedding index found 23 expected files in the top five.

That gap needs context because I had written the notes, so my queries shared vocabulary with recent entries. Older notes used different terms, and the embedding index handled those cases better. Seven queries succeeded only with vectors, while one query succeeded only with keywords.

The cost comparison favored keywords for setup and vectors for recall. The keyword path needed no model, no build step, and 38-millisecond responses. The vector path needed a 90 MB download, a 96-second build, and 18.4 MB of storage.

I also tested a hybrid path during the second week. When the query contained an identifier with underscores or a dotted path, the script called `ripgrep` first. Other queries went to the vector index by default.

The hybrid scored 25 hits from 30 queries. It added about 40 lines of routing code and one config flag. The added code checks for code-like tokens before choosing the search path.

Maintenance differs between the options. The keyword script needs almost no care beyond Python updates. The vector index needs a rebuild after bulk edits, plus a check when the embedding library releases a new version.

## The Setup I Kept

The benchmark changed my daily flow in a narrow way. I still use `ripgrep` when I remember an identifier, a path, or an exact error string. I use the vector index when I remember the problem but forgot the words I used.

The hybrid script now lives behind one alias in my shell. It routes code-like queries to keywords and sends the rest to vectors. The alias saved me from choosing a system before I had described the question.

This project taught me a smaller lesson than wholesale replacement. Measurement beat preference, and a 30-query sample exposed strengths I had missed. The numbers were fictional here, but the routine transfers to real collections.

I'll extend the sample with 20 harder queries this autumn and record where the hybrid still misses. If you want to follow along, don't forget to subscribe.
