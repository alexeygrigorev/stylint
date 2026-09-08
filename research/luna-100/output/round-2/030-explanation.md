# Checking restores after the course database incident

During the AI Shipping Labs migration, I reused the Terraform setup for the DataTalks.Club course platform. I wanted to save perhaps $5 to $10 a month, but that mixed the new website with production infrastructure for another project.

I also left the Terraform state on my old computer. When I let Claude Code run the plan and apply, Terraform treated the existing resources as absent and started creating duplicates.

I stopped it and asked Claude to remove the duplicates through the AWS CLI. While that happened, I transferred an archive of the old Terraform directory. Claude unpacked it and replaced the current state with the production state without my noticing.

I let `terraform destroy` run because I thought it would remove what we'd just created. It deleted the real RDS database, VPC, and ECS cluster. The load balancers and bastion host were deleted as well.

AWS Support eventually found a snapshot that wasn't visible in my console. After an internal escalation, they restored it 24 hours after the deletion. I recreated the database and verified 1,943,200 rows in the `courses_answer` table before bringing the platform back.

Agents no longer execute Terraform commands for me. I review each plan manually and run the commands myself, with automatic execution disabled.

I created backups that Terraform doesn't manage, including copies in S3. I hadn't expected the automated snapshots to disappear with the database, so I wanted backups outside that infrastructure lifecycle.

I also wanted to test restoration continuously instead of assuming a backup was usable. AWS creates the regular backup at 2 AM. Around 3 AM, a Lambda creates a new database from that backup, which takes about 20 to 30 minutes.

Step Functions then runs another Lambda to check the restored database with a read query, such as `SELECT COUNT(*) FROM email`. When that succeeds, the instance is stopped instead of deleted. I keep paying for storage while avoiding the compute cost of leaving it running.

The previous day's restored instance is then deleted. That leaves one recent copy whose restoration has already been tested. If production goes down, I could start the replica and redirect traffic. I may not always use it that way.

I enabled deletion protection in Terraform and AWS. Those protections can still be removed explicitly, but they add steps before someone can destroy the resources.

For the S3 backups, I enabled versioning so earlier objects remain available after a deletion. Terraform state also moved to S3. I no longer depend on a local file that can be left behind when I switch computers.

For AI Shipping Labs, I'm also considering separate AWS accounts to isolate development from production. That's a possible next change, while the backup checks and command restrictions are already in place.
