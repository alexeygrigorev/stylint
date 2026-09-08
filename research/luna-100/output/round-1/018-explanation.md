# The Three Parts of a Slack Automation Bot

AuTomator was built to reduce repetitive moderation in a large Slack community. DataTalks.Club had more than 88,000 members across many channels, and rule enforcement in the shameless-promotion channels involved deleting messages and explaining the decision to each author. The bot connected an administrator’s reaction to a specific action, while keeping Slack’s event timing constraint separate from the work itself.

The backend ran on AWS Lambda and was divided into three functions: a router, an automator, and a moderator. Each had a different responsibility.

The router handled incoming reaction events. It checked whether an administrator had added the emoji and then forwarded the event to the automator. This extra function existed because Slack required reaction events to be acknowledged quickly. The router stayed small, while the actual action happened elsewhere. That separation reduced the chance that slow work would lead to a timeout or a dropped event.

The automator translated an approved reaction into behavior. Its mapping lived in a YAML configuration file, which made the set of supported actions visible and made adding a reaction relatively straightforward. A reaction could delete a message, repost it in a thread, or request an AI-generated reply. A rule-related reaction also contacted the original author with a direct message explaining why the post had been removed. The emoji was the trigger; the configuration supplied the meaning.

The moderator was a separate experiment. Implemented with GitHub Copilot, it watched message activity and looked for simple patterns such as too many posts from one person in a short time. When it found one, it sent an alert to an administrator with buttons inside Slack. The administrator could delete recent messages, deactivate the user, or ignore the alert. At the time of the account, this Lambda had not been deployed and still needed real-world testing, so its design was not presented as a finished result.

The maintenance story showed another useful boundary. When one reaction failed to delete a message, Claude Code was asked to inspect the previous two hours of logs. It found a missing `GROQ_API_KEY` for `ask-ai` reactions and an error triggered by curly braces in message content. Claude fixed the deletion problem while the key was being located, then updated the Lambda environment variables after the key was supplied. The repair happened without opening the AWS console.

This arrangement separated three kinds of work: acknowledging an event quickly, executing a configured action, and watching for patterns that needed human attention. The bot did not try to make every moderation decision autonomously. An administrator still supplied the reaction or chose an action button. The automation handled the repetitive steps that followed.

The same distinction shaped the choice of coding tool. Claude Code was useful for urgent maintenance and operational fixes, where finding and executing a repair mattered most. For slower, interactive development, the author preferred Cursor, Google Antigravity, or GitHub Copilot. The architecture and the maintenance workflow both kept a human decision at the point where context mattered.
