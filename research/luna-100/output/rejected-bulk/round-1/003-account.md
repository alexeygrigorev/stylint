# What We Showed at Demo Day



I want to describe what happened, because the sequence of small decisions is more useful than a polished summary. 

One Idea I Want to Share https://www.youtube.com/watch?v=7RlT8EJH0dohttps://maven.com/alexey-grigorev/fro

m-rag-to-agents showcased their final projects. The goal for this cohort was to move beyond simple

prompts and build robust, end-to-end AI applications and agentic workflows: systems that allow AI models

interact with databases, manage external tools, and handle messy real-world data. Asked Gemini to

illustrate the AI Bootcamp Demo Day and got another cool image Four students and I presented what we’ve

been building over the last couple of months. In this post, I want to walk through the architecture, the

tech stacks, and the specific engineering challenges we solved in these projects. 1. To-Do List Agent

https://github.com/alexeygrigorev/my-daily-tasks-agentPython for the backend. The agent does not use RAG

or a knowledge base. Instead, it relies on the backend's OpenAPI specification. I fed this specification

to the model so it could create tools to get tasks or mark them as complete. To monitor the system, I

chose Logfire, which tracks the entire session, including the specific tools used and the cost of each

interaction. I also wrote 18 tests using pytest to cover different scenarios, like checking if the right

tool is invoked when asking about today’s tasks. 2. Cybersecurity Disclosure Agent by Scott DeGeest

Scott’s Cybersecurity Disclosure Agent generating a reply Securities and Exchange Commission. The goal

is to help supply chain professionals quickly find out if a company has disclosed a data breach or

ransomware attack. The system downloads raw files, often in XML or PDF format, from the SEC website.

Scott had to build logic to handle valid and invalid XML structures. The data is then converted and

indexed in Elasticsearch. One interesting challenge was handling subsidiaries; the agent needs to know

that “Change Healthcare” is related to “United Health Group.” He also added a monitor for input and

output tokens to keep an eye on costs and context limits. https://www.linkedin.com/in/dscottdegeest/ 3.

User Satisfaction Analyst Agent by Carlos Pumar-Frohberg A detailed architecture and processes described

for Carlos’ project Carlos wanted to analyze client satisfaction using data from Stack Exchange. He

focused on user interface discussions to find frustration patterns. His architecture uses a Docker

pipeline to fetch data and dump it into two places: MongoDB for unstructured data and Neo4j for graph

data. The system uses an “orchestrator” agent to decide where to route user questions. If the question

is about “what” or “how,” it goes to a MongoDB agent. If it is about relationships, it goes to a

“Cipher” agent that translates natural language into graph queries. Carlos noted that the orchestrator

often decides to call both agents simultaneously to be on the safe side.

https://www.linkedin.com/in/carlos-pumar-frohberg/ 4. Habit Builder Agent by Vancesca Dinh Architechture

of Vancesca’s habit builder agent Vanchesca created a “Habit Builder” agent. It helps users identify

goals and understand the “why” behind them, grounded in data from the Huberman Lab podcast and medical

publications. She engineered a detailed data pipeline: downloading RSS feeds, transcribing audio with

Faster Whisper, and storing embeddings in a Qdrant vector database. For the agent itself, she

implemented a tool that rewrites user queries three different ways to improve search results. She also

utilized Logfire for logging and Pydantic for



That is the part I would keep from this example: connect each tool to the problem that made it necessary, and keep the limitation next to the claim. The details matter because they explain what can be reused and what was specific to this project.
