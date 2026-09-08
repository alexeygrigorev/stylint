# Putting eleven workshops in one place

My Gen AI workshops had accumulated across YouTube, GitHub, conference archives, and Slack. Some had recordings, some only notes, and their code lived in separate repositories. I collected them in the Workshops section of the AI Shipping Labs website so one sign-up gives access to the library.

This update was part of a larger platform migration. The first site, built by Valeriia with v0 and Cursor, was a Next.js landing page with resources, a newsletter form, and checkout. More than 80 people signed up, which was enough to justify a platform with membership tiers, events, progress tracking, and profiles. I started moving the site to Django piece by piece.

The workshop library was a good first section because it solved both access and format problems. A long README can work as a reference, but it is difficult for someone learning from the beginning. There is no natural stopping point in a 1.5-hour workshop and no clear sense of progress. I asked Claude Code to turn each README into a multi-part tutorial with navigation, progress tracking, comments, and Mermaid diagrams where a visual explanation helped.

I reviewed each result and fixed what needed judgment. The contained reformatting task used one agent. Larger platform changes went through the agent team: PM grooming, SWE implementation, testing, and final PM acceptance. GitHub Issues track the work, and I add comments or new issues as the platform develops.

The eleven workshops cover search, RAG, agents, safety, deployment, and AI coding tools. The foundations start with building a search engine from the DataTalks FAQ and an agentic RAG pipeline. Other workshops build agents with MCP, PydanticAI, OpenAI, Django scaffolding, skills, and Temporal. The safety workshop adds input and output guardrails. Deployment workshops move a FAQ bot from Jupyter to FastAPI, Docker, Railway, CI/CD, and AWS Lambda.

Most workshops are free after sign-up. The two deployment workshops are members-only, with written materials in the Basic tier and recordings in higher plans. Membership also includes community access, group coding, mini-courses, and personal reviews.

I moved AI Hero to the platform too. It is a free seven-day course covering search, RAG, function calling, evaluation, and deployment. Previously one lesson arrived by email each day, which made progress and questions hard to track. Now each day is a page with comments, profile progress, and a certificate earned through a project submission and peer review. The migration changed the material from scattered references into something people can follow and revisit.

The update was therefore partly a content move and partly a change in how the material is learned. A recording can remain useful as a reference, but structured sections and progress markers make it easier to return to a workshop after a break.
