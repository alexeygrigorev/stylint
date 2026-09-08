# Building SQLiteSearch for Small Projects

I wanted a compact Python search library that was local, easy to integrate and persistent. My existing minsearch library already supported text and vector search through a simple API, but it kept the index in memory. When the Python process ended, the indexed data disappeared and I had to rebuild it after every restart.

The need came from an AI Engineering Buildcamp project. I wanted participants to build an ingestion pipeline that could operate independently of the RAG agent, so an in-memory index wasn't enough. The replacement needed to run in Python, work locally without Docker and support both regular text search and vector search.

## Choosing the library structure

A server such as Elasticsearch felt too large for this use case. The source describes it as a system designed for large production deployments that can cost more than $200 per month. Qdrant and PostgreSQL offered other possibilities, but using either would mean an external service or a Docker setup.

I used ChatGPT to brainstorm because I knew the requirements but didn't yet know whether an existing library matched them. It suggested SQLite text search. SQLite was appealing because it's embedded in Python and stores data locally. It didn't provide vector search by default.

I checked possible SQLite-compatible approaches. lshashing was pure Python but kept its hash tables in memory. SparseLSH supported storage backends such as Redis, LevelDB and BerkeleyDB, but not SQLite. narrow-down supported SQLite, yet depended on a native Rust extension. None met all the requirements, so I decided to build a new library.

## Making the implementation understandable

I added locality-sensitive hashing to the design for vector search. I already understood LSH from implementing random projections several times. I chose that approach instead of a more advanced technique that would be harder for me to debug. If something failed, I wanted to understand the code well enough to fix it without depending on an AI assistant.

I also asked ChatGPT to design an API close to minsearch. That would let the Buildcamp participants use familiar operations rather than learn a completely different interface. The first name in the plan was LightSearch. I renamed it SQLiteSearch before publishing because litesearch was already taken on PyPI.

The implementation process had a deliberate handoff. ChatGPT helped me research existing solutions and iterate on the design, then produced a summary and a detailed plan. I put the plan in a GitHub repository, renamed `summary.md` to `plan.md`, and asked Claude Code to read it and implement the library. I reminded Claude to include tests because a reusable library needs more than a working demonstration.

## Final architecture

SQLiteSearch stores the index, its tables and search metadata in one SQLite database file. SQLite runs inside the Python process, so there's no separate server, network layer or background daemon to configure. I could install the package and use it without cluster management, JVM tuning or DevOps work.

That makes the library a fit for small personal and course projects where persistent search matters more than production-scale infrastructure. It sits between an in-memory tool such as minsearch and larger systems such as Elasticsearch or Qdrant. The project also gave me a repeatable release workflow: my Claude Code `/release` command handles Python package publication. `/init-library` can create the project configuration, tests and CI/CD needed for a new library.
