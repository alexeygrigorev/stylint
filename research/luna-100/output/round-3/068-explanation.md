# Temporary credentials need a boundary

A workshop or coding agent may need AWS access for a short task. Putting a long-lived key in a laptop, repository, or Codespace makes the credential the boundary, which is a poor one. A more useful approach issues temporary credentials through an endpoint. It keeps the work in a separate sandbox account and makes the endpoint easy to turn off.

EC2 instance profiles provide the model. An EC2 instance starts with an attached role and calls STS. It receives temporary credentials and exposes them through the instance metadata service. The AWS CLI, boto3, and other SDKs know where to find those credentials, which AWS refreshes after they expire. The workload receives short-lived credentials instead of someone copying a permanent secret into it.

Outside EC2, `AWS_CONTAINER_CREDENTIALS_FULL_URI` provides the hook. It tells an AWS SDK which HTTP URL to ask for credentials. A Lambda can assume an AWS role and return temporary credentials in the format the SDK expects. A Codespace can use that URL, request credentials when needed, and avoid storing an AWS key in its repository or dev container.

The account boundary matters as much as the endpoint. For a workshop, put the Lambda and its role in a dedicated sandbox account.

A repository template can provide a dev container and the configured URL. Participants can open Codespaces with a common environment. A public repository can expose the URL to anyone. The endpoint needs a check such as a workshop secret shared offline. That's a deliberate disposable setup, and the operator remains responsible for securing it.

## Apply the same boundary to agents

The same arrangement limits coding agents. Keep their experiments in a separate AWS account and away from production. For a real infrastructure change, an agent can write Terraform and push it to GitHub while a human applies it from a controlled laptop. For exploratory work, `aws-sandbox-cli` can write temporary credentials into the project for about an hour. The agent gets room to discover which resources and permissions it needs without receiving a path to the main environment.

Sometimes the safest credential is unavailable. A phone-controlled gate can enable or disable the Lambda behind the sandbox endpoint. With the gate closed, `aws sts get-caller-identity` fails. Opening it after fingerprint authentication grants a 15-minute window, and switching it off removes access again. That control is useful when the operator is away from the laptop and still wants to approve a bounded experiment.

Review the design through four checks. Access must be scoped to a sandbox, expire, and be revocable. It must also have no route to production.

Temporary credentials aren't automatically safe. The role can be too broad, the endpoint can be open, or the sandbox can connect to real infrastructure. The endpoint and role policy enforce part of the limit. The secret check, timer, and deployment process enforce the rest.

This approach applies to workshops and agents alike. The shared mechanism is temporary, revocable access with no long-lived key sitting on the machine. The surrounding boundaries decide whether that mechanism is actually safe enough for the task.
