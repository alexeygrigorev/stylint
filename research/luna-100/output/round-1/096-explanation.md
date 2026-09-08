# How the AI Dev Tools Course Is Organized

That continuity helps students see why each operational decision matters.

It also makes the final project less disconnected from the earlier exercises.

The sequence is useful because each module leaves a more complete system than the previous one. Students do not learn deployment as an isolated command or evaluation as a separate theory; they apply both to the same application they have been developing.

The AI Dev Tools Zoomcamp uses one project to teach a complete development lifecycle. The modules are ordered so the student first learns how to direct an agent, then builds and deploys an application, operates it, and finally extends the agent workflow.

Module 1 is about specifications, context, loops, and roles. Turn a vague idea into a document and backlog. Store project rules in durable context. Separate product management from implementation and QA, and use checkable conditions when a loop should continue. The result is a process for reviewing generated work.

Module 2 applies that process to a local full-stack app. Build the frontend, define OpenAPI, implement the backend, add SQLite, and test behavior. A generated implementation is not accepted because it looks plausible. Compare it with the specification and test the behavior that matters.

Module 3 covers the seams between components. Add integration and end-to-end tests, switch to Postgres, containerize the application, and run checks in CI. Deployment turns the local project into a public service. A documented rollback path is part of the result.

Module 4 adds operating discipline. Deploy every change to development, then promote a tested version to production. Collect metrics, logs, and traces with OpenTelemetry. Display them in Grafana and alert on sustained user impact. An AI agent can investigate a bounded evidence packet, while code enforces permissions and allowed actions. Security audits and incident records complete the operational context.

Module 5 focuses on coding-agent capabilities: instructions, MCP, reusable skills, hooks, subagents, plugins, and custom agents. The goal is to understand each capability well enough to use it across tools. Students document permissions, guardrails, and the way a specialist fits into the project.

The course is free and can be followed independently, but a live cohort adds deadlines, peer review, office hours, a leaderboard, and certificates. Homework exercises help students keep pace. The final project must demonstrate a frontend, backend, API specification, persistent storage, tests, containers, public deployment, and clear setup instructions. It must also explain how AI contributed and how the student reviewed the result.

When a problem appears, the course platform handles deadlines and submissions, GitHub holds materials, Slack supports questions, and the FAQ collects previous answers. This separation gives each activity a place and keeps the learning process reproducible.
