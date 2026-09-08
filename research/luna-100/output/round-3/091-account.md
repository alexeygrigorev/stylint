# Making the Interview Canvas Safer to Operate

The interview canvas was already deployed and tested, but a deployed application still needs an operating process. I wanted changes to go to development first and promote the exact tested version to production.

I also wanted enough information to understand failures and an agent in the first response to an alert.

This was still a workshop proof of concept. Safe access, backups, escalation, and rollback remained for later work.

The first change was to create two environments. Every push to `main` deploys the latest version to development, where we check it. Production is a separate copy and doesn't receive every commit automatically.

A manual GitHub Actions workflow promotes the development version when we decide it's ready.

Infrastructure as code makes the two copies reusable. We still need differences such as machine size, but most resources can stay the same.

I also separated building from deploying. Before this change, EC2 built the Docker image during deployment. A production promotion would build again, and the resulting artifact might differ from the one tested in development. The new pipeline builds the image once, pushes it to Amazon ECR, and deploys the tagged image.

Tags use a timestamp and short commit hash, so production can pull exactly what ran in development.

Then I added observability by collecting metrics, logs, and traces. Metrics show numbers over time, logs record individual events, and traces show the spans a request passes through.

OpenTelemetry instruments the application and includes the service name, environment, and deployed version.

An OpenTelemetry Collector sends metrics to Prometheus, logs to Loki, and traces to Tempo. Grafana displays the data.

For this application I track rooms created, active participants, canvas elements, and failures while creating components.

A dashboard can filter by environment and deployed version. I keep the observability setup in a separate Docker Compose project from the application.

That's acceptable for a workshop, although real observability services and databases should be private with required authentication.

Dashboards don't help if nobody watches them, so I added an actionable alert for repeated canvas component-creation failures. Its threshold and duration represent user impact.

The alert includes the service, environment, and version, then names the owner and dashboard URL.

The on-call proof of concept polls the alert API every minute. When an alert fires, it starts a headless coding agent with the alert details.

The agent reads the code, reproduces the failure, and makes the smallest correction when a real bug exists. It runs backend tests and commits the fix.

A false positive should produce an explanation without changing code. I introduced a reproducible bug to test the whole response.

This is still a small experiment rather than a complete production incident system. In a larger setup, SNS could start a container job that runs the agent and stores its logs.
