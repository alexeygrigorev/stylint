# A 28-Step Path to Production

The shortest useful way to use coding agents on a product is to keep the boundaries explicit. Start with a specification, build a testable frontend, and define the API.

Implement the backend, then add persistence and operations so each stage leaves something you can run. The cloud provider matters less than the handoffs between these parts.

In the Build stage, discuss the raw idea with a chat assistant and save a specification. Generate a frontend with one service layer and a mock backend. Create a manual scenario that describes the user journey. Derive an OpenAPI schema from the service layer, compare backend stack options, and save the choice before implementation.

Build the backend against the schema with an in-memory store, seeded data, authentication, and tests. Use a Makefile for repeatable commands. Connect the real frontend and run the manual scenario. Replace the store with SQLite and an ORM after the connection works. This order shows whether a failure belongs to the interface, API, or persistence.

The Deploy stage begins by putting the frontend's built static files and backend in one container. Add Postgres for production and Docker Compose for local management.

Integration tests should exercise backend and database interaction. End-to-end tests should start in the browser and verify the complete path to the database.

Choose a cloud and an infrastructure-as-code method. Then add CI/CD that runs tests, builds, deploys, and checks health.

The Operate stage protects users from every commit. Create development and production environments, deploy every push to development, and promote manually. Build the image once and store it in a registry so production receives the exact tested artifact. Instrument the backend with OpenTelemetry and choose a managed or self-hosted destination for metrics, logs, and traces.

Select product metrics rather than collecting numbers without a question. Show them on a dashboard filtered by environment and version.

Add an actionable alert for a sustained user-impacting failure, including ownership and a dashboard link. An on-call script can start a headless agent with the alert details.

The agent investigates and reproduces the problem. It tests the change and commits the smallest fix, or explains a false positive.

The complete path has 28 concrete steps, but it doesn't promise a production-perfect product.

Several production concerns remain:

- backups, VPCs, and managed databases
- scaling, rollback, and security audits
- container management

The framework gives you a sequence and leaves the next decision visible instead of hiding it inside generated code.
