# Operating an AI-Built Application

A successful build is only a snapshot. Once people depend on the application, releases need a controlled path, failures need evidence, and someone needs to decide what happens after an alert. These concerns apply to the collaborative interview canvas and to similar services.

Keep development and production separate. Pushes can deploy the latest code to development, where it's checked. Production should receive a deliberate promotion. Infrastructure as code makes a second environment easier to create and keep close to the first.

This gives the team a place to find regressions before users receive every change. Build the container once and promote that artifact.

If the deploy stage builds directly on an EC2 instance, a production promotion may rebuild the code. The result could differ from the version checked in development.

Split CI into a build stage that uploads a tagged image to a registry and a deploy stage that pulls it. Production should use the same tag that ran in development. This keeps the release artifact tied to the checks that preceded promotion.

Telemetry provides evidence about application behavior. Metrics are numbers over time, logs record events such as an error or failed database query, and traces show the spans a request passes through.

OpenTelemetry is a common way to instrument the application. The service name, environment, and deployed version let a dashboard distinguish releases.

An OpenTelemetry Collector can route that data to storage. One self-hosted arrangement uses Prometheus for metrics, Loki for logs, Tempo for traces, and Grafana for dashboards. A managed service is another option.

Keep the observability stack separate from the application stack. Protect it with private networking and authentication when it contains sensitive information.

Choose metrics that reflect user impact. For a collaborative canvas, track rooms created and active participants. Also track elements created and component-creation failures.

Add filters for environment and version. A dashboard helps during investigation, but nobody can watch every panel. Create an alert with a threshold and duration that represent a real failure, and include the owner and dashboard details.

An on-call worker can poll the alert API and start a headless agent when an alert fires. Give the agent a bounded evidence packet and instructions to reproduce the issue, make the smallest correction, run tests, and commit only a real fix. A false positive should produce an explanation.

Production systems need escalation and access controls. This sequence still gives you a concrete loop from deployment to observation to response.
