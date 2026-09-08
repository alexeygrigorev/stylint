# Turning a Telegram bot into a writing assistant

Much of my work happens before a project or article becomes public. I collect early ideas, corrections, voice notes, files, and screenshots, but the finished result hides that background. Telegram was a convenient place to capture it, and at first I used a chat as a shared brain dump. The problem was what happened afterward: messages accumulated and manual sorting became slow.

Some notes belonged to an existing article. Others were only partial thoughts or follow-ups. To turn the stream into something usable, I had to reread messages, switch between audio, links, and files, and stitch related pieces together. That was enough friction to make me think about an assistant that could stay inside the same workflow.

I first discussed the idea with ChatGPT. I recorded the workflow, refined it, and eventually asked ChatGPT to save the conversation as `summary.md`. That document became the system specification. I did not want to implement the whole thing myself, so I asked Claude Code to follow the specification and build the first version. The result was a Telegram bot connected to a GitHub repository.

I tested it by using the bot as intended. I sent messages and voice notes, then recorded improvement ideas in the same chat. The assistant processed those inputs and updated the system. This mattered because the testing activity was part of the workflow rather than a separate demo prepared for the occasion.

The normal processing cycle starts in Telegram. I can send text, a voice note, an image, or a file. The raw inputs are saved locally on my laptop. When I run `/process`, the assistant reads the accumulated material as a batch. For each item, it decides whether it belongs to an existing article or should begin a new one. Articles are updated incrementally, so the assistant does not regenerate every article from scratch.

After processing, the changes are committed to GitHub. The commit has a description of what changed and why, and the assistant sends the commit link back to Telegram. If I find a bug or want a feature, I can record that request in the same chat. `/check-tasks` reads those messages, looks for issues and suggestions, and updates the prompt or code before committing the change.

There are a few focused capabilities behind this flow. Whisper through Groq transcribes voice messages, after which the original audio is removed and the extracted text is kept. Groq Vision describes images and stores them under an article-specific assets directory. Russian voice notes can be translated into English during processing. Links are fetched and summarized so they become part of an article’s context.

The assistant is orchestrated through Git. Each run leaves a concrete diff, and the repository records the evolving specification as well as the code. That gives the stream of rough ideas a place to go without requiring me to leave Telegram every time I want to capture something.
