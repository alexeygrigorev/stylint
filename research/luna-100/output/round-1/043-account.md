# An unexpected look at AI memory

Milla Jovovich and developer Ben Sigman launched MemPalace, an open-source project that made me look again at how an AI assistant can remember. I found the project through the recent discussion around it and read the repository to understand the design. The interesting part is that the memory layer does not depend on an LLM call. It runs locally, uses deterministic heuristics, and still reports 96.6% recall@5 on LongMemEval.

The project borrows the memory palace idea. Instead of putting every past conversation into one flat index, it organizes information as wings, rooms, halls, and drawers. A wing can represent a project, person, or broad topic. A room is a category such as auth or planning. A hall identifies the type of memory, for example a fact, event, preference, discovery, or advice. The drawer is the original text chunk, kept verbatim.

There are also tunnels. If the same room appears in multiple wings, MemPalace creates a connection between those areas. A closet stores a compressed representation that points back to the original drawers. This structure is intended to make related information discoverable without asking semantic search to do everything.

The project uses ChromaDB and PyYAML as its two dependencies. Classification, chunking, room detection, and compression use regular expressions and keyword scoring. The LLM remains available for the conversation itself, but the memory infrastructure can run offline. The repository contains 21 Python modules, with no server, graph database, or API key required for the memory layer.

The four loading levels are designed around token cost. L0 is a manually written identity file of about 100 tokens. L1 selects the most important stored memories and produces an essential story of roughly 500 to 800 tokens. L2 loads a topic on demand, and L3 performs a deeper ChromaDB search. The wake-up context is around 600 to 900 tokens, leaving most of the model context available for the current conversation.

MemPalace also keeps a temporal knowledge graph in SQLite. Facts have `valid_from` and `valid_to` dates, so a query can ask what was true at a particular time. When a fact changes, the old triple expires and a new one is inserted. That is a useful distinction from a memory store that only knows the latest text.

The most unusual part is AAAK compression. It removes common words, encodes entities and emotions with short codes, and tags a note with semantic flags. The result is much smaller while remaining readable to an LLM. The project claims that the hierarchy improves retrieval from 60.9% to 94.8% over flat vector search. Whether those numbers transfer to another system is a separate question, but the design makes a clear argument: organization, time, and token budgets belong in memory architecture.
