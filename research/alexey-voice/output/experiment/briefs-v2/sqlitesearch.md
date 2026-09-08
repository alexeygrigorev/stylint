# Assignment

Write a 250–400 word first-person newsletter excerpt about why Alexey built SQLiteSearch and how he handed the design to Claude Code. This is a reconstruction of an archived account. Use only the facts below. Headings are optional. Output only article prose.

# Fact ledger

- S1: Alexey wanted a persistent, lightweight search library for a project in AI Engineering Buildcamp.
- S2: He already had minsearch, which supported text and vector search but kept indexed data in memory. He had to rebuild the index after restarting the Python process.
- S3: He wanted to teach a data ingestion pipeline that runs independently of the RAG agent. That required persistence.
- S4: He wanted Python, local operation without Docker, easy setup, and both text and vector search. Google Colab was one environment he wanted to support.
- S5: He discussed requirements and existing options with ChatGPT. SQLite text search fit many requirements; he then looked for a vector-search approach to use with it. None of the options he reviewed met all his requirements.
- S6: He chose locality-sensitive hashing (LSH) because he understood it and had implemented random projections before. He wanted to be able to debug the implementation himself without relying on an AI assistant.
- S7: He asked for an API resembling minsearch so course participants would not need to learn a new interface.
- S8: ChatGPT prepared a plan. Alexey saved it in a GitHub repository as plan.md, asked Claude Code to implement it, and reminded it to include tests.
- S9: SQLiteSearch stores its search index in one SQLite database file on disk and runs in the Python process without a separate server.

# Editorial instructions

Do not infer that LSH was the fastest or best method. This is an instruction for the writer, not a disclaimer for the article.

# Required content

Retain S1 through S9, especially why persistence, LSH and a familiar API mattered. Do not add prices, benchmarks, named alternative libraries, a release narrative, future plans or a CTA. These scope exclusions are instructions, not article content.
