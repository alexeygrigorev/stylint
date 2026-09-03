# A Personal Knowledge API for Reused Ideas

This synthetic style exercise uses a fictional project and invented details.

Last year I filled 312 markdown notes while I studied retrieval systems. Three months later I couldn't find the note explaining why I rejected a vector database for my first personal search tool.

I tried folder names and better titles first. They helped a little, but they depended on me remembering the exact vocabulary I used at the time. That assumption was wrong: I often remember the conclusion and forget the words I used to reach it.

In this post, I'll share:

- how I modeled notes as records with stable ideas and reusable evidence
- why I added citations before I added semantic search
- how the API exposes search, citations, and related notes
- what the first month of real usage showed
- what I still do manually

The usage counts in this article are invented examples rather than records from a real product.

## The Data Model

I use three record types:

- a note, the original markdown file
- a claim, one sentence that I want to reuse
- a source, a book, article, talk, or one of my own projects

I use this schema for a claim:

```text
claim:
  id: "2026-07-14-retrieval-latency"
  text: "Retrieval quality usually dominates model quality for small, focused domains."
  status: working
  confidence: medium
  evidence:
    - source: "my book-search prototype"
      quote: "Better filtering raised successful lookups from 62% to 81%."
      date: "2026-06-30"
  related:
    - "2026-07-02-evaluation-set"
```

The schema is deliberately small. It links a reusable sentence to the evidence that convinced me, so an old note can answer a new question.

## Citations Before Search

My first version imported all notes into SQLite and searched them with SQLite FTS5. It found notes quickly, but it didn't tell me why a result deserved attention.

I tested it with 20 questions from my own project journal. Nine results were useful, five were nearby, and six were irrelevant. More annoyingly, three useful results referenced claims I had already stopped believing.

So I inverted the work before improving search and extracted claims with attached evidence. A claim without evidence received a draft status, while stale evidence made it outdated. The API could then suppress outdated claims while keeping the original note available.

This made the collection slower to grow, but it made each item more useful when it appeared.

## The API Surface

I built a small FastAPI service with four endpoints:

```bash
uvicorn knowledge_api.app:app --reload --port 8000
```

The command starts a local server, so I don't run it in production.

The routes are these:

- `GET /claims?q=` for full-text search
- `GET /claims/{id}` for one claim and its evidence
- `GET /claims/{id}/related` for connected notes
- `POST /ingest/note` for a new markdown file

Search uses SQLite FTS5 over the claim text, source titles, and tags. The related endpoint follows explicit `related` links first. If there are fewer than three, it fills the remaining slots with semantic neighbors from a local embedding model.

The important rule is ordering: explicit citations come before inferred similarity. That keeps a personal opinion grounded in the reason I recorded it.

## First Month of Usage

I imported 187 of the 312 notes and extracted 94 claims. Another 118 notes stayed out because they were meeting fragments or temporary calculations. The remaining seven were duplicates.

For four weeks I used the API while writing two project reviews. It surfaced useful evidence 23 times. Sixteen answers came from full-text search, and seven came from semantic neighbors. Six of the 23 included a forgotten citation.

The sample is small, but the time saved was real. Review drafting took about 45 minutes per project instead of 90 to 120 minutes. Most of the gain came from not reopening notebooks to find an old benchmark.

The API also exposed weak assumptions. Eleven claims were outdated during import, and seeing them beside current claims made it easier to update the underlying notes.

## Manual Work

I write the claim sentence by hand. The extractor can propose candidates, but a sloppy claim creates bad search results for months. I also choose related links, which encode judgment about what belongs together.

Ingestion stays semi-automatic because the parser reads frontmatter and headings. It then shows me a preview, and I accept or edit the proposed claims before they enter the database.

The biggest gap is source quality. The API knows that evidence exists, but it doesn't know whether a measurement was careful. For now, I use a three-level confidence field and keep personal measurements separate from external sources.

The principle I took from the month: make evidence a first-class record. A personal knowledge base becomes useful when it preserves why an idea earned a place.

I'll write more about the ingestion parser in a future article. If you want to follow along, don't forget to subscribe.
