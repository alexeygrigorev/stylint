# Temporary AWS access for workshops and agents

I needed to run an Exasol workshop for 50 or 60 participants. Exasol Personal runs in a participant’s AWS account, so everyone needed cloud resources, but I did not want to distribute my AWS keys. I also wanted to use GitHub Codespaces, where participants get the same tools without installing anything locally.

Sharing a key would have been a bad security choice and would leave me responsible for anything provisioned with it. I also did not want strangers using my main account. The solution came from the way EC2 instance profiles work. An instance assumes a role through STS, receives temporary credentials, and refreshes them when they expire.

I found `AWS_CONTAINER_CREDENTIALS_FULL_URI`, an environment variable that tells AWS SDKs where to request credentials. I hosted a Lambda that assumes a role and returns temporary credentials in the expected format. The SDK calls the endpoint when it needs access and refreshes the credentials without the participant seeing a long-lived key.

The Lambda lived in a separate sandbox account. A public repository template contained a dev container and the credential URL. Participants forked the repo, opened a Codespace, and ran workshop commands. I added a secret check so anyone finding the public endpoint could not request credentials. The workshop secret was shared offline.

The same mechanism became useful for coding agents. After an agent dropped my production database, I stopped giving agents a path to production. Agents run on a disposable remote sandbox server. They can write Terraform and push it to GitHub, while I apply real infrastructure changes from my laptop without skip-permissions mode.

Sometimes I still want an agent to experiment with AWS resources. `aws-sandbox-cli` writes temporary credentials into the project directory for about an hour. The account is separate from production, so an experiment can fail without reaching the real environment.

I also wanted to turn access on while away from my laptop. The remote sandbox already points to the Lambda, so I built `phone-aws-gate`. From my phone, I connect to the server with Termius, toggle the Lambda, authenticate with my fingerprint, and grant access for 15 minutes. `aws sts get-caller-identity` fails when the gate is closed, works while the timer is active, and fails again after I switch it off.

One credential endpoint now serves three situations: a workshop, agent experiments, and temporary phone-controlled access. It is still my responsibility to secure the endpoint, and the workshop secret was a deliberate disposable trade. The rule I keep is simpler: access must be scoped to a sandbox, temporary, revocable, and unable to reach production.

The endpoint does not remove the need to choose role permissions carefully. It only changes how credentials are issued and how long they remain available. The account boundary and the ability to turn access off are still part of the design.
