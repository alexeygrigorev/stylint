# Processing article notes through a Telegram bot

I use a Telegram bot to collect the background work that could become an article. I can send a thought as text or record it as a voice message. Images and files go into the same chat, so I don't have to organize everything when I capture it.

The inputs are saved locally on my laptop. I process them in a batch by running `/process`, which asks the assistant to read the accumulated material.

It checks whether a note adds something to an existing article or needs a separate one. If an article already exists, the assistant updates it incrementally. It doesn't write the whole article again whenever another note arrives.

After processing, the assistant commits the changes to GitHub. It describes what it changed and why, then sends the commit link back to Telegram. I can follow that link to the diff instead of trying to reconstruct the edits from the chat.

The inputs need some processing before they can be used in articles. For voice messages, I use Whisper through Groq to get a transcript. Once transcription finishes, the original audio file is removed and the extracted text is kept.

I often record notes in Russian even though I write articles in English. Claude translates the material during processing, so I can use the language that comes naturally when I'm recording an idea.

Groq Vision describes images, which the assistant moves into `assets/images/{article_name}/` so I can reference them in the article. When a message contains a link, the assistant fetches the page and incorporates a summary into the appropriate article.

I also use the chat to describe changes I want in the assistant. A voice note can contain a bug report or feature suggestion, and I can attach an image if it helps explain the issue.

Running `/check-tasks` asks the assistant to look for those requests. It can update its system prompt or code and commit the result to the repository. That lets me record improvement ideas while using the system, without leaving the workflow to describe them elsewhere.

I began by discussing this process with ChatGPT. I recorded voice messages and refined the description until it was clear enough to use as a specification. ChatGPT saved the conversation as `summary.md`, then I asked Claude Code to build what it described.

Claude produced the first working bot and connected it to GitHub. I tested it by sending messages and recording improvement ideas in the chat, which it then used to update the system.

I keep the specification in the repository alongside subsequent changes. I can give the agent instructions about keeping it current, including pulling the latest state before processing the next batch.
