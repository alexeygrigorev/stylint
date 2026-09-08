# Turning a Telegram bot into a writing assistant

I collect early ideas, corrections, and voice notes before an article becomes public. I also save files and screenshots. Telegram was a convenient place to capture them, but messages accumulated and manual sorting became slow.

Some belonged to an existing article, while others were partial thoughts or follow-ups. I wanted to keep the capture step in Telegram while making the material usable afterwards.

The assistant is for my own writing workflow, so it doesn't decide what should be published. It keeps the raw material available while organizing it into article drafts.

I discussed the workflow with ChatGPT, refined it, and asked it to save the conversation as `summary.md`. I used that file as the specification. I then asked Claude Code to implement it, producing a Telegram bot connected to a GitHub repository.

I tested the bot by using it as intended. I sent messages and voice notes, then recorded improvement ideas in the same chat. The normal cycle starts when I send text, a voice note, image, or file. Raw inputs are saved locally.

When I run `/process`, the assistant reads the batch and decides whether each item belongs to an existing article or starts a new one. Articles are updated incrementally instead of being regenerated from scratch.

After processing, the changes are committed to GitHub. The commit explains what changed and why, and the assistant sends the link back to Telegram. A bug or feature request can go into the same chat. `/check-tasks` reads those messages, looks for issues and suggestions, and updates the prompt or code before committing the next change.

Different inputs use different capabilities. Whisper through Groq transcribes voice messages, while the original audio is removed and the text retained. Groq Vision describes images and stores them under an article-specific assets directory.

Russian voice notes can be translated into English. Links are fetched and summarized so the resulting information becomes part of an article's context.

The repository is part of the workflow. Each run leaves a concrete diff, and Git records both code changes and the evolving specification. That makes it possible to see what the assistant changed rather than relying on an invisible conversation.

The commit is also a checkpoint. If a change isn't useful, I can look at when it appeared and adjust the prompt or code in a later run.

The raw files remain available while the article receives the organized version.

The bot doesn't remove the need to decide what belongs in an article. It makes the first steps cheaper. I can capture a thought while it's available, keep the raw material, and process it in a batch when there's enough context. That's the reason I kept Telegram as the input surface and moved the organization into GitHub.
