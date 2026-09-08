# Deleting the course platform during a website migration

I wanted to move the AI Shipping Labs website from GitHub Pages to AWS. My plan was to put the static site on S3 and move DNS, then deploy a Django replacement on a subdomain. I'd switch the main domain after testing it.

I already had Terraform managing the DataTalks.Club course platform. Claude suggested keeping the new site separate, but I wanted to save perhaps $5 to $10 a month by reusing the existing setup. That put the website changes alongside infrastructure holding two and a half years of homework and project submissions.

On Thursday night, I let Claude run Terraform without reviewing the plan myself. It started creating a long list of resources even though the infrastructure already existed. I had switched computers without moving the state file, so Terraform thought it was starting from nothing.

I stopped the apply, but it had already created some resources. I asked Claude to identify the duplicates through the AWS CLI and remove only those resources.

While it worked, I went to the old computer and archived the Terraform folder with its state. I transferred the archive and pointed Claude to it so it could compare the old resources with the newly created ones.

I didn't notice that it unpacked the archive and replaced the current state with the old production state. When Claude proposed `terraform destroy`, I still thought it was cleaning up duplicates and didn't stop it.

The command deleted the production VPC, RDS database, and ECS cluster. The load balancers and bastion host disappeared too, and the course platform went down.

I looked for daily snapshots in the RDS console and couldn't find them. The events showed a backup had been created, but I couldn't open it. I didn't yet know whether it was deleted or simply inaccessible.

Around midnight, I upgraded to AWS Business Support, adding about 10% to my cloud costs. Support replied to my new ticket in roughly 40 minutes and found a snapshot on their side that wasn't visible to me. They escalated the recovery internally.

While waiting, I rebuilt other infrastructure and created an empty database in preparation for a possible restore. Exactly 24 hours after deletion, AWS restored the snapshot. I recreated the database through Terraform and checked that `courses_answer` contained 1,943,200 rows. The platform came back with its homework assignments visible.

I changed how I use agents with Terraform. I now review the plan and run commands myself, with automatic execution disabled.

I also created backups outside Terraform, including separate S3 copies, and enabled deletion protection in Terraform and AWS. S3 versioning protects earlier backup versions, and Terraform state now lives in S3 rather than on one laptop.

A daily workflow uses Lambda and Step Functions to restore a database from the nightly backup and check it with a read query. After verification, it stops the restored instance rather than deleting it. Yesterday's restored copy is then removed, leaving a recent replica available.

I had relied on the agent to run destructive commands and assumed my backups could be restored. While AWS investigated, I had to consider losing the older course data permanently. Their recovery gave me the chance to bring the platform back and keep those safeguards in place.
