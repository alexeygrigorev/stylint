# Operating an AI-Built Application

The goal is a controlled loop, not a collection of dashboards.

Each part should support a decision.

The application in the example is a collaborative system-design canvas, but the operational questions are general. A successful build is only a snapshot. Once people depend on it, releases need a path, failures need evidence, and someone needs to decide what happens after an alert.

Getting a deployment command to finish tells you very little about whether users can use the application. An operating setup needs controlled releases, telemetry, alerts, and a response process. The pieces can be added to the interview canvas or any similar service.

Keep development and production separate. Pushes can deploy the latest code to development, where it is checked. Production should receive a deliberate promotion. This protects users from a change that passes a build but introduces a regression. Infrastructure as code makes a second environment easier to create and keep close to the first.

Build the container once and promote that artifact. If the deploy stage builds directly on an EC2 instance, promoting to production may rebuild the code and produce something different. Split CI into a build stage that uploads a tagged image to a registry and a deploy stage that pulls it. Production should use the same tag that ran in development.

Telemetry provides the evidence needed to understand behavior. Metrics are numbers over time, logs are records of events, and traces show the spans a request passes through. OpenTelemetry is a common way to instrument an application. Include service, environment, and deployed version so a dashboard can distinguish releases.

An OpenTelemetry Collector can route data to storage. A self-hosted example uses Prometheus for metrics, Loki for logs, Tempo for traces, and Grafana for dashboards. A managed service is another option. Keep the observability stack separate from the application stack and protect it with private networking and authentication when it contains sensitive information.

Choose application metrics that reflect user impact. For a collaborative canvas, rooms created, active participants, elements created, and component-creation failures are useful. Add filters for environment and version. A dashboard helps investigation, but nobody can watch every panel, so create an alert with a threshold and duration that represent a real failure. Include owner and dashboard details in the alert.

An on-call worker can poll the alert API and start a headless agent when an alert fires. Give the agent a bounded evidence packet and instructions to reproduce the issue, make the smallest correction, run tests, and commit only a real fix. A false positive should produce an explanation. Production systems need escalation and access controls, but this provides a concrete starting loop from deploy to observation to response.
