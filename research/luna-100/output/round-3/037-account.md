# Splitting the work in my Telegram assistant

My Telegram writing assistant started with voice notes, text messages and links. As I added more tasks, one Claude Code context had to handle the incoming material alongside long external articles.

Processing several URLs together filled that context quickly. Responses slowed down, compaction happened more often, and the agent sometimes lost details. I split the work between subagents so the main agent could concentrate on my messages and coordinate the rest.

## Research and newsletter links

I created an `article-summarizer` subagent for external reading. It takes a URL, fetches the page through Jina Reader, and adds a structured summary to the relevant research article. The main agent receives that result without having to process the whole external document.

For newsletter links, I added `resource-describer` to write something shorter. It also retrieves the page with Jina Reader, but produces a description of two to four sentences for `interesting-resources.md`. That file holds the resources I might include in the newsletter.

Having separate agents lets me change how I describe a resource without changing how I process a research article. The main agent delegates the external reading and continues handling voice messages.

## Checking what was left out

I had already told the main agent to preserve the details in my voice notes. It still sometimes summarized them during processing. A shorter draft could lose the context that explained why I made a decision.

I added `verify-content` to compare the generated content with the original voice messages. It runs after the main agent finishes and fills in information that was omitted. This gives the workflow a separate step for checking something the original instruction hadn't reliably prevented.

I also changed how I send longer recordings. Telegram stops recording a voice note when the app goes into the background, so I wanted to send regular audio files instead.

The first implementation didn't work through the whole pipeline. After debugging ingestion and transcription, I could send files such as MP4 or M4A and have them processed as speech input. I also added YouTube transcript retrieval, so a video link can supply material for a draft without manual transcript extraction.

## Turning corrections into skills

Some changes came from repeatedly correcting the same behavior. With the `/process` command, I resolve a mistake in the session and then ask the agent to examine what happened. It uses that discussion to update the command file.

I use a similar process for workshop slides. I dictate the ideas into Telegram and then open an interactive Claude Code session with the material. The `create-slides` skill prepares the slides, which I review and refine. I also added `slides-to-pdf` for producing the PDF.

I developed this workflow while preparing a Zalando workshop, which took longer than subsequent attempts. Later workshops gave me examples I could reference when asking for changes. I could ask for a previous layout without describing it from scratch each time.
