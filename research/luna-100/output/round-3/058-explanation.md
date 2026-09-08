# Following the workshop library one section at a time

I collected eleven workshops in the AI Shipping Labs library so you can find them through one sign-up. The recordings had been on YouTube, with code on GitHub and other material in conference archives or Slack. Some conference workshops were never recorded, so those have written material without a video.

I also changed the notes from long READMEs into tutorials with separate parts. A single page works as a reference, but it makes a 90-minute workshop harder to follow across several study sessions.

Claude Code split each README into logical sections and adapted the headings to the platform. It added Mermaid diagrams where showing the architecture or data flow helped. I reviewed the results and corrected the parts that needed more work.

You can now follow the navigation between parts, track progress from your profile, and ask questions in the comments under a section.

## Search and agents

For search, you start with the DataTalks.Club FAQ documents. You build TF-IDF search and rank results with cosine similarity, then add embeddings for semantic search.

In the RAG workshop, you use tools that return snippets or open a full document. The model can search first and request the full text when a result looks useful.

You also build an agent using raw OpenAI calls before trying the Agents SDK and PydanticAI. You expose tools through MCP too. For coding agents, you work with filesystem tools and reusable skills, including an updated workshop that combines those topics.

You use Temporal to build a research agent over podcast transcripts, concentrating on reliable ingestion and system design. In the guardrails workshop, you add input and output checks to a FAQ assistant, including checks against off-topic requests and unsupported promises.

## Deployment and access

One deployment workshop takes a FAQ chatbot from a Jupyter notebook to FastAPI. You add a JavaScript frontend with SSE streaming, package the service with Docker, and deploy it to Railway. GitHub Actions handles CI/CD.

You replace FastAPI with a custom AWS Lambda runtime in the next workshop. The runtime serves the frontend and streaming API from a container deployed through a Lambda Function URL. Both workshops include the coding-agent prompts used during development.

Most workshops are free after sign-up. You need a membership for the deployment workshops, with written lessons available in Basic. Recordings are included in the Main and Premium plans.

The library also has a coding-tools comparison, using the same React Snake game task to compare different kinds of assistants.

## AI Hero

I moved the free seven-day AI Hero course from email to the website as well. Each lesson now has its own page and comments, and you can track completion through your profile.

The course covers search and RAG, then function calling, evaluation, and web deployment. You can earn a certificate by submitting a project and completing peer review.
