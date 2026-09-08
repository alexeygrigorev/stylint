# How I Turned Telegram Notes into Draft Articles

Most of my project work happens before anything becomes public. There are early ideas, small experiments, and intermediate workflows that disappear once a project, talk, or article is finished. When I started this Substack, I wanted to share that background work as well, because it explains how I approach projects and can give readers ideas to try.

At first, Telegram was simply a brain dump. I created a chat for my team and me and collected ideas there for the newsletter. It worked for the first editions, but the raw material accumulated quickly. Voice notes, files, screenshots, partial thoughts, corrections, and follow-ups formed a long unstructured list. Before publishing, I had to switch between messages, links, and files, then reread, sort, and stitch everything together by hand. That was slow and mentally expensive.

I started the assistant by describing the workflow with ChatGPT. I recorded voice messages, discussed what I wanted, and refined the description until it was clear enough to write down. Then I asked ChatGPT to save the conversation as `summary.md`, which became the system specification. I asked Claude Code to follow that specification and build the first version. Claude created a Telegram bot connected to a GitHub repository containing the specification and later updates.

I tested it inside the same workflow I was trying to improve. I sent messages, recorded improvement ideas as voice notes, and let Claude process those inputs. The final assistant starts with a Telegram chat. I can send text, voice notes, images, or files, and the raw material is saved locally on my laptop.

When I run `/process`, the assistant reads the accumulated material as a batch. For each item, it decides whether the content belongs to an existing article or should begin a new one. Articles are updated incrementally instead of being generated from scratch. The changes are committed to GitHub with a description of what changed and why, and the bot sends the commit link back to Telegram.

The same chat is used for maintenance. I can record a bug report or feature idea as a voice note, add an image, and run `/check-tasks`. The assistant looks through the messages, updates its prompt or code, and commits the result.

Several focused capabilities support this workflow. Whisper through Groq transcribes voice messages, and the original audio is removed after transcription. Groq Vision describes incoming images and places them under `assets/images/{article_name}/`. Russian voice notes are translated into English during processing, while links are fetched and summarized into the relevant article. Git keeps every run visible as a concrete diff, and the assistant can follow instructions such as pulling the latest repository state first.

The system is not a machine that publishes without review. It is a way to keep background work in one place and turn a messy stream into drafts and visible changes. Telegram makes capture easy, Claude handles the repeated processing, and GitHub gives the workflow a history I can inspect.
