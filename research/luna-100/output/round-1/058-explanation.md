# A workshop library that supports learning in stages

Workshop material often starts as a README because that is the fastest way to publish code and notes. It is a poor format for learning from the beginning, though. A long page does not show where you are, and a 1.5-hour workshop has no natural place to stop. AI Shipping Labs’ workshop library addresses this by turning scattered recordings and repositories into structured tutorials.

The library collects eleven workshops in one place. Recordings that used to live on YouTube, code that lived on GitHub, and conference materials that were never recorded now share a platform and a single sign-up. Most workshops are free. The two deployment workshops are members-only, with written material in the Basic tier and recordings in higher plans.

The content was reformatted with Claude Code. For each workshop, the agent read the existing README, split it into logical parts, lifted headings into the platform structure, and added Mermaid diagrams where an architecture or data flow was easier to understand visually. I reviewed the results and corrected the parts that needed judgment. A small content migration could use one agent even though larger platform features use an agent team.

The workshop sequence begins with search and RAG. One tutorial builds a search engine from TF-IDF through cosine similarity and embeddings. Another builds an agent with `search()` and `get_file`, allowing the model to search snippets before opening a full document. Later workshops build agents with OpenAI, PydanticAI, MCP, Django tools, and reusable skills. A Temporal workshop focuses on reliable ingestion for a research agent over podcast transcripts.

Safety is its own topic. The guardrails workshop protects an FAQ assistant with input and output checks, blocks off-topic questions, and prevents unsupported promises such as deadline extensions. It ends with an asynchronous pattern that runs checks in parallel and cancels the agent when a check fails.

Deployment tutorials start from a notebook and end with running services. One wraps an FAQ chatbot in FastAPI, adds a JavaScript frontend with SSE streaming, containerizes it, deploys to Railway, and adds GitHub Actions. The Lambda workshop replaces FastAPI with a custom runtime and deploys a single container through a Lambda Function URL. Both include prompts used with the coding agent.

AI Hero was moved into the same structure. Its seven lessons used to arrive as daily emails, with no progress tracking or comments. The website gives each day a page, lets members ask questions, tracks completion, and awards a certificate after a project submission and peer review. The change is small technically, but it turns a sequence of messages into a course that can be revisited.

The result is a clearer path through the material. A learner can stop after one section, return later, see what is complete, and ask a question where it belongs.
