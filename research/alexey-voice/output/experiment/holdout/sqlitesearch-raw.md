I built SQLiteSearch for a project in the AI Engineering Buildcamp. I wanted a persistent, lightweight search library that I could use for teaching a data ingestion pipeline separately from the RAG agent.

I already had minsearch. It supported both text and vector search, but it kept the indexed data in memory. Every time I restarted the Python process, I had to rebuild the index. That was fine for some experiments, but it wasn't what I needed for a pipeline that should run independently. I needed the index to stay available between runs.

I also had a few practical requirements. I wanted to use Python, run everything locally without Docker, keep the setup easy and support both text and vector search. Google Colab was one of the environments I wanted to support. I discussed these requirements and the existing options with ChatGPT. SQLite text search fit many of them, so I looked for an approach that could add vector search to it. None of the options I reviewed met all my requirements.

For vector search, I chose locality-sensitive hashing, or LSH. I understood how it worked and had implemented random projections before. That mattered because I wanted to be able to debug the implementation myself. I didn't want to depend on an AI assistant every time something went wrong. This was a choice I could work with and explain; I wasn't claiming that LSH was the fastest or best method.

I also asked for an API that resembled minsearch. The course participants already had that interface in mind, and I didn't want them to learn a new one just to use the persistent version.

Once I had the requirements and the design, I discussed them with ChatGPT and asked it to prepare a plan. I saved the plan in a GitHub repository as plan.md, then asked Claude Code to implement it. I reminded Claude Code to include tests, because the design needed to be checked as it became code.

The result stores the search index in one SQLite database file on disk. It runs in the Python process, so it doesn't need a separate server. That gives me the persistence I needed while keeping the library local and straightforward to set up.
