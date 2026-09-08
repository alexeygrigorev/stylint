# A Small Search Library Between Memory and Infrastructure

SQLiteSearch grew from a gap between two kinds of search systems. minsearch was simple and supported text and vector search, but its index lived only in memory. Large services such as Elasticsearch offered more infrastructure than a small course project needed. The desired middle ground was local, persistent search in Python, with no Docker or separate service.

The requirements were specific. The library had to be available in Python, easy to set up, and usable in environments such as Google Colab. It also had to support regular text search and vector search. SQLite supplied the persistence because it is an embedded relational database included with Python’s standard library. A single database file could survive process restarts without introducing a server.

Text search was available through SQLite, but vector search required another design choice. An initial review found three imperfect options. lshashing was pure Python but stored hash tables in memory. SparseLSH supported Redis, LevelDB, and BerkeleyDB, but not SQLite. narrow-down used SQLite but depended on a native Rust extension. Each solved part of the problem and missed another requirement.

The implementation therefore used locality-sensitive hashing, or LSH, for vector search. LSH groups similar vectors so a search can narrow the candidates quickly. The author chose random-projection techniques already familiar to him instead of a more complex method, because understanding the algorithm made debugging possible without depending on an AI assistant. The public API was designed to resemble minsearch, reducing the amount that course participants had to learn.

The development process separated research, planning, and implementation. ChatGPT helped compare existing solutions and turn the conversation into a plan. The project began as LightSearch and was renamed SQLiteSearch before publication because a similar name was already taken on PyPI. The plan was saved in a GitHub repository, and Claude Code read `plan.md` and implemented the library. Tests were included as part of the library work.

The final index lives in one SQLite file. That file contains application data, structures for fast lookup, and search metadata. SQLite reads and writes directly from the Python process, so there is no database server, network layer, background daemon, cluster management, or JVM configuration. The tradeoff is its intended scale: the library was designed for small personal and course projects where persistence and low operational complexity mattered more than production search infrastructure.

Publication used another reusable workflow. A Claude Code `/release` command automates the Python package pipeline, and `/init-library` can create a project with packaging files, tests, a command-line interface, and CI/CD. When a build fails, Claude diagnoses the problem, changes configuration or tests, and reruns the pipeline. The goal is not to hide the release process, but to make it repeatable.

SQLiteSearch therefore occupies a deliberate middle position. It keeps the API and local simplicity of a small library while adding persistence, then adds vector search without requiring a separate service. Its value comes from matching the constraints of the project rather than trying to replace systems built for a different scale.
