# Build a Full-Stack App by Replacing One Part at a Time

When an AI coding assistant creates a full-stack application, asking for the entire system in one request makes failures difficult to locate. A staged build gives each component a boundary that can be tested before the next component replaces a temporary one. The interview canvas shows the sequence, which also applies to other small applications.

Begin with a precise specification. Describe who owns a session, how another person joins, which canvas elements can be placed, and what real-time behavior both participants should see. ChatGPT in dictation mode can help explore these decisions before implementation. The written specification gives the frontend and backend the same expectations.

Build an interactive React frontend first. Put every backend call behind one service layer and add a mock service. The application can run without a server, so you can check the screens and the idea while they're still cheap to change. Later, the mock implementation gives you a defined replacement point.

Next, turn that service layer into an OpenAPI description. List each endpoint with its method and path, then add its request body, response body, and authentication rule.

The API file gives the backend a concrete target. It also exposes mismatches in the frontend expectations before backend code introduces another interpretation.

Implement the backend against that description with FastAPI and an in-memory store. Routers, models, authentication, and tests are enough for the first connection. A Makefile can keep the run command simple, and the generated API documentation gives you another way to look at what the server exposes. Switch the frontend from the mock service to the real client and test the main flow in two browser windows.

Only after that connection works should you add persistence. Replace the in-memory store with SQLite and SQLAlchemy, then configure the database URL through an environment variable. Avoid SQLite-specific behavior where possible.

Restarting the server should leave sessions and diagrams intact, and SQLAlchemy keeps the database code open to a later change.

Each stage produces something concrete. First you get a specification, a frontend prototype, and an API description. Then you get a connected application and persistent data. When a screen is wrong, you can fix it before debugging a database. When the API doesn't match the frontend, the OpenAPI file shows the boundary to revisit.

Deployment, integration tests, migrations, and CI still come later. A local application that works from one browser session to another is enough evidence for the next step. It's a safer starting point than a large generated structure whose boundaries have never been exercised.
