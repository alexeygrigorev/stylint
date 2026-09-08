# From a Vague Idea to a Running Product

I use a staged process when I take an idea to production with coding agents. The AI Dev Tools Zoomcamp presents it in three stages. They're Build, Deploy, and Operate.

The sequence is tool-agnostic, so I can change the assistant or language while keeping the same boundaries. The framework, cloud, and observability service can change too.

I usually start a new session for each step. The agent then has only the context needed for that task.

The Build stage starts with a specification. I use ChatGPT in dictation mode to explain an idea, answer questions, and turn the discussion into `_docs/specs.md`.

Then I build the frontend before the backend, using mock data and one service layer for backend calls. A clickable interface is a cheap way to see whether the idea makes sense.

Before writing the backend, I define a manual test scenario. For a study-group application, it might include signing up and creating a group with an event.

The scenario then joins from another browser and checks that the first session sees the result. I keep it as a reference while the system changes.

I also add `AGENTS.md` with focused commit guidance so new sessions have project context. The frontend service layer becomes the OpenAPI specification.

I ask the agent to describe endpoints and methods. It also records paths, request and response bodies, and authentication.

Then I choose a backend stack and save the decision. The backend starts with a seeded in-memory store, authentication, and tests. A Makefile hides the commands I otherwise forget.

Once the frontend talks to the real backend, I replace the store with SQLite and an ORM. The same manual scenario tells me whether integration still works. For deployment, I build the frontend into static files and serve them from the backend container.

Postgres replaces SQLite, and Docker Compose runs the application and database together. Integration tests check the backend and database.

An end-to-end Playwright test covers the browser, frontend, backend, and database in one flow.

I then choose a deployment platform and infrastructure-as-code option, and deploy the application. The CI/CD pipeline runs tests and builds the Compose stack. It executes integration and end-to-end checks, deploys, and verifies a health endpoint.

The Operate stage adds a second environment, manual promotion, and a registry image. It also adds OpenTelemetry, dashboards, alerts, and an on-call worker.

The complete sequence has 28 concrete steps.

I don't need a perfect production system before the first test. I need enough structure to learn what the product does and add reliability as its use requires.
