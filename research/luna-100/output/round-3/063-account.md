# Starting with one coding-agent task

People ask me how to get started with coding agents. I initially thought installing one was enough of an answer, but they were also asking about permissions and models. Skills and subagents, along with the setups people post on X, made it seem as though there was a lot to learn first.

I'd work through the setup gradually. Choose an assistant and finish a real task, then try automation. Document repeated work and turn useful documents into skills. Add subagents when context becomes a problem.

I used to recommend GitHub Copilot at $10 a month, but its move to token-based billing changed that advice. ChatGPT Plus includes Codex for $20 a month. Claude Code comes with Claude Pro at $20, with Max plans at $100 or $200.

I can't say one tool is best for everyone, and the lower Claude limits can run out quickly. I'd start with what fits the budget and learn from using it on a complete task.

That might be a Python script or course homework. It could also be the Snake game from AI Dev Tools Zoomcamp, or a small fix in a project you already use. You can leave advanced features until you know whether the agent solves your problem and how you like working with it.

For permissions, an allow-list makes approved commands automatic over time. Skip-permissions mode lets the agent run whatever is available in the terminal, so it can also delete things.

I use that mode for many projects when I want work to continue overnight. For production infrastructure or Terraform, I use an allow-list. The same applies to cloud permissions and billing, where a mistake can be expensive.

Automation became more useful to me through repeated work. For LLM Zoomcamp videos, Claude downloads the videos and transcripts after finding the links, then cuts the videos with ffmpeg. It uses the subtitles to prepare chapters.

I still check the cuts, bulk-upload the videos, and click Save to publish them because of the API limitations. Claude handles video IDs and metadata, adds timecodes, and orders the playlist.

Once that worked, I asked the agent to document the process in Markdown. I could then point it at the document when more videos needed processing.

For less common tasks, the document needs context the agent won't know. My homework-publishing process includes the production URL and API-key location, plus API details and payload structure. It also describes what to do when something fails.

When I keep returning to a document, I turn it into a skill. Claude Code uses `.claude/skills/<skill-name>/SKILL.md`, while Codex uses `.codex/skills/<skill-name>/SKILL.md`. The file needs YAML frontmatter with a name and description, and I can ask the agent to create it.

Subagents help when a large transcript would fill the main session. A separate agent can summarize it and save the result, returning the summary without putting the full transcript into the drafting context.

I also keep project instructions in `CLAUDE.md` and `AGENTS.md`, including test commands and important files. I reset the session for each new task so the agent can begin with those instructions and a clean context.
