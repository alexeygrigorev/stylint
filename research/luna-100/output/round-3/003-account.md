# Projects from Demo Day

On December 15 I hosted an AI Bootcamp Demo Day. Four students and I presented projects built during the first cohort. The goal was to move beyond prompts and build applications that connect models to databases, tools, and messy data.

I started with a reference to-do agent, using Lovable for the frontend and FastAPI for the backend. I built it to help students understand the project requirements.

The agent uses the backend's OpenAPI specification rather than RAG. The model can call tools to list tasks or mark them complete. Logfire records the session, tools, and cost, and 18 pytest tests check cases such as choosing the right tool for today's tasks.

Scott DeGeest built a Cybersecurity Disclosure Agent for supply-chain professionals who need to find reports of data breaches or ransomware attacks. It downloads SEC filings in XML and PDF, handles invalid XML, and indexes the normalized data in Elasticsearch.

The agent also needs to associate subsidiaries such as Change Healthcare with a parent such as UnitedHealth Group. Scott monitors input and output tokens because context limits and cost matter for this workflow.

Carlos Pumar-Frohberg's User Satisfaction Analyst works with Stack Exchange data about interface discussions to find what frustrates people using them. A Docker pipeline stores unstructured records in MongoDB and graph data in Neo4j. An orchestrator routes "what" and "how" questions to a MongoDB agent and relationship questions to a Cipher agent that writes graph queries. Carlos noticed that the orchestrator sometimes calls both to be safe.

Vanchesca Dinh built a Habit Builder using Huberman Lab podcasts and medical publications. She wanted to help people identify goals and understand why they wanted to pursue them.

Her pipeline downloads RSS feeds, transcribes audio with Faster Whisper, and stores embeddings in Qdrant. A tool rewrites each user query three ways to improve retrieval. She uses Logfire for logging, with Pydantic providing structure.

She also showed a problem with the agent's behavior. It would follow unrelated requests such as drawing a pig or translating text into Romanian, so she needed guardrails around its intended use.

Asia Amodeo built an intelligent email agent and couldn't attend, so I presented it. It fetches Gmail messages, indexes them in Elasticsearch, and exposes a Streamlit chat interface. Users can ask about particular messages or what matters today. The current focus is reading and fetching, with the broader aim of reducing email fatigue.
