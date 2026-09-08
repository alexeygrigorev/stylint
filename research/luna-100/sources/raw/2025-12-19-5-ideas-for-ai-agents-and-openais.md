## One Idea I Want to Share

On December 15, I hosted the [AI Bootcamp Demo Day](https://www.youtube.com/watch?v=7RlT8EJH0do), a live event where graduates from the first iteration of the [AI Bootcamp](https://maven.com/alexey-grigorev/from-rag-to-agents) showcased their final projects.

The goal for this cohort was to move beyond simple prompts and build robust, end-to-end AI applications and agentic workflows: systems that allow AI models interact with databases, manage external tools, and handle messy real-world data.


Asked Gemini to illustrate the AI Bootcamp Demo Day and got another cool image

Four students and I presented what we’ve been building over the last couple of months.

In this post, I want to walk through the architecture, the tech stacks, and the specific engineering challenges we solved in these projects.

### 1. To-Do List Agent

I started by presenting a reference project I built to help students understand the requirements. The idea is an [agent that interacts with a simple to-do list application](https://github.com/alexeygrigorev/my-daily-tasks-agent). I used Lovable to prototype the frontend and FastAPI (Python) for the backend.


The agent does not use RAG or a knowledge base. Instead, it relies on the backend's OpenAPI specification. I fed this specification to the model so it could create tools to get tasks or mark them as complete. To monitor the system, I used Logfire, which tracks the entire session, including the specific tools used and the cost of each interaction. I also wrote 18 tests using pytest to cover different scenarios, like checking if the right tool is invoked when asking about today’s tasks.

### 2. Cybersecurity Disclosure Agent by Scott DeGeest


Scott’s Cybersecurity Disclosure Agent generating a reply

Scott, a Principal Data Scientist who studies supply chains, built an agent to track cybersecurity incidents reported to the SEC (Securities and Exchange Commission). The goal is to help supply chain professionals quickly find out if a company has disclosed a data breach or ransomware attack.

The system downloads raw files, often in XML or PDF format, from the SEC website. Scott had to build logic to handle valid and invalid XML structures. The data is then converted and indexed in Elasticsearch. One interesting challenge was handling subsidiaries; the agent needs to know that “Change Healthcare” is related to “United Health Group.” He also added a monitor for input and output tokens to keep an eye on costs and context limits.

[Scott’s LinkedIn](https://www.linkedin.com/in/dscottdegeest/)

### 3. User Satisfaction Analyst Agent by Carlos Pumar-Frohberg


A detailed architecture and processes described for Carlos’ project

Carlos wanted to analyze client satisfaction using data from Stack Exchange. He focused on user interface discussions to find frustration patterns.

His architecture uses a Docker pipeline to fetch data and dump it into two places: MongoDB for unstructured data and Neo4j for graph data. The system uses an “orchestrator” agent to decide where to route user questions. If the question is about “what” or “how,” it goes to a MongoDB agent. If it is about relationships, it goes to a “Cipher” agent that translates natural language into graph queries. Carlos noted that the orchestrator often decides to call both agents simultaneously to be on the safe side.

[Carlos’ LinkedIn](https://www.linkedin.com/in/carlos-pumar-frohberg/)

### 4. Habit Builder Agent by Vancesca Dinh


Architechture of Vancesca’s habit builder agent

Vanchesca created a “Habit Builder” agent. It helps users identify goals and understand the “why” behind them, grounded in data from the Huberman Lab podcast and medical publications.

She engineered a detailed data pipeline: downloading RSS feeds, transcribing audio with Faster Whisper, and storing embeddings in a Qdrant vector database. For the agent itself, she implemented a tool that rewrites user queries three different ways to improve search results. She also utilized Logfire for logging and Pydantic for structure. A key part of her presentation showed the need for guardrails, as she found the agent would obediently “draw a cute pig” or translate text into Romanian if asked, which was not the intended use.

[Vancesca’s LinkedIn](https://www.linkedin.com/in/vancesca-dinh/)

### 5. Personalization: Intelligent Email Agent by Asia Amodeo


Asia’s Streamlit interface to interact with her agent

Asia could not attend, so I presented her project. She built an intelligent email agent designed to help manage an inbox.

The agent integrates with the Gmail API to fetch emails and indexes them in Elasticsearch. It features a chat interface built with Streamlit, where you can ask questions to find specific emails or see what is important for the day. While it currently focuses on fetching and reading, the concept addresses “email fatigue” by making it easier to sift through communication.

[Asia’s LinkedIn](https://www.linkedin.com/in/asiaamodeo/)

If you want to see the full demos, you can watch the recording here:

And if you are interested in building reliable systems like this yourself, I’m opening the next iteration of the [AI Bootcamp](https://maven.com/alexey-grigorev/from-rag-to-agents) on January 26, 2026.

By the way, the end of the year is a good time to review your learning budget. If your company offers a learning budget and you haven’t used it yet, now is usually the easiest moment to do so. You can expense my AI Bootcamp: I’ve prepared a [short message](https://docs.google.com/document/d/12LBC7KBR_NE-ehSf7YTOOTlMgPD_0g-KU7g5KxTxpbs/edit?usp=sharing) you can send to your manager to request approval.
