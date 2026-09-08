# A Full-Stack Build Without Guessing the Whole System

The example is an interview canvas, but the sequence applies to other small applications. The particular framework can change; the useful boundary is between a temporary implementation and the contract that the next component must satisfy.

It is a workflow for reducing uncertainty one interface at a time.

An AI coding assistant can create a full-stack application quickly, but asking for the entire system at once makes it hard to tell which part is wrong. A better sequence keeps the interfaces stable while replacing temporary components one at a time.

Begin with a specification. For a shared system-design canvas, define the session owner, joining flow, canvas elements, and real-time behavior. The specification should be precise enough that a frontend and backend can work from the same expectations. ChatGPT in dictation mode is useful for exploring those decisions before implementation.

Build the frontend first for a small project. Generate an interactive React application, but put every backend call behind one service layer. Add a mock service so the application can run without a server. This lets you evaluate the idea and screens early, and it creates one place to switch from mock calls to real HTTP calls.

Next, turn the service layer into an API contract. Ask the coding assistant to create an OpenAPI file containing each endpoint, method, path, request, response, and authentication rule. This step is optional but useful because the backend receives a precise target. It also exposes what the frontend actually expects before backend code introduces another interpretation.

Implement the backend against that contract with an in-memory store. FastAPI, routers, models, authentication, and tests are enough for this stage. The goal is to prove the connection, not to solve persistence. Run the backend through a simple Makefile and inspect its generated API documentation. Then switch the frontend to the real client and exercise the important path in two browser windows.

Only after the connection works should you add a database. Replace the store with SQLite and SQLAlchemy, use an environment variable for the database URL, and avoid SQLite-specific behavior so another database can be introduced later. Restart the server and verify that state survives.

This approach gives you a testable result after each step: specification, frontend prototype, backend contract, connected application, and persistence. It also limits the scope of each agent session. If a screen is wrong, fix it before debugging a database. If the API does not match the frontend, the contract shows where.

The resulting application may still need deployment, integration tests, migrations, and CI. Those are later stages. A local application that behaves end to end is a better starting point than a large generated structure whose boundaries have never been tested.
