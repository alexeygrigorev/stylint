# Designing a Persistent Search Library Without a Server

A useful way to choose a search tool is to start with the constraints of the project. SQLiteSearch was designed for small personal and course projects that need persistence without full infrastructure. It occupies the middle ground between an in-memory library such as minsearch and systems such as Elasticsearch or Qdrant.

## Begin with explicit requirements

The library needed to be available in Python and easy to set up. It also had to run locally without Docker, which matters in environments such as Google Colab. Finally, it needed both regular text search and vector search.

Those requirements ruled out some otherwise capable choices. Elasticsearch was described as a large production system and could cost more than $200 per month, which was excessive for this scale. Qdrant and PostgreSQL were possible alternatives, but using them here would require an external service or Docker. A small project shouldn't inherit that operational work unless it needs the capabilities.

The existing minsearch library already offered a simple API for both text and vector search. Its limitation was persistence: it stored the index in memory, so the data disappeared when the Python process ended. A persistent ingestion pipeline needed an index that survived a restart.

## Separate text search from vector search

ChatGPT suggested SQLite text search because SQLite is embedded in Python and can store data locally. SQLite solved the storage and text-search parts, but it didn't provide vector search by default. I therefore checked libraries that might add vector search while keeping SQLite as the backend.

Each candidate missed a requirement. lshashing was pure Python, but its hash tables stayed in memory. SparseLSH supported Redis, LevelDB and BerkeleyDB, yet not SQLite. narrow-down supported SQLite, but it used a native Rust extension rather than remaining pure Python. Since no option matched the complete list, a new library became the practical choice.

## Choose an algorithm you can explain

The vector-search design used locality-sensitive hashing, or LSH. I had implemented random projections several times, so I understood the basic approach and could debug it directly. That familiarity mattered more than choosing a newer or more complex technique whose behavior I would have to understand through an assistant.

The API was designed to resemble minsearch. Buildcamp participants could then use a familiar interface while learning how the persistent version worked. The implementation plan began as LightSearch and was renamed SQLiteSearch before publication because litesearch was already taken on PyPI.

ChatGPT helped research options, refine the design and produce a summary followed by a detailed plan. I put the plan in a repository, renamed `summary.md` to `plan.md`, and asked Claude Code to read it and implement the library. I also asked for tests, since a reusable library needs checks around its behavior.

## Understand the operational tradeoff

SQLiteSearch stores data tables, lookup structures and search metadata in one SQLite file. SQLite runs inside the Python process, so the setup has no separate server, network layer or background daemon. The package can therefore provide persistent search without cluster management, JVM tuning or Docker configuration.

That simplicity defines the intended scope. The library is useful when a personal or course project needs a local persistent index, while larger systems still make sense for larger production requirements. A release command can automate the final workflow. `/release` builds and publishes the Python package. It can also let Claude diagnose build or test failures and rerun the pipeline until it passes.
