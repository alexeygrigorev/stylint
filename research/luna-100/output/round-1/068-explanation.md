# A pattern for temporary AWS credentials

Workshops and coding agents often need cloud access, but handing out long-lived AWS keys creates a problem. A safer pattern is to expose a credential endpoint that returns temporary credentials, place it in a sandbox account, and make access revocable.

The starting point is the EC2 instance-profile flow. An instance receives an attached role, calls STS, obtains temporary credentials, and makes them available through instance metadata. AWS CLI and SDKs know where to look, and the credentials refresh when they expire. The same idea can work outside EC2 through `AWS_CONTAINER_CREDENTIALS_FULL_URI`.

The endpoint is a small Lambda. It assumes an AWS role and returns credentials in the format expected by the SDK. A Codespace can point to that URL, request credentials when needed, and use AWS tools without storing a permanent key in the repository or dev container.

For a workshop, put the Lambda in a dedicated sandbox account. A repository template can supply a dev container and the credential URL. Participants open Codespaces and run the same setup. Add a secret check because a public repository can expose the endpoint to anyone. A workshop-specific secret shared offline can be enough for a disposable session, although the endpoint remains something the operator must secure.

The same boundary applies to coding agents. Keep agents away from a main account and let them work in a separate AWS sandbox. For longer-term changes, agents can write Terraform and push it to GitHub while a human applies the change from a controlled machine. For experiments, a tool such as `aws-sandbox-cli` can write temporary credentials into the project for about an hour.

Temporary credentials are useful, but sometimes access should be off entirely. A phone-controlled gate can enable or disable the Lambda. When the gate is closed, an AWS identity request fails. When it is opened, the sandbox receives credentials for a short timer. Fingerprint authentication and a 15-minute window provide a concrete control when the operator is away from a laptop.

The design has four questions. Is the access scoped to a sandbox? Does it expire? Can it be revoked? Can it reach production? The last answer must be no. A temporary credential is not automatically safe if the role is too broad or the account is connected to real infrastructure.

This pattern was built for a workshop, then reused for agent experiments and phone-based operations. Its value is the common boundary: users and agents get enough access to do the exercise, but they never receive a permanent key or a route into production. The endpoint, role policy, secret, and revocation switch still need careful ownership.

Temporary access is therefore one layer of the system. The sandbox account, role scope, secret check, timer, and deployment process all contribute to the limit. Removing any one of them can change what the credential endpoint permits.
