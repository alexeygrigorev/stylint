# Memory Needs More Than Chunk Search

An AI assistant starts every conversation with a basic limitation: its language model is stateless. Without an external system, it can't remember a project decision from last week. It also can't put a preference from yesterday back into context.

Use a retrieval index for this problem. RAG splits documents into chunks, searches them with keywords or embeddings, and gives selected text to the model.

That fits FAQs and documentation. Books and transcripts work too, while agent memory needs more structure.

Memories don't all have the same importance, change over time, and may connect to one another.

MemPalace approaches the problem through the memory-palace idea. The open-source project, launched by Milla Jovovich with developer Ben Sigman, organizes information into spatial structures.

It runs locally with ChromaDB and PyYAML as its two dependencies.

The project reports 96.6% recall@5 on LongMemEval, useful evidence about its design but not a universal guarantee.

The key design choice is to keep the memory layer deterministic. Regular-expression heuristics and keyword scoring handle classification, chunking, room detection, and compression.

The assistant still uses an LLM to answer questions and generate conversation. The LLM isn't called to decide what to save, where to place it, or which memories to retrieve.

You can think of the workflow as four stages: incoming text is divided into meaningful pieces first.

Second, the system detects the room and level where a piece belongs. Third, it compresses the representation using the project's AAAK dialect.

Finally, retrieval can navigate the resulting structures and knowledge graph. A separate navigation graph helps the system follow relationships instead of treating every chunk as an isolated search result.

This structure addresses weaknesses of naive context stuffing because a context window is finite.

Irrelevant history makes reasoning harder, and the user pays for every token included. A plain similarity search can find related text while missing the broader relationship that gives the fact meaning.

Rooms, levels, and graphs provide additional evidence before the model receives context.

The local design changes the cost model. After installation, memory operations don't require an LLM API call. They run locally.

The operations are deterministic and can be checked independently of the conversation model. MCP integration provides a standard interface for an assistant to use the system, while the conversational model remains replaceable.

"Memory" doesn't have to mean a larger prompt or a more elaborate chain of model calls.

It can mean choosing a representation, enforcing classification rules, and building navigation links before generation begins. MemPalace still needs retrieval evaluation. The memory layer can be measured and changed separately from the model that talks to the user.
