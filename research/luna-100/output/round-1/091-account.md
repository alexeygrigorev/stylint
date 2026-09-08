# Making the Interview Canvas Safer to Operate

This was a workshop proof of concept, so it leaves several production concerns for later. Safe access, backups, escalation, and rollback need deliberate design when real users depend on the service.

The interview canvas was already deployed and tested, but a deployed application still needs an operating process. I wanted changes to go to development first, promote the exact tested version to production, collect enough information to understand failures, and involve an agent in the first response to an alert.

The first change was to create two environments. Every push to main deploys the latest version to development, where we check it. Production is a separate copy and does not receive every commit automatically. A manual GitHub Actions workflow promotes the development version when we decide it is ready. Infrastructure as code makes the two copies largely reusable, with differences such as machine size.

I also separated building from deploying. Previously EC2 built the Docker image during deployment. That means a promotion would build again, and the artifact might differ from the one tested in development. The new pipeline builds the image once, pushes it to Amazon ECR, and deploys the tagged image. Tags use a timestamp and short commit hash, so production can pull exactly what ran in development.

Then I added observability. Metrics show numbers over time, logs record individual events, and traces show the spans a request passes through. OpenTelemetry instruments the application and includes the service name, environment, and deployed version. An OpenTelemetry Collector sends metrics to Prometheus, logs to Loki, and traces to Tempo. Grafana displays the data.

For this application I track rooms created, active participants, canvas elements, and failures while creating components. A dashboard can filter by environment and deployed version. The setup is a separate Docker Compose project from the application. It is acceptable for a workshop, although real observability services and databases should be private and authenticated.

Dashboards do not help if nobody watches them. I added an actionable alert for repeated canvas component-creation failures, with a threshold and duration representing user impact. The alert includes the service, environment, version, owner, and dashboard URL.

The on-call proof of concept polls the alert API every minute. When an alert fires, it starts a headless coding agent with the alert details. The agent reads the code, reproduces the failure, makes the smallest correction if a real bug exists, runs backend tests, and commits the fix. A false positive should produce an explanation without changing code.

I introduced a reproducible bug to test the whole response. This is still a small experiment, not a complete production incident system. In a larger setup, SNS could start a container job that runs the agent and stores its logs. The important result is that deployment, observability, and response form one loop.
