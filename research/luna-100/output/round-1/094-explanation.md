# A 28-Step Path to Production

The process remains inspectable at every boundary.

That is the main benefit.

The exact cloud provider is less important than the handoffs. A frontend should have a contract, a backend should have a testable store, and a deployed artifact should be the one that passed the checks. Those relationships are easier to reason about than a single large prompt.

The shortest useful way to use coding agents on a product is to keep the boundaries explicit. Start with a specification, build a testable frontend, define the API, implement the backend, and only then add persistence and operations. Each stage should leave something you can run.

In the build stage, discuss the raw idea with a chat assistant and save a specification. Generate a frontend with a single service layer and mock backend. Create a manual scenario that describes the user journey. Then derive an OpenAPI schema from the service layer, compare backend stack options, and save the choice before implementation.

Build the backend against the schema with an in-memory store, seeded data, authentication, and tests. Use a Makefile for repeatable commands. Connect the real frontend and run the manual scenario. Replace the store with SQLite and an ORM after the connection works. This order makes it clear whether a failure belongs to the interface, API, or persistence.

The deployment stage begins by putting the frontend’s built static files and backend in one container. Add Postgres for production and Docker Compose for local management. Integration tests should exercise backend and database interaction. End-to-end tests should start in the browser and verify the complete path to the database. Choose a cloud and infrastructure-as-code method, deploy, and add CI/CD that runs tests, builds, deploys, and checks health.

The operate stage protects users from every commit. Create development and production environments, deploy every push to development, and promote manually. Build the image once and store it in a registry so production receives the exact tested artifact. Instrument the backend with OpenTelemetry and choose a managed or self-hosted destination for metrics, logs, and traces.

Select product metrics rather than collecting numbers without a question. Show them on a dashboard filtered by environment and version. Add an actionable alert for a sustained user-impacting failure, including ownership and a dashboard link. An on-call script can start a headless agent with the alert details. The agent investigates, reproduces, tests, and commits the smallest fix, or explains a false positive.

The complete path is not a promise that a new product is production-perfect. Backups, VPCs, managed databases, scaling, rollback, security audits, and container management still require attention. The framework gives you a useful sequence and leaves the next decision visible instead of hiding it inside generated code.
