# Moving the Interview Canvas from Local to AWS

The interview canvas worked locally, but I wanted to make it available on the internet. I took the React and FastAPI project from the previous workshop and prepared it for deployment.

I handled containerization and Postgres first. Then I added end-to-end tests and AWS infrastructure before setting up CI/CD. It was still a workshop-sized system, so I kept the infrastructure simple and left the main user flow unchanged.

Locally I ran the frontend and backend as separate services. In production the frontend becomes static HTML, CSS, and JavaScript after the build. It doesn't need its own container.

I created a two-stage Dockerfile where Node compiled the frontend and a Python image contained the backend together with the generated files. FastAPI served the frontend from that container.

SQLite was convenient during development because the database was one file. For production I added Postgres. SQLAlchemy made the change manageable because the application already had a database abstraction. I put Postgres and the application into Docker Compose and added a health check. With `docker compose up --build`, I could start a local setup that resembled the deployed one.

I kept testing the full user path. One browser creates an interview session and shares the join link. A second browser joins as the candidate and moves a canvas element. The interviewer must see the change.

Playwright automated this two-session test. Integration tests checked that the backend communicated with Postgres and that the frontend compiled. I ran the path after each major boundary because a passing unit test doesn't establish that two clients can use the application together.

Once those checks passed, I deployed with AWS CloudFormation. One EC2 instance ran Caddy, the application, and Postgres in one setup. Caddy supplied HTTPS and WSS support, so the arrangement was fine for a proof of concept. A managed database such as RDS would be a better production choice.

The first deployment used a temporary administrative AWS user while I watched what the coding agents did. I didn't want that to become the normal release process.

GitHub Actions now runs frontend and backend tests in parallel. It builds the Docker Compose stack, runs integration and end-to-end checks, and deploys only when they pass. OpenID Connect lets the runner assume a restricted AWS role instead of storing long-lived credentials.

I also added a health check after deployment. A push to `main` now goes through tests and deployment before I see the updated service.

The application still needs observability, safer infrastructure, backups, and rollback for a real production system. It became a deployable version of the same local workflow.
