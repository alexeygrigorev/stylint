# The Day I Dropped Production



I want to describe what happened, because the sequence of small decisions is more useful than a polished summary. 

https://aishippinglabs.com/ and wanted to migrate its current version from static GitHub Pages to AWS.

And later, replace the original Next.js setup with a Django version. My gradual plan was: 1. Move the

current static site from GitHub Pages to AWS S3 2. Move DNS to AWS so the domain is fully managed there

3. Deploy the new Django version on a subdomain 4. When everything works, switch the main domain to

Django The result way, everything would already be inside AWS, and the final switch would be seamless.

The migration strategy itself was reasonable, but the problems came from how I executed it.

https://courses.datatalks.club/ that stored data for 2.5 years of all submissions: homework, projects,

leaderboard entries, for every course run through the platform. To make matters worse, all automated

snapshots were deleted too. I had to upgrade to AWS Business Support, which costs me an extra 10% for

quicker assistance. Thankfully, they helped me restore the database, and the full recovery took about 24

hours. In this post, I’ll share how I let this happen and the steps I’ve taken to prevent it from

happening again. Course management platform with no data: no courses, no questions, no answers, no login

providers Incident Timeline Thu, Feb 26 ~10:00 PM: Started deploying website changes using Terraform,

but I forgot to use the state file, as it was on my old computer. RDS. I later discovered that all

snapshots were also deleted, prompting me to create an AWS support ticket. Fri, Feb 27 ~12:00 AM:

Upgraded to AWS Business support for faster response times. ~12:30 AM: AWS support confirmed that a

snapshot exists on their side. ~1:00-2:00 AM: Had a phone call with AWS support, which was escalated to

their internal team for restoration. During the day: Implemented preventive measures, including setting

up a backup Lambda function, enabling deletion protection, creating S3 backups, and moving the Terraform

state to S3. ~10:00 PM: The database was fully restored, containing 1,943,200 rows in the coursesanswer

table alone. The platform was brought back online. How the Disaster Happened Reusing an Existing

Terraform Setup https://courses.datatalks.club/. Instead of creating a separate setup for AI Shipping

Labs, I added it to the existing one to save a small amount of money. VPC with all resources in a

private network, a bastion for hosting machines. The savings are not that big, maybe $5-10 per month,

but I thought, why do I need another VPC, and told it to do everything there. That increased complexity

and risk since changes to this site were now mixed with those to other infrastructure. First Warning

Sign Instead of going through the plan manually, I let Claude Code run terraform plan and then terraform

apply. My first clue that something was off was when I saw a long list of resources being created. That

made no sense: the infrastructure already existed. We weren’t building a new environment. I stopped

Claude and asked, “Why are we creating so many resources?” The agent’s answer was simple and terrifying

at the same time: Terraform believed nothing existed. But why? I had recently moved to a new computer

and hadn’t migrated Terraform. When I



That is the part I would keep from this example: connect each tool to the problem that made it necessary, and keep the limitation next to the claim. The details matter because they explain what can be reused and what was specific to this project.
