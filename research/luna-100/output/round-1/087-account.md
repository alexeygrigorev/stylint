# Taking the Interview Canvas to AWS

The result was easy to verify.

This was still a workshop-sized system, so the infrastructure choices were intentionally simple. The goal was to learn the path from a local service to a publicly reachable one while keeping the test scenario unchanged.

The interview canvas worked locally, but that was not enough. I wanted to make the application available on the internet, so I took the React and FastAPI project from the previous workshop and prepared it for deployment. The work included containerization, Postgres, end-to-end tests, AWS infrastructure, and CI/CD.

Locally I ran the frontend and backend as two services. In production the frontend becomes static HTML, CSS, and JavaScript after the build, so it does not need its own container. I created a two-stage Dockerfile: Node compiled the frontend, then a Python image contained the backend and the generated files. FastAPI served the frontend from the same container.

SQLite was convenient during development because the database was one file. For production I added Postgres. SQLAlchemy made the change manageable because the application already had a database abstraction. I also put Postgres and the application into Docker Compose. A health check lets the application wait until the database accepts connections, and `docker compose up --build` starts the local production-like setup.

The most important test is the full user path. One browser creates an interview session and shares the join link. A second browser joins as the candidate and moves a canvas element. The interviewer must see the change. I called this the two-session test and ran it after each major boundary. Playwright automated the same scenario, while integration tests checked that the backend could communicate with Postgres and the frontend compiled.

Once those checks passed, I deployed to AWS with CloudFormation. One EC2 instance ran Caddy, the application, and Postgres. Caddy provided HTTPS and WSS support. This was appropriate for a proof of concept, although a managed database such as RDS would be a better production choice.

The first deployment used an administrative AWS user while I watched the agent. I did not want that to be the normal release process. GitHub Actions now runs frontend and backend tests in parallel, builds the Docker Compose stack, runs integration and end-to-end checks, and deploys only when they pass. OIDC lets the runner assume a restricted AWS role instead of storing long-lived credentials.

I also added a health check after deployment. A push to main now gives me a complete path from code to a tested running service. There is still more to do for a real production system, including observability, safer infrastructure, backups, and rollback, but the local application became a deployable one without changing its main workflow.
