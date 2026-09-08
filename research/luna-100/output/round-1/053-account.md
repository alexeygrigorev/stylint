# What the second AI Engineering cohort built

The second cohort of my AI Engineering course finished a few weeks ago, and its projects covered personal assistants, professional tools, and health-related use cases. I want to describe the systems through the decisions their creators made, because the variety is a useful reminder that an agent is shaped by its data and constraints.

Eduardo Almorox built bAIpacking for long-distance cyclists. It scrapes race reports from DotWatcher, stores them in PostgreSQL, and uses a RAG pipeline to recommend tires, drivetrain, and bags. FastAPI resolves an event, finds similar races, retrieves rider setups, and summarizes the evidence. A Reflex interface presents the result. Every recommendation is logged and later scored by an offline judge.

Pavlo Skorodziievskyi’s Meal-Map plans meals for a family while considering preferences, goals, and allergies. Its knowledge base contains 28 documents from four public nutrition sources. The agent has nine tools for nutrition lookup, recipe search, and meal planning. Pavlo evaluates it with a hand-built ground truth set, an LLM judge, and retrieval parameter sweeps. A session is limited to 20 model calls and $0.50 per day, after which deterministic logic takes over.

Camila Gaitan Mosquera built an Engineering Decision Memory Agent. It indexes architecture decision records, RFCs, and postmortems so teams can recover why a choice was made. The demo used about 21 documents, split into overlapping chunks and embedded with a Hugging Face model in ChromaDB. Claude receives retrieved context and returns structured cards for the decision, alternatives, tradeoffs, constraints, and sources. A dashboard tracks queries, latency, token use, answers found, and feedback.

Mladen Maric’s VoiceIssue Agent creates GitHub issues from Telegram voice notes. It assigns an idea to a project and asks for confirmation before taking action. Docker Compose runs the services, while PostgreSQL stores sessions. A secrets interface, session dashboard, Grafana cost and latency view, and an LLM judge support operations.

Spyros Koumarianos built a local medical transcription app. It uses Whisper for transcription, basic speaker diarisation, and a local Llama model to produce SOAP notes. Everything runs offline, so audio does not leave the clinician’s computer. A three-minute recording takes about ten minutes on regular hardware without a GPU.

The remaining projects included Cyber Sachet for bilingual Nepali cybersecurity guidance, SnapSplit for extracting and assigning restaurant bill items, an AMR education platform using WHO and CDC sources, and an AI regulation assistant covering European, US, and Dutch jurisdictions. They all make different choices about retrieval, tools, citations, monitoring, and evaluation. That was the useful part of the demo day: the same course ideas became systems with very different boundaries.

Several projects also made their limits visible. The medical app traded speed for local processing, Meal-Map traded model freedom for a daily budget, and VoiceIssue asked for confirmation before changing a repository. Those details were part of the project designs rather than afterthoughts.
