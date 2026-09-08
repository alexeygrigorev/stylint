# Handling moderation actions with Slack reactions

In DataTalks.Club, more than 88,000 people use our Slack channels. I introduced posting rules and templates for the shameless-promotion channels, but enforcing them meant deleting messages and explaining each removal in a DM. I built AuTomator to handle those repetitive steps.

An admin's emoji reaction tells the bot what to do. The backend runs on AWS Lambda, with a router that receives Slack events and an automator that performs the configured action. I've also implemented a moderator function to watch message activity, though it still needs testing before deployment.

The router first checks whether an admin added the reaction. If so, it passes the event to the automator. I keep this function small because Slack imposes a strict time limit for acknowledging reaction events. Doing the heavier work elsewhere avoids delaying that acknowledgment.

The automator reads a YAML file that maps reactions to actions. Adding a supported reaction means configuring what should happen when an admin uses it.

For example, I can ask it to delete a message or repost it in a thread. With `:ask-ai:`, it generates a reply in the thread. With `:shameless-rules:`, it removes the post and sends its author an explanation of the rule violation.

I implemented the moderator with GitHub Copilot to look for activity such as a person sending too many messages within a short period. It should send an alert to an admin with action buttons inside Slack.

The admin can use those buttons to delete recent messages or deactivate the user. There's also an option to ignore the alert. I haven't deployed this part yet, so I still need to review the implementation and check its behavior with real activity.

I recently used Claude Code to investigate a failure in the existing bot. A message didn't disappear after I added a reaction, and I was preparing for a family trip. I asked Claude to read the last two hours of logs instead of opening CloudWatch and investigating manually.

It found a missing `GROQ_API_KEY` affecting the AI replies, plus an error when deleting messages containing curly braces. Claude fixed the deletion error while I located the replacement key. After I gave it the key, it updated the Lambda environment variables.

I could keep packing while it worked, and I didn't need to open a browser or use the AWS console. That repair saved me at least two hours of debugging.

For urgent maintenance and operational work, Claude Code fits how I want to get a fix done. When I have time for slower interactive coding, I prefer Cursor, Google Antigravity, or GitHub Copilot.
