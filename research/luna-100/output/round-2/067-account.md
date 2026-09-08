# Keeping workshop AWS access temporary

When Exasol asked me to run a workshop, the technical setup was easy for one person. Exasol Personal runs in a participant's own AWS account. Supporting 50 or 60 people was harder because some would arrive without an account, permissions, or anything installed. I wanted everyone to work from GitHub Codespaces, and I didn't want to give a room full of people my AWS keys.

A shared key would have been difficult to control. Once it escaped, whoever had it could provision resources until I disabled it. I also didn't want unknown participants operating in my main account. I needed the convenience of a ready-made environment with a boundary around the damage.

I started from the way EC2 instance profiles already work. An instance receives a role, asks STS to assume it, and gets temporary credentials. The AWS tools find those credentials through the instance metadata service, and AWS refreshes them when they expire. I wanted the same structure outside EC2, including in a Codespace.

The useful piece was `AWS_CONTAINER_CREDENTIALS_FULL_URI`, which tells an AWS SDK where to fetch credentials. I put a Lambda behind an HTTP endpoint. The Lambda assumes a role and returns temporary credentials in the format the SDK expects. A Codespace can point at that endpoint, request credentials when necessary, and refresh them without a long-lived key being copied into the workshop project.

I put the Lambda in a separate AWS sandbox account. The public repository template included a dev container. Participants could fork it and open a Codespace with the tools and credential URL already configured. Because the repository was public, I added a secret check to the endpoint and shared the workshop secret offline. It was a disposable workshop arrangement, and security was still my responsibility.

## Reusing the endpoint for agents

The same mechanism became useful for coding agents. After an agent dropped my production database, I stopped treating access to the main account as an acceptable convenience. Agents now work on a remote sandbox server that I can recreate. They can write Terraform and push it to GitHub, while I apply infrastructure changes from my laptop under normal permissions. When an agent needs to experiment directly with AWS, `aws-sandbox-cli` writes credentials into its project for about an hour, inside a separate sandbox account.

I also wanted to grant access when I was away from my laptop. The remote sandbox already used the credential endpoint, so I built `phone-aws-gate` to toggle the Lambda. From my phone, I connect with Termius, authenticate with my fingerprint, and open a 15-minute window. With the gate closed, `aws sts get-caller-identity` fails. During the timer it works, and after I switch access off it fails again.

One endpoint now supports a workshop, agent experiments, and phone-controlled access. It doesn't make permissions correct. I still have to secure the endpoint, limit the role, keep the sandbox separate, and ensure there's no route to production. The useful rule is that access should be temporary, revocable, and bounded before anything gets to use it.
