# Designing memory for a long-running AI assistant

An LLM starts each conversation without knowledge of yesterday’s decisions. Sending the entire history every time is expensive, and irrelevant context can make answers worse. Retrieval augmented generation helps by selecting document chunks, but persistent assistant memory needs a few additional ideas: importance, time, navigation, and a way to load only what the conversation needs.

MemPalace, an open-source project by Milla Jovovich and Ben Sigman, organizes memory using the metaphor of a memory palace. The implementation runs locally with ChromaDB and PyYAML. Its memory layer uses regular expressions and keyword scoring instead of LLM calls, so classification and retrieval preparation are deterministic and free to run.

The hierarchy has several levels. A wing is a broad domain such as a project or person. Rooms divide a wing into topics like auth, billing, or planning. Halls classify the kind of memory, including facts, events, discoveries, preferences, and advice. Drawers contain the original text, stored in chunks of 800 characters with 100-character overlap. A tunnel links rooms with the same name across different wings. A closet is a compressed summary that points to its source drawers.

Room detection can use different evidence. For project files, the system checks the directory first, then the filename, and finally scores content keywords. For conversations, it counts keywords in categories such as technical, architecture, planning, decisions, and problems. Users can approve or edit assignments through configuration. This is a useful property of heuristics: the classification can be inspected and corrected.

Loading should be progressive. L0 is an identity file that the user writes and the assistant always reads. L1 selects important memories from the local database and creates a short essential story. L2 retrieves drawers for a specific wing or room when a topic appears. L3 falls back to semantic search when structured navigation is not enough. The initial context stays around 600 to 900 tokens, while deeper information is loaded only when needed.

Persistent facts need time. MemPalace stores entities and RDF-style triples in SQLite, with `valid_from` and `valid_to` fields. When a person moves, the old location can be closed and the new one added. A historical query can then return what was true on a particular date. Deduplication prevents an unchanged triple from being inserted repeatedly.

Compression is another option for reducing context. AAAK removes stop words, extracts topics, selects a short key sentence, and encodes entities, emotions, and semantic flags. It remains readable to an LLM without a special decoder. This treats the model as a decompressor while keeping the stored representation small.

The broader lesson is that memory is more than a vector index. A searchable collection is useful for static documents, but an assistant also needs a sense of importance, changing facts, connected domains, and token budgets. The reported benchmark results are claims from this project, not a guarantee for every memory system, but the architecture gives concrete places to test those ideas.
