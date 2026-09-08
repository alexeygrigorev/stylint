The second cohort of my AI Engineering course finished a few weeks ago, and in this post I want to share with you what we built. The projects are real-life and include personal assistants, professional tooling, and health-case assistants.

Some of us presented the projects live a few weeks ago on the demo day, so we’ll start with them.

### 1) bAIpacking Agent by Eduardo Gonzalo Almorox


Edu’s [bAIpacking Agent](https://github.com/edugonzaloalmorox/baikpacking-agent) helps long‑distance cyclists decide which tires, drivetrain, and bags to use for specific races. The agent scrapes event reports from [DotWatcher](https://dotwatcher.cc/) (a platform for bike races), stores them in PostgreSQL, and builds a RAG pipeline.

On the backend side, FastAPI resolves the event name, finds similar events, retrieves rider setups, and summarizes evidence. Then the results are presented via a Reflex UI.

Evaluation runs offline: each recommendation call is logged and later scored by a judge script.

### 2) Meal‑Map by Pavlo Skorodziievskyi


Pavlo’s [Meal‑Map](https://github.com/elgrassa/CapstoneMealMapSimplified) is a meal planner for an entire family. It takes into account dietary preferences, goals and allergies. The output is a list for grocery shopping as well as a list of recipes.

The knowledge base consists of 4 public‑domain nutrition sources chunked into 28 documents. The agent interacts with the knowledge base using 9 tools such as nutrition lookup, recipe search, and meal‑plan generation.

Evaluation uses a hand‑crafted ground-truth set, an LLM judge, and a search parameter sweep to tune retrieval. The agent limits calls to 20 LLM requests per session and $0.50 of cost per day; once exceeded, it downgrades to deterministic logic.

### 3) Engineering Decision Memory Agent by Camila Gaitan Mosquera


Engineering Decision Memory Agent helps engineering teams recover context from past technical decisions. It indexes ADRs (architecture decision records), RFCs (request for comments), and postmortems so engineers can ask questions like “Why did we move from a monolith to microservices?” or “Why was Kafka chosen over SQS?”

The flow for the demo:

* Camila indexed around 21 documents.
* The system split them into overlapping chunks, embeded them with a Hugging Face model, stored them in ChromaDB.
* On user query, the system retrieves the most relevant chunks for a question, and passes them to Claude as context.
* Claude returns a structured JSON response that maps directly to UI cards: decision, alternatives considered, tradeoffs, context and constraints, and source documents.

Camila also built a monitoring dashboard with queries per day, answers found vs. not found, latency distribution, token usage, interaction history, and basic thumbs-up feedback. Her next step is to rebuild the same agent with [spec-kit](https://github.com/github/spec-kit) to define clearer requirements, constraints, and implementation details.

### 4) VoiceIssue Agent by Mladen Maric


The [VoiceIssue Agent](https://github.com/lomodev-mmaric/voice_issue_code) lets users create GitHub issues via voice through Telegram.

When you have a lot of projects, keeping track of ideas is difficult, especially when you’re away from your computer. The agent simplifies this process by letting you use voice notes: you simply dictate your idea, and the bot assigns it to appropriate project. Before making any actions, the bot asks for a confirmation.

Everything is deployed via Docker Compose. Additionally, services include an interface for managing secrets, a session dashboard connected to the PostgreSQL log database, and a Grafana dashboard for analyzing cost and latency. There’s also an LLM‑as‑judge container that scores each session to filter out low-quality requests.

### 5) Medical Transcription App by Spyros Koumarianos


Spyros developed an app for clinicians to turn doctor-patient sessions into actionable [SOAP notes](https://www.ncbi.nlm.nih.gov/books/NBK482263/). This is information is sensitive, so it’s important to do everything locally. The app transcribes with a local Whisper model, performs basic diarisation (speaker disambiguation), and summarizes the discussion into a SOAP note using a local Llama model.

Operating entirely offline, doctors can disconnect their computers from the internet and create notes without transmitting audio to any server. Processing a three-minute recording takes around ten minutes on regular hardware without any GPUs.

Some of the projects weren’t presented live on the Demo day. I’ll describe them here too.

### 6) Cyber Sachet by Nirajan Acharya


[Cyber Sachet](https://github.com/nirajanacharya/Cyber-Agent) is a bilingual AI assistant for cybersecurity awareness. The agent targets Nepali users who need guidance on phishing, social engineering, and legal penalties. In Nepal, this information is scattered and often available only in English.

It uses a local knowledge base and selects tools based on the user’s intent, such as semantic search, law search, or penalty check. Responses are provided in both English and Nepali and include citations.

It uses Logfire for monitoring, and includes an LLM judge to measure accuracy, precision, and recall. The app is deployed on Streamlit Cloud for evaluation.

### 7) SnapSplit by James Watkins

SnapSplit is an AI‑powered receipt‑splitting app.

The target users are people who go to restaurants often, and often with the same group of friends. You upload a picture of a restaurant bill, and a vision model extracts the line items. Then the system understands who each dish belongs to and then splits the bill.

If any mismatches are detected, it re-runs OCR with specific hints and escalates to human review if needed.

### 8) AMR Awareness Platform by Juan Perez Prim


Juan’s [Antimicrobial Resistance (AMR) Awareness Platform](https://github.com/juanpprim/amr_ai) educates users about the causes, risks, and prevention of AMR.

A pipeline ingests data from 15 sources, including WHO, CDC, FAO, PubMed, and Our World in Data, and converts HTML and PDF documents into Markdown. The text is chunked and embedded with BioBERT. Retrieval combines BM25 keyword search with BioBERT semantic search via reciprocal rank fusion.

A PydanticAI agent, backed by Claude, answers questions with citations via a Gradio interface.

### 9) AI Regulation Research Assistant by Léonore Tideman


[AI Regulation Research Assistant](https://github.com/LEMTideman/MyAgent) helps practitioners navigate AI compliance across European, US, and Dutch jurisdictions.

The pipeline:

* A scope guard filters out off-topic prompts.
* The agent uses a local retrieval system over a curated corpus before performing a web search.
* The web search utilizes Brave Search combined with Jina Reader to fetch and clean page content.
* The agent connects to [Ansvar](https://ansvar.eu/)’s external legal data services (EU, US, Dutch, and automotive regulations) and uses them to answer legal questions.

Integration tests ensure the agent routes questions correctly, and an LLM judge scores answers against structured compliance criteria.

I’m really happy to see these projects! We’ve already started Cohort 3 (now we’re finishing week 3). I’m very excited to see what we will build this time!

If you’re planning to enroll in the next edition of the course, join the mailing list. I don’t know when exactly I’ll run it, but you’ll be the first to know about it.

[Join Mailing List](https://maven.com/alexey-grigorev/from-rag-to-agents)
