# Fixing our Slack bot while packing for a trip

DataTalks.Club has more than 88,000 people across its Slack channels. As the community grew, I introduced rules and templates for the shameless-promotion channels. When someone ignored them, I had to delete the message and send a DM explaining why.

That became too much repetitive work, so in June 2022 I built AuTomator. I kept adding features as new needs appeared. It handles actions such as removing a message and contacting its author after I react with a configured emoji.

The backend uses AWS Lambda, with separate functions for routing events and performing actions. I've also implemented a moderator function, though it isn't deployed yet.

The router checks whether an admin added an emoji reaction and forwards the event to the automator. Slack requires a quick acknowledgment of reaction events, so I keep the router lightweight and let the automator do the actual work.

A YAML file defines the supported reactions and what each one does. The automator looks up the reaction and runs its action. It can delete a message or repost it in a thread, and the `:ask-ai:` reaction requests an AI-generated reply.

With `:shameless-rules:`, it removes the message and sends the author a DM about the rule violation. I still choose the reaction, but I don't have to perform those follow-up steps manually.

I used GitHub Copilot to implement the new moderator. It's intended to watch message activity and alert an admin when, for example, someone posts too many messages in a short period.

The alert has Slack buttons for deleting recent messages, deactivating the user, or ignoring the alert. I still need to review Copilot's code and test whether it works in practice.

Recently, a message stayed in the channel after I added the deletion reaction. Normally I'd open CloudWatch and go through the logs, then fix and redeploy the code. I was getting ready for a family trip and didn't have several hours for that.

I asked Claude Code to fetch the previous two hours of logs and find the problem. It found that `GROQ_API_KEY` was missing for `ask-ai` reactions. It also found a deletion error when messages contained curly braces.

While I looked for the new key, Claude repaired the curly-braces problem. I then supplied the key, and it updated the Lambda environment variables. The bot was working again while I packed, without my opening the AWS console or a browser.

It saved me at least two hours of debugging. I find Claude Code useful for urgent maintenance when execution matters more than careful design. For slower and more interactive coding I prefer Cursor, Google Antigravity, or GitHub Copilot.
