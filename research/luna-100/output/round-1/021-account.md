# Why I Built SQLiteSearch

I wanted a compact Python search library for small projects. It needed to run locally, be easy to integrate, and keep its data after the Python process stopped. I already had minsearch, which provided text and vector search through a simple API, but it kept the index in memory. Every restart meant rebuilding everything.

That limitation mattered for the AI Engineering Buildcamp. I wanted participants to build an ingestion pipeline separately from the RAG agent, so the search index needed to persist independently. Elasticsearch was designed for much larger production systems and, in my estimate, could cost more than $200 per month. Qdrant and PostgreSQL were possible alternatives, but they meant using an external service or running Docker. That was more setup than I wanted for a course project.

I wrote down four requirements: Python support, a simple local API, no Docker, and both regular text and vector search. I used ChatGPT to investigate the options because the exact solution was not clear to me yet. It suggested SQLite text search, which matched the local and persistent parts. SQLite is embedded in Python and included in the standard library, but it did not provide vector search out of the box.

I continued the conversation to find a vector-search approach that could work with SQLite. The options did not line up with all the requirements. lshashing was pure Python but kept its hash tables in memory. SparseLSH supported other storage backends but not SQLite. narrow-down used SQLite but depended on a native Rust extension, so it was not pure Python. None of them was the small, local, persistent combination I needed.

For vector search, I chose locality-sensitive hashing. I had implemented random projections before, so I understood the technique well enough to debug it without relying on an AI assistant. More advanced methods might have been possible, but knowing how the chosen method worked was more useful for this project. I also asked for an API resembling minsearch, so Buildcamp participants would not have to learn an entirely new interface.

ChatGPT turned our discussion into an implementation plan. The working name was LightSearch, but I changed it to SQLiteSearch before publishing because “litesearch” was already taken on PyPI. I saved the plan, created a GitHub repository, renamed the file to `plan.md`, and asked Claude Code to implement it. I reminded Claude to include tests because a library needs more than code that appears to work once.

The result stores the index, lookup structures, and metadata in one SQLite file. It runs inside the Python process, without a separate server, network calls, cluster management, or JVM tuning. That puts it between an in-memory library like minsearch and production search systems such as Elasticsearch or Qdrant.

I used the same workflow to publish it. A Claude Code `/release` command handles the Python package pipeline, while `/init-library` creates the initial project structure. If a build or test fails, Claude updates the configuration or tests and runs the pipeline again. Publishing becomes a repeatable workflow rather than a sequence of commands I have to remember.
