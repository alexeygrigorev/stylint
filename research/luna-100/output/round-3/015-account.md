# Organizing my Telegram notes into articles

When I started this Substack, I wanted to share more of the work behind my finished projects. The early thinking and small experiments usually disappear from the final result. I thought that showing them could help readers understand how I work and find ideas for their own projects.

I created a Telegram chat for my team and me, then used it to collect newsletter ideas. That helped with the first editions, but the chat soon became difficult to organize.

Voice notes accumulated alongside screenshots, files, and text messages. Some messages continued an earlier idea, while others corrected something or introduced a different topic. Before publishing, we had to go back through the material and work out what belonged together.

Switching between messages, links, and files took time and effort. I wanted an assistant that could organize the incoming notes into articles while I kept using Telegram to capture them.

I described the workflow to ChatGPT through voice messages and refined it in conversation. Once I could explain what I wanted clearly, I asked it to save our discussion as `summary.md`. That became the specification for the system.

I didn't want to implement it myself, so I gave the specification to Claude Code. It built a Telegram bot connected to a GitHub repository, where it stored the specification and subsequent updates.

I tested the assistant by using the same chat to send notes and record ideas for improvements. Claude processed those messages and changed the system, so I could keep describing problems as I encountered them.

The bot accepts text and voice messages, along with images and files. It saves the incoming material locally on my laptop. When I run `/process`, it reads the accumulated batch and decides which notes should update existing articles and which need new ones.

Existing articles receive incremental edits. The assistant commits its changes to GitHub with an explanation and sends the commit link back to Telegram, where I can follow what changed.

I use `/check-tasks` for bug reports and feature suggestions recorded in the chat. It reads those messages and updates the prompt or code, then commits the changes.

Whisper through Groq transcribes my voice messages. After transcription, the assistant removes the audio files and keeps the text for later processing. I often record in Russian, so Claude also translates the material into English for the articles.

Groq Vision describes incoming images and moves them into `assets/images/{article_name}/`. Links are fetched during processing, and the relevant information becomes part of the appropriate article.

Each run leaves a diff in Git. I can also give the agent instructions about that process, such as running `git pull` before processing new material to work from the latest repository state.
