# The Night I Deleted Our Production Infrastructure

I was moving the AI Shipping Labs website from static GitHub Pages to AWS, with a longer-term plan to replace its Next.js setup with Django. The migration plan was reasonable: move the site to S3, move DNS to AWS, deploy Django on a subdomain, and switch the main domain after testing. The failure came from how I executed it.

I reused a Terraform setup that already managed the DataTalks.Club course platform because it saved roughly $5–10 per month. That decision mixed the new site with infrastructure holding two and a half years of homework, projects, and leaderboard data. I had also moved to a new computer without migrating the Terraform state file.

On Thursday night, I ran Terraform with auto-approval. Terraform believed no infrastructure existed and began creating resources. I stopped the apply after seeing the long list, then asked Claude to identify and remove the duplicates through the AWS CLI. While that cleanup was happening, I found the old computer, archived the Terraform folder with its state, and transferred it to the new machine.

I did not notice Claude unpacking the archive and replacing the current state with the old state for the course platform. When the agent proposed `terraform destroy`, it sounded like a clean way to remove the resources it had created. I let it proceed. The command deleted the real production VPC, RDS database, ECS cluster, load balancers, and bastion host. The course platform went down.

The snapshots were gone from the console too. I checked the RDS events and saw that a backup had been created, but the snapshot itself was not visible. Around midnight, I upgraded to AWS Business Support, which added about 10 percent to my cloud costs, and opened another ticket. Support replied in about 40 minutes and found a snapshot on their side. The case was escalated while I rebuilt other infrastructure and created an empty database for a possible restore.

Exactly 24 hours after the deletion, AWS restored the snapshot. I recreated the database with Terraform and checked the data. The `courses_answer` table alone contained 1,943,200 rows, and the course platform came back with its assignments visible.

The incident changed how I used the agent with infrastructure. Agents no longer execute Terraform commands. I generate a plan, review it myself, and run the commands manually. I also added backups outside Terraform state, S3 versioning, deletion protection in Terraform and AWS, and a daily restore test. A Lambda creates a database from the nightly backup, another checks it with a query, and the restored copy is stopped rather than deleted. Terraform state now lives in S3 instead of on one laptop.

The database recovery was fortunate. The safer conclusion was uncomfortable: I had delegated destructive operations and assumed backups were usable without testing the restore path. The infrastructure needed friction before deletion, and the agent needed to stop at the plan for a human review.
