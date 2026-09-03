# Replacing a Notebook Search Script with a Local RAG Index

This synthetic style exercise follows a fictional practitioner. Last month that practitioner needed a note about Postgres partitioning and couldn't find it. The practitioner has 412 markdown notebooks, written over three years. They cover ML work, deployment experiments and reading notes. An old script found filenames and lines, but it couldn't connect a half-remembered idea to the note.

I thought I had the answer ready: "RAG" is retrieval-augmented generation, a method for giving a model relevant context before it answers. This project uses only the retrieval part.

The first version took an evening. It scans every `.md` file, splits notes into chunks, embeds those chunks and stores them in a local SQLite database. A single FastAPI page provides the browser UI with one search box.

In this post, I'll share:

- why the keyword script stopped working
- how the local index and search API work
- what the first queries got wrong
- how I changed chunking and ranking
- what the project costs and where it still fails

## Notes That Resist Search

Most notebooks start as a shortcut for a concrete task. Each note contains a command block, a decision and a caveat. For example, one note records a CORS fix in FastAPI and explains that the browser sends the preflight request before the real request.

That structure helps me write, but it hurts search. The useful answer may sit under a heading that says "Debugging", while the actual error text is two sections away. My notes also use the words I knew at the time, and I don't remember those words three months later.

The old workflow had one command:

```bash
rg -i "postgres partition" ~/notes
```

That command works when I remember the exact vocabulary, and it returned 38 matches for the query. Only two results were useful, and neither had the caveat about maintenance windows.

## The First Version

The obvious choice was a small Python script with a vector store. I had already used Chroma in other experiments, so I picked it again. The script walks `~/notes`, ignores `.obsidian` and `_templates`, then reads every file that ends with `.md`.

The first chunker split every note by blank lines, so each paragraph became one record. I saved 1,837 chunks in Chroma with `sentence-transformers` and the `all-MiniLM-L6-v2` model. The full import took 91 seconds on my ThinkPad.

The initial command was short:

```bash
uv run python scripts/build_note_index.py
```

Importing worked, but the surprise came when I searched the index. Vector search found paragraphs with related vocabulary, yet it often returned one good sentence without the surrounding context.

## Failure Queries

The first test query was "cloud backup for small database", and it exposed a real omission. The index returned a paragraph about PostgreSQL point-in-time recovery, and that result was useful. It omitted the actual constraint: the database was only 3.2 GB and the practitioner wanted backups from a home server.

The second query was "rate limit Celery tasks", and its top result came from a note about Nginx. It used the word "limit" and described traffic, but it had nothing to do with Celery. The system had returned a retrieval failure.

Paragraph chunks were too small. A paragraph that says "run this after changing the config" needs its neighboring section to make sense. The embedding also saw headings only by accident because I had removed them as noise.

The rule I took from the first week: retrieval has to return a reviewable context, and the context needs to include the note's own frame.

## Chunking By Section

The second version changed the unit from paragraph to section. The parser records the file path, section heading and section text. It keeps each section intact when the section is under 1,200 characters. A longer section gets split at paragraph boundaries, and each child record repeats the heading.

That change immediately improved the preview. When I search "Celery rate limit", the UI now shows the heading, the note date, the parent file and eight lines around the match. The record still stores the embedding, but the display gives me enough to judge the result.

The updated index records these fields:

```text
id
file_path
section_title
chunk_number
content
embedding
updated_at
```

The rebuild script writes to a temporary database and renames it at the end. That avoids a partially updated index if the process stops. A full rebuild now takes 47 seconds with the larger chunks.

## Search Results In Practice

I wrote 24 test queries from real questions I had asked during March. For each query, I marked whether a useful note appeared in the first five results. The keyword script scored 13 of 24. The section-based index scored 19 of 24.

That number deserves a caveat. I wrote the test set after using the new index, so I was already thinking in its vocabulary. A fairer test would use questions recorded before any search.

Three query families now work well:

- commands remembered only by their outcome
- errors copied from a terminal
- broad topics such as "auth for internal dashboard"

Exact matches still beat vector search. If I search an identifier such as `AWS_ACCESS_KEY_ID`, the script falls back to `ripgrep`. That hybrid path returns stable results and avoids the odd embedding gap for tokens that look like configuration.

## The Cost Of Running It

Everything runs locally on a ThinkPad with 32 GB of RAM. The embedding model uses about 120 MB, and the index database is 14.6 MB. The API usually answers in 45 to 120 milliseconds after a warm-up search.

There's no API bill, and the one-time download for `sentence-transformers` was about 90 MB. The rebuild runs in the background while I make coffee, and local storage costs nothing.

The bigger cost is attention. On two occasions I spent 40 minutes improving search when I should have been writing a note. Internal tools include that hazard.

## Lessons From The First Month

The project did its job last Tuesday. I typed "restore table after accidental delete", and the first result took me to a note from February. It had the command, the warning about point-in-time recovery and the reason I hadn't enabled that feature on the database.

This project taught me a narrower lesson than "add RAG to everything". Keyword search remains the right first tool for identifiers and exact error strings. Local embeddings add value when the words in a question differ from the words in a note.

The index still has gaps because it doesn't search PDFs, images or code repositories. It also has no freshness measure, so a corrected note can sit beneath an older one. My next change is a small date boost, followed by another 20-query check.

I'll write about that evaluation in a future post. If you want to follow along, don't forget to subscribe.
