# Why I Built AuTomator for Our Slack Community

The DataTalks.Club community had grown to more than 88,000 people across many Slack channels. Moderating a community at that size took time, especially in the shameless-promotion channels. I introduced rules and message templates, but enforcing them meant deleting messages manually and sending each author a direct explanation.

That work quickly became too repetitive. I wanted a tool that could remove a message violating the rules and explain the reason to the person who posted it. I built the AuTomator bot in June 2022 and kept adding features as new needs appeared. The bot eventually became an AWS Lambda backend split into three smaller Lambdas.

The router handles the first technical constraint. Slack expects reaction events to be acknowledged within a strict time limit. The router checks whether an emoji reaction came from an administrator and forwards the event to the appropriate component. Keeping that first function lightweight means the heavier work does not cause a timeout or a dropped event.

The automator performs the action. A YAML file maps a predefined set of emoji reactions to behaviors. Adding a new reaction is therefore a configuration change. One reaction can delete a message, another can repost it in a thread, and `:ask-ai:` asks an AI to write a reply. The `:shameless-rules:` reaction deletes a rule-breaking message and sends its author a direct explanation.

I also started a moderator experiment with GitHub Copilot. The new Lambda watches message activity over time and looks for simple patterns, such as one person posting too many messages in a short period. It then alerts an administrator and places buttons in Slack for deleting recent messages, deactivating the user, or ignoring the alert. That component was not deployed yet and still needed real-world testing.

Then AuTomator broke. A message did not disappear after I added the expected reaction. Under normal circumstances, I would have opened CloudWatch, searched the logs, reconstructed the failure, fixed the code, and redeployed it. I was preparing for a family trip and did not have several hours, so I asked Claude Code to investigate.

I told Claude to fetch the previous two hours of logs and find the problem. It identified two causes: `GROQ_API_KEY` was missing for `ask-ai` reactions, and deleting messages containing curly braces produced an error. While I looked for the new key, Claude fixed the curly-braces issue. I supplied the key, and it updated the Lambda environment variables. The bot was fixed while I was packing, without opening a browser or clicking through the AWS console.

That experience clarified where this kind of tool fits for me. Claude Code was useful for urgent maintenance and operational work where execution mattered more than careful design. For slower, interactive coding, I still preferred Cursor, Google Antigravity, or GitHub Copilot.
