# MemPalace and the AI Memory Problem

Milla Jovovich unexpectedly entered a technical conversation I had been following about AI memory. She launched MemPalace, an open-source project, with developer Ben Sigman.

The project caught my attention because it treats memory as a local information problem. It avoids adding more model calls and infrastructure.

MemPalace draws on the classical memory-palace technique. Instead of keeping recalled information as an undifferentiated collection of chunks, it arranges it in spatial structures.

The project runs locally with ChromaDB and PyYAML as its dependencies. Its GitHub description reports 96.6% recall@5 on the LongMemEval benchmark.

The memory layer is deterministic. Classification, chunking, room detection, and compression use regular-expression heuristics and keyword scoring.

An LLM still handles conversation, answers questions, and generates responses. It's not responsible for deciding what to store, where it belongs, or what to retrieve.

Those operations therefore don't require an LLM API call.

That matters because language models are stateless. A new conversation doesn't know what happened yesterday or what a user prefers. It also forgets decisions made last week.

Putting the entire history into a context window is expensive and eventually ineffective. Context windows are finite, so irrelevant material competes for attention and every included token costs something.

The conventional answer is retrieval-augmented generation. Documents are split into chunks, placed in an index, and searched when a question arrives.

Search can use keywords, vector similarity, or both. That approach fits static collections such as documentation, books, and transcripts.

Persistent assistant memory is harder because memories have different importance, need structure over time, and may relate to one another.

MemPalace answers that problem with a hierarchy. Incoming information is assigned to rooms and levels, then compressed into a compact representation.

The system also builds a knowledge graph and a navigation graph, so retrieval can follow relationships instead of relying only on similarity. Its AAAK compression dialect is part of the mechanism for storing more information in less space.

MCP integration gives an assistant a standard way to use the memory system. Local execution makes the memory infrastructure free to run after installation. The operations are deterministic and visible.

It doesn't mean every memory problem is solved, and the benchmark number is a project-reported result rather than a guarantee for every workload.

What stayed with me was the division of labor. The model can remain responsible for conversation while a simpler, local system handles classification and retrieval.

A memory palace is a striking metaphor, but the practical idea is to give stored information structure before asking a model to reason over it. 
