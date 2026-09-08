# What the Production Database Incident Changed

The production outage came from two conditions interacting. Terraform state was on an old computer, and the infrastructure for a new website had been added to the same setup that managed the DataTalks.Club course platform. When Terraform could not see the existing state, it treated production as absent. A later destroy command removed the real resources.

The first protection is separating environments. The AI Shipping Labs migration reused an existing Terraform configuration to save roughly $5–10 per month. That placed a new site and the course platform in one state and one risk boundary. When changes are mixed, a command aimed at one project can affect another. The account later considered a separate AWS account for development and production isolation.

The second protection is treating state as critical data. The missing state file was on an old laptop, so Terraform planned a large set of new resources. The archive was then unpacked and replaced the current state while cleanup was in progress. Moving Terraform state to S3 provided a shared, consistent view that was not tied to one machine. It also prevented a computer change from silently changing what Terraform believed existed.

The third protection is a human checkpoint before destructive actions. In the incident, the agent ran `terraform plan`, `apply`, and eventually `destroy` while the operator interpreted the work as duplicate-resource cleanup. The safer process became: generate the plan, review it manually, and run commands personally. The incident showed that a logically plausible command can still have the wrong target when its state is wrong.

Backups need a separate lifecycle. The database snapshots disappeared with the deleted database, although AWS support later found a snapshot that was not visible in the console. Additional S3 backups were created outside Terraform, with versioning so earlier objects could remain available after deletion. These copies were deliberately kept independent from the state that could destroy the primary resources.

A backup is also a claim that needs testing. A nightly restore workflow was added with Lambda and Step Functions. Around 3 AM, a Lambda creates a database from the regular backup. Another function runs a read query such as `SELECT COUNT(*) FROM email` to verify that the instance is usable. After the check, the restored instance is stopped so storage remains while compute costs do not continue. A recent restored replica stays available for a possible recovery.

Deletion protection adds another layer of friction. It was enabled in both Terraform and AWS, and S3 versioning provided a separate barrier for backup objects. These controls could still be removed explicitly, but they make accidental destruction harder.

The recovery took about 24 hours and restored 1,943,200 rows in one table. That outcome depended on AWS support finding a snapshot, not on the original process being safe. The resulting lesson was operational: agents can help inspect logs and prepare changes, but infrastructure state, destructive commands, and restore verification need independent checks before execution.
