# How I would start with a coding agent

People often ask how to get started with coding agents. The question usually includes much more than installation: which model, permissions, commands, skills, subagents, plugins, MCP servers, local or remote setup, phone access, and every new trick shared online. Seeing all of that at once creates FOMO. My suggested path is much smaller.

First choose an assistant. Claude Code, Codex, OpenCode, GitHub Copilot, Antigravity, and Cline are all options. I used to recommend Copilot’s $10 plan, but its token-based billing changed the calculation. ChatGPT Plus at $20 includes Codex. Claude Code is included with Claude Pro at $20 and Max at $100 or $200, although the lower plan can run out quickly. I don’t think one tool is best for everyone. Budget is a reasonable first filter.

Then use the assistant on one real task. Write a script, solve course homework, build a small game, or fix a problem in a project you already use. You do not need a skill, plugin, subagent, or MCP server yet. Check whether the agent can solve the problem and whether its way of working suits you.

Permissions are the first practical choice. An allow-list lets you approve useful commands once and stop seeing repeated prompts. Skip-permissions or YOLO mode lets the agent run any terminal command, which is faster but means it can delete something. I use it for isolated projects and use an allow-list for production infrastructure, Terraform, permissions, and billing. I learned the cost of giving an agent too much access when it dropped a production database.

The next step is automation. While preparing LLM Zoomcamp videos, I asked Claude to find links, download videos and subtitles, cut them with ffmpeg, update descriptions and chapters, and place them into playlists. I still checked the cuts, bulk-uploaded files, and clicked Save because the YouTube API could not handle those steps. Once a service has an API or command-line interface, an agent can often connect it to a larger workflow.

When a process repeats, document it. After finishing the YouTube workflow, I asked the agent to write the steps in Markdown. Next time I could point it at the document instead of paying for it to rediscover the production URL, API key location, payload shape, and failure handling.

Repeated documents can become skills. Claude Code looks for `.claude/skills/<name>/SKILL.md`; Codex uses `.codex/skills/<name>/SKILL.md`. YAML frontmatter needs a name and description. Subagents come later, when context becomes noisy. A large transcript can be handled in a separate context while the main session receives only the summary. Start with one task, then add structure when repetition or context makes it necessary.
