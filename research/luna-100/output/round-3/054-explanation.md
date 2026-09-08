# Patterns Across Nine AI Engineering Projects

The second AI Engineering cohort built projects for personal use, professional work and health-related tasks. The systems differ in their domains. Their designs repeatedly retrieve evidence, limit what systems do, evaluate outputs and keep a human involved when mistakes matter.

Eduardo Gonzalo Almorox's bAIpacking Agent helps long-distance cyclists choose tires, drivetrains and bags for races. It retrieves event evidence from DotWatcher through PostgreSQL and a RAG pipeline. FastAPI finds similar events and rider setups before a Reflex interface presents the summary. Each recommendation is logged for offline judge scoring.

Pavlo Skorodziievskyi's Meal-Map plans family meals around dietary preferences, goals and allergies. Its knowledge base has four public-domain nutrition sources split into 28 documents, and its agent uses nine tools. The system evaluates retrieval with a ground-truth set, an LLM judge and a parameter sweep. It also limits each session to 20 LLM requests and $0.50 per day, then falls back to deterministic logic.

Camila Gaitan Mosquera's Engineering Decision Memory Agent retrieves context from ADRs, RFCs and postmortems. Around 21 documents are chunked, embedded and stored in ChromaDB. Claude receives relevant chunks and returns structured cards for decisions, alternatives, tradeoffs, constraints and sources. A monitoring dashboard tracks unanswered queries, latency, tokens and feedback.

Mladen Maric's VoiceIssue Agent turns Telegram voice notes into GitHub issues. It assigns an idea to a project and asks for confirmation before creating the issue. Docker Compose runs the system, while session, cost and latency dashboards provide operational visibility. An LLM judge filters low-quality requests.

Spyros Koumarianos's medical transcription app keeps sensitive audio offline. Local Whisper transcribes a doctor-patient session, diarisation separates speakers and local Llama generates a SOAP note. A three-minute recording takes around ten minutes on regular hardware without GPUs.

Nirajan Acharya's Cyber Sachet answers Nepali cybersecurity questions in English and Nepali. It uses a local knowledge base and selects tools for semantic search, law search or penalty checks. Citations, Logfire monitoring and an LLM judge support the evaluation.

James Watkins's SnapSplit uses vision to read restaurant receipts and assign dishes to people. When mismatches appear, it reruns OCR with hints and escalates to human review. The escalation is part of the design rather than an afterthought.

Juan Perez Prim's AMR Awareness Platform combines BM25 keyword retrieval with BioBERT semantic retrieval through reciprocal-rank fusion. It ingests 15 sources, including WHO, CDC and FAO. The other sources include PubMed and Our World in Data. A PydanticAI agent backed by Claude answers with citations.

Léonore Tideman's AI Regulation Research Assistant covers European, US and Dutch jurisdictions. It uses scope guarding, local retrieval, Brave Search, Jina Reader and Ansvar's legal services. Integration tests check routing, while an LLM judge scores answers against compliance criteria.
