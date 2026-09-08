# Keep the Deployment Path Small and Verifiable

Deployment is easier when a working local application keeps its boundaries while you add one operational concern at a time. Start with the frontend and backend.

Then make the same flow repeatable in a container, connect a production database, test the boundaries, and release a controlled artifact. Normal automation should use restricted roles and have a cleanup path alongside the application.

In development, Vite serves changing frontend files and the backend runs separately. In production, build the frontend once and let the backend serve its static output. A two-stage Docker build uses Node only for compilation, then copies the files into a Python image. The runtime image has no need for a separate frontend container or the frontend build dependencies.

SQLite is convenient locally because it needs no server, while production often needs Postgres. If the application already uses SQLAlchemy, change the database URL and add Postgres support without rewriting every data operation. Docker Compose can run the database and app together. A health check prevents the app from starting before the database accepts connections.

Test the boundaries as well as isolated functions. The frontend must compile, and the backend must connect to Postgres. The real user flow must also work across two clients.

For the interview canvas, Playwright can log in and create a session. It can join from a second client, change a diagram, and verify that the first client receives the update. A single command can run these end-to-end checks against the Compose stack.

Once the local stack works, deploy it to a cloud environment. CloudFormation can create an EC2 instance and networking. It can also create Caddy, the application, and Postgres.

Treat that arrangement as a proof of concept. Before calling the architecture mature, consider a managed database, private networks, and backups. Scaling and rollback also need attention. After testing a workshop deployment, remove the cloud resources and check that the stack is gone, especially when it uses paid services.

Continuous integration and deployment should separate build from release. Run frontend and backend tests, build the image, and publish it to a registry such as ECR. Deploy that exact image to development. After checking it, promote the same tag to production. Rebuilding during promotion could produce a different artifact from the one that passed tests.

GitHub Actions can use OpenID Connect to assume a restricted cloud role instead of keeping long-lived administrator credentials. The workflow can run integration and end-to-end tests, deploy development, and verify a health endpoint. Production promotion can be manual. This sequence leaves evidence that the version promoted is the version tested.
