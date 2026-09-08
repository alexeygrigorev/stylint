# A Safe Path from Local App to Deployment

This keeps routine releases auditable and limited.

Use restricted roles for normal automation and avoid leaving administrative access in the routine pipeline. These details affect how safely the application can be changed.

Temporary infrastructure should also have a cleanup path. After testing a workshop deployment, remove the cloud resources and check that the stack is gone, especially when the setup uses paid services.

Deployment becomes easier when you preserve the application’s boundaries and add one operational concern at a time. Start with a working local frontend and backend, then make the same flow repeatable in a container, with a production database, integration tests, and a controlled release.

In development, Vite serves changing frontend files and the backend runs separately. In production, build the frontend once and let the backend serve its static output. A two-stage Docker build uses Node only for compilation, then copies the files into a Python image. This leaves frontend dependencies out of the runtime image and reduces the deployment to one container.

SQLite is useful locally because it needs no server. Production usually needs Postgres. If the application already uses SQLAlchemy, change the database URL and add Postgres support without rewriting every data operation. Docker Compose can run the database and app together, with a health check that prevents the app from starting before the database is ready.

Test the boundaries, not only isolated functions. The frontend must compile, the backend must connect to Postgres, and the real user flow must work across two clients. For an interview canvas, Playwright can log in, create a session, join from a second client, change a diagram, and verify that the first client receives the update. A single command should run these end-to-end checks.

Once the Compose stack works, deploy it to a cloud environment. CloudFormation can create an EC2 instance, networking, Caddy, the application, and Postgres. This is a proof-of-concept arrangement. A managed database, private networks, backups, scaling, and rollback are concerns to add before treating it as a mature production architecture.

Continuous integration and deployment should separate build from release. Run frontend and backend tests, build the image, and publish it to a registry such as ECR. Deploy that exact image to development. When it has been checked, promote the same tag to production. Rebuilding during promotion could produce a different artifact.

GitHub Actions can use OIDC to assume a restricted cloud role instead of keeping long-lived administrator credentials. The workflow should run integration and end-to-end tests, deploy development, and verify a health endpoint. Production promotion can be a manual action. This sequence gives you evidence that the version being promoted is the version you tested.
