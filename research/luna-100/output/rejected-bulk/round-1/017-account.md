# Keeping a Large Slack Community Useful



I want to describe what happened, because the sequence of small decisions is more useful than a polished summary. 

One Thing I Want to Share The result Week DataTalks.Club community has grown to more than 88,000 people

and lives across many Slack channels. Moderating a community at this scale is time-consuming.

https://alexeygrigorev.notion.site/Shameless-channels-template-f565ac6aa2064f7190382f2ffd82c876 for

posting there. I had to manually delete messages that violated the rules and send DMs explaining the

reasons to those people. It quickly became impractical since it required a lot of manual steps That is

what pushed me to build an automation tool that could delete messages violating the rules and send a

direct message explaining why. The number of messages deleted in the past week, grouped by reaction

type. Without AuTomator, deleting these messages and sending direct messages with an explanation would

all have been manual work. https://github.com/alexeygrigorev/au-tomator-lambda back in June 2022 and

kept adding features as new needs came up. Recently, the bot broke, and I fixed it using Claude Code,

which saved me at least two hours of debugging. In this post, I walk through how the bot is built and

how I chose AI to diagnose and fix it. How the AuTomator Works AuTomator bot is a backend running on AWS

Lambda. It is split into three Lambdas, each with a clear responsibility. 1. Router: Routes Slack events

to the automator or moderator The router checks incoming emoji reactions to see whether they were added

by an admin. If so, it forwards the event to the automator. The router exists for a purely technical

reason: Slack enforces a strict time limit on how quickly reaction events must be acknowledged. By

keeping the router lightweight and delegating all real work to the automator, the system avoids timeouts

and dropped events. 2. Automator: Acts based on the emoji reaction by the admin The automator is

responsible for actually doing something when a reaction emoji is added.

https://github.com/alexeygrigorev/au-tomator-lambda/blob/main/automator/config.yaml, and adding a new

reaction is fairly straightforward. https://github.com/alexeygrigorev/au-tomator-lambda/blob/main/automat

or/config.yamlL214 reaction, the automator replies in the thread with an AI-generated answer.

https://github.com/alexeygrigorev/au-tomator-lambda/blob/main/automator/config.yamlL87 reaction, the

automator deletes the message and sends the author a direct message explaining that the post violated

the community rules and was removed. 3. Moderator: watches message activity and helps the admin react

quickly The moderator is a new Lambda that I implemented with GitHub Copilot. It is not deployed yet and

still needs real-world testing. Its role is to monitor message activity over time and spot simple

patterns, like someone posting too many messages in a short period. When that happens, it sends an alert

to an admin and includes action buttons directly in Slack. These buttons allow the admin to delete

recent messages, deactivate the user, or ignore the alert without leaving Slack. I’ll need to review

Copilot’s work and check whether the moderator actually works as intended. Fixing the bot with Claude

Code In addition to my Moderator experiment, Claude helped me fix the AuTomator when it stopped working.

One of the messages didn’t get deleted after I added a reaction. Under normal circumstances, fixing this

would have meant spending several hours on: Opening CloudWatch Searching through logs Trying to

reconstruct what broke and why Manually fixing and redeploying I didn’t have that time since I was

preparing



That is the part I would keep from this example: connect each tool to the problem that made it necessary, and keep the limitation next to the claim. The details matter because they explain what can be reused and what was specific to this project.
