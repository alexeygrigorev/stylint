# A Telegram Workflow for Turning Background Work into Articles

The Telegram writing assistant was built around a simple problem: useful work often happens before a project becomes public, then disappears from the final result. The system captures that background work and turns it into structured articles stored in GitHub. Its design has four stages: capture, batch processing, versioning, and configuration updates.

Capture begins in a Telegram chat. The author can send text, voice notes, images, or files. The raw material is saved locally on a laptop, so the input format does not decide what the eventual article will look like. This matters when a thought is easier to record as speech or when a useful reference arrives as an image or link.

Processing is explicit rather than continuous. When `/process` runs, the assistant reads the accumulated materials as one batch. For each item, it decides whether the content belongs to an existing article or should start a new one. Existing articles are updated incrementally instead of being regenerated from scratch. That preserves the connection between a new note and the draft it changes.

The next stage is versioning. After processing, the assistant commits every update to a GitHub repository. The commit describes what changed and why, then sends a link back to the Telegram chat. Git turns an invisible editing process into a series of inspectable diffs. The repository stores both the system specification and the later changes produced from the chat.

The same input channel handles maintenance. Improvement ideas, bug reports, and feature requests can be recorded as voice notes or accompanied by images. Running `/check-tasks` makes the assistant scan those messages, update the system prompt or code, and commit the result. The workflow therefore has a way to revise its own instructions without requiring a separate issue tracker.

Several focused capabilities keep the stages connected. Whisper through Groq transcribes voice messages, and the original audio is removed so downstream steps work with text. Groq Vision describes images and moves them into `assets/images/{article_name}/`, where an article can reference them. Russian voice notes are translated into English during processing because English is the article language. Links are fetched and summarized into the relevant article rather than left as detached URLs.

The assistant was specified before it was implemented. ChatGPT helped refine the workflow and saved the conversation as `summary.md`. Claude Code then followed that specification to build the Telegram bot and GitHub connection. Testing the system through the same chat used for capture made it possible to record improvements without leaving the workflow.

This arrangement does not make publishing automatic. It makes the incoming stream manageable and leaves a history of what the assistant did. Telegram is optimized for quick capture, batch processing supplies a moment for organization, and GitHub provides reviewable state. Those boundaries are what turn a chat full of fragments into material that can become an article.
