# Five workflows behind practical AI agents

An agent becomes useful when it can connect a model to the data and actions required by a specific task. The projects from the first AI Bootcamp cohort used different workflows, and comparing them is more useful than treating "agent" as one architecture.

I built the reference to-do agent around the backend's OpenAPI specification. It doesn't use RAG because the model can use the API to retrieve tasks or mark them complete.

I used Logfire to record tool calls and their cost, and wrote 18 pytest tests for different requests. For example, I checked whether a question about today's tasks selected the expected operation. The frontend was prototyped in Lovable, with FastAPI providing the Python backend.

Scott DeGeest's Cybersecurity Disclosure Agent works with SEC filings to help supply-chain professionals find reported breaches or ransomware attacks. Those filings arrive as XML or PDF, and Scott needed to handle malformed XML before indexing the data in Elasticsearch.

He also needed to account for subsidiaries, associating Change Healthcare with UnitedHealth Group. He monitors input and output tokens to track context usage and cost.

Carlos Pumar-Frohberg's satisfaction analyst routes different questions to different stores. A Docker pipeline puts unstructured Stack Exchange records in MongoDB and graph data in Neo4j. He uses interface discussions to find what frustrates clients.

An orchestrator sends "what" and "how" questions to the MongoDB agent. Questions about relationships go to the Cipher agent, which translates natural language into graph queries. Carlos found that the orchestrator often calls both agents to be on the safe side.

Vanchesca's habit builder uses Huberman Lab podcasts and medical publications to help people understand their goals. She downloads RSS feeds and transcribes audio with Faster Whisper, then stores embeddings in Qdrant. A query-rewriting tool creates three search variants to improve retrieval.

She uses Logfire for logging, with Pydantic providing structure. During the demo, she showed that the agent could be persuaded to draw a pig or translate text into Romanian. It followed those instructions even though they had nothing to do with helping people form habits.

Asia Amodeo's email agent applies a familiar workflow to Gmail. It fetches messages, indexes them in Elasticsearch, and uses Streamlit for questions about the inbox. The system currently focuses on reading and retrieving information. Asia wanted to reduce email fatigue by helping people find particular messages or work out what mattered that day.
