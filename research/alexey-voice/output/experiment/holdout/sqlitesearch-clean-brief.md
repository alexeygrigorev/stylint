I wanted a persistent, lightweight search library for a project in the AI Engineering Buildcamp. I already had minsearch, which supported both text and vector search, but it kept the indexed data in memory. Every time I restarted the Python process, I had to rebuild the index.

That became a problem because I wanted to teach a data ingestion pipeline that runs independently of the RAG agent. For that, the data had to persist. I also wanted the library to use Python, run locally without Docker, be easy to set up, and support both text and vector search. Google Colab was one of the environments I wanted to support.

I discussed the requirements and existing options with ChatGPT. SQLite text search fit many of them, so I looked for a way to add vector search to it. None of the options I reviewed met all my requirements. I chose locality-sensitive hashing, or LSH, because I understood it and had implemented random projections before. I wanted to be able to debug the implementation myself instead of relying on an AI assistant.

I also asked for an API that resembled minsearch. Course participants could then use a familiar interface instead of learning a new one. ChatGPT prepared a plan, which I saved in a GitHub repository as plan.md. Then I asked Claude Code to implement it and reminded it to include tests. This was how I handed the design over: the requirements and decisions were in a plan, and the implementation could be checked with tests.

SQLiteSearch stores its search index in one SQLite database file on disk. It runs in the Python process without a separate server, which gives me the persistence I needed while keeping the setup local and lightweight.
