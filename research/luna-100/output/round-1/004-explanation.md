# What These Five Agent Projects Had in Common

The AI Bootcamp Demo Day projects show what changes when an AI application has to do more than answer a prompt. Each system connected a model to data, tools, or both. The details differed, but five practical patterns appeared across the demonstrations.

First, an agent needs a clear interface to the application around it. In the to-do reference project, the model received the backend’s OpenAPI specification. That description was enough to expose tools for reading tasks and completing them, without adding a RAG system or a separate knowledge base. The project also had 18 pytest tests, including checks that a question about today’s tasks led to the appropriate tool. The specification described what the backend could do; the tests checked whether the agent selected it correctly.

Second, real data arrives in inconvenient formats. Scott DeGeest’s cybersecurity agent downloaded SEC disclosures as XML and PDF files. Some XML was valid and some was not, so the ingestion code had to account for both. The converted records went into Elasticsearch. The application also needed a relationship that would not be obvious from a single document: Change Healthcare was treated as related to United Health Group. Handling a file and handling an organization’s subsidiaries were separate data problems.

Third, routing is useful when the questions need different kinds of storage. Carlos Pumar-Frohberg collected Stack Exchange discussions in MongoDB for unstructured text and Neo4j for graph relationships. An orchestrator sent “what” and “how” questions toward MongoDB, while relationship questions went to a Cipher agent that produced graph queries. In practice, the orchestrator often called both agents, because it preferred extra coverage over making a risky single choice.

Fourth, retrieval can be improved before the search itself. Vancesca Dinh’s Habit Builder used podcast episodes and medical publications. RSS feeds were downloaded, audio was transcribed with Faster Whisper, and embeddings were stored in Qdrant. She added a tool that rewrote each user query in three ways before searching. This was paired with Logfire and Pydantic, so the system had visibility and structured data around the model calls.

Vancesca’s demo also shows why guardrails belong in the design. The agent followed requests to draw a cute pig or translate text into Romanian even though those actions were outside the habit-building purpose. A model can be obedient and still be wrong for the application. The intended task has to be represented in the system’s boundaries.

Finally, a useful agent can start with a narrow read-only job. Asia Amodeo’s email agent fetched messages through Gmail, indexed them in Elasticsearch, and provided a Streamlit chat interface for finding emails or identifying what was important. It focused on reading rather than changing the inbox. That limited scope still addressed email fatigue and made the system easier to inspect.

Together, these examples describe an engineering workflow rather than a single agent recipe: define tools, normalize messy inputs, choose storage for the question, improve retrieval, observe model behavior, test routing, and set boundaries. The projects came from a cohort trying to build end-to-end applications, so the hard parts were visible around the model instead of hidden behind a prompt.
