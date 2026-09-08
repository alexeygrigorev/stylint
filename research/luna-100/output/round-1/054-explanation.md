# Nine ways to turn RAG and agents into applications

Course projects become easier to understand when each one connects a user problem to a data source, tools, and an evaluation method. The second AI Engineering cohort produced nine such examples.

bAIpacking helps cyclists choose equipment for a race. It retrieves evidence from DotWatcher reports, stores it in PostgreSQL, and uses FastAPI to resolve events, find similar races, and summarize rider setups. Meal-Map plans family meals from 28 nutrition documents and exposes nine tools. It limits sessions to 20 model calls and $0.50 per day, then falls back to deterministic logic. Both projects show why a useful agent needs an explicit operating limit.

An Engineering Decision Memory Agent addresses a different retrieval problem. Instead of answering from a general corpus, it searches architecture decisions, RFCs, and postmortems. Camila’s demo indexed about 21 documents and returned structured fields for decisions, alternatives, tradeoffs, constraints, and sources. Monitoring recorded latency, token usage, answers found, and feedback.

VoiceIssue shows how an agent can turn unstructured capture into an action. A user dictates an idea in Telegram, the system assigns a project, and the user confirms before a GitHub issue is created. Medical Transcription takes the opposite approach to deployment: it stays offline. Local Whisper, diarisation, and Llama produce SOAP notes without sending audio to a server, though a three-minute recording takes around ten minutes on ordinary hardware.

Cyber Sachet serves Nepali users who need cybersecurity guidance in English or Nepali. It selects semantic search, legal search, or penalty tools based on intent and includes citations. SnapSplit uses vision to read a restaurant receipt, assign dishes to people, rerun OCR when needed, and escalate mismatches to a human.

The AMR Awareness Platform combines 15 sources, including WHO, CDC, FAO, PubMed, and Our World in Data. It converts HTML and PDFs to Markdown, uses BioBERT embeddings with BM25 and reciprocal rank fusion, and answers through a PydanticAI agent with citations. The AI Regulation Research Assistant adds a scope guard, local retrieval, Brave Search, Jina Reader, and external legal services for EU, US, Dutch, and automotive regulations.

Across the projects, evaluation is part of the design. There are offline judges, ground-truth sets, retrieval sweeps, dashboards, integration tests, cost limits, and human review. RAG supplies context, but the application still needs routing, structured outputs, monitoring, and boundaries. The projects do not all solve the same problem, and that is why they are useful examples: an agent architecture follows the user’s data and risk rather than a fixed recipe.

The student projects also show why deployment choices matter. A local medical assistant and a hosted regulation assistant have different constraints, even when both retrieve documents and call a model. The engineering work is in connecting the model to the right data and deciding what the system is allowed to do.
