# Nine AI Engineering Projects from the Second Cohort

The second cohort of my AI Engineering course finished a few weeks ago, and I wanted to document what the students built. The projects covered personal assistants, professional tools and health-related assistants. Some students presented them on demo day, while others are included here because their systems showed useful engineering choices.

## Personal and professional assistants

Eduardo Gonzalo Almorox built bAIpacking Agent for long-distance cyclists choosing tires, drivetrains and bags for specific races. It scrapes event reports from DotWatcher, stores them in PostgreSQL and builds a RAG pipeline. FastAPI resolves an event, finds similar races and retrieves rider setups before summarizing evidence in a Reflex interface. Each recommendation is logged and later scored by an offline judge script.

Pavlo Skorodziievskyi's Meal-Map plans meals for an entire family while accounting for dietary preferences, goals and allergies. Four public-domain nutrition sources become 28 documents, and the agent uses nine tools for nutrition lookup, recipe search and meal-plan generation. Its evaluation combines a ground-truth set, an LLM judge and a retrieval-parameter sweep. The system limits a session to 20 LLM requests and $0.50 per day, then falls back to deterministic logic.

## Decision and voice tools

Camila Gaitan Mosquera built an Engineering Decision Memory Agent for recovering context from architecture decision records, RFCs and postmortems. She indexed around 21 documents, split them into overlapping chunks, embedded them with a Hugging Face model and stored them in ChromaDB. Claude receives the retrieved context and returns structured JSON for decision, alternatives, tradeoffs, constraints and sources. A dashboard tracks queries, unanswered results and latency. It also tracks token use, interaction history and thumbs-up feedback.

Mladen Maric's VoiceIssue Agent creates GitHub issues from Telegram voice notes. The user dictates an idea, the bot assigns it to a project and asks for confirmation before acting. Docker Compose runs the system. It also includes secret management and a PostgreSQL session dashboard. Grafana provides cost and latency monitoring.

An LLM judge filters low-quality requests.

## Health and public-interest systems

Spyros Koumarianos built a medical transcription app for clinicians. A local Whisper model transcribes doctor-patient sessions, basic diarisation separates speakers and a local Llama model turns the discussion into a SOAP note. The application runs offline so audio need not reach a server. A three-minute recording takes around ten minutes on regular hardware without GPUs.

Nirajan Acharya built Cyber Sachet, a bilingual cybersecurity assistant for Nepali users. It answers questions about phishing, social engineering and legal penalties using a local knowledge base and intent-selected tools. Responses appear in English and Nepali with citations. Logfire monitors the app, an LLM judge measures accuracy, precision and recall, and the evaluation deployment runs on Streamlit Cloud.

## More applied systems

James Watkins built SnapSplit to divide restaurant bills from a photo. A vision model extracts line items and assigns dishes to people. If mismatches appear, the system reruns OCR with hints and escalates to human review when needed.

Juan Perez Prim's AMR Awareness Platform educates users about antimicrobial resistance. It ingests 15 sources, including WHO, CDC, FAO and PubMed. Our World in Data is another source. The pipeline converts HTML and PDF material to Markdown.

It then combines BM25 with BioBERT semantic search through reciprocal-rank fusion. A PydanticAI agent backed by Claude answers with citations in a Gradio interface.

Léonore Tideman built an AI Regulation Research Assistant covering European, US and Dutch jurisdictions. A scope guard filters unrelated prompts. Local retrieval searches a curated corpus, while Brave Search with Jina Reader gathers web material. The agent also connects to Ansvar's legal data services.

Integration tests check routing, and an LLM judge scores answers against structured compliance criteria.
