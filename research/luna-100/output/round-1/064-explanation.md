# A gradual setup for coding agents

Coding agents become easier to use when the setup grows from an actual problem. Advanced configuration is not a prerequisite. A practical sequence is: choose one assistant, complete one task, automate a repeated workflow, document it, turn repeated documentation into a skill, and use subagents when the main context becomes too large.

For the first choice, compare only what matters immediately: price, access, and interface. Claude Code, Codex, OpenCode, Copilot, Antigravity, and Cline all provide possible starting points. ChatGPT Plus includes Codex at $20 per month. Claude Code is part of Claude Pro and Max plans, with different limits. Tools change, so learning from one finished task is more useful than trying to identify a permanent winner.

Pick a task small enough to verify from start to finish. A script, course exercise, small game, or bug fix gives you a concrete result. At this stage, avoid installing MCP servers, plugins, or custom skills. You need to learn whether the agent understands the request and whether you can review its work.

Permissions should match the cost of an error. An allow-list lets you approve safe commands and remember them. Skip-permissions mode removes the prompts but gives the agent broad terminal authority. It can be convenient for an isolated project, while production infrastructure, Terraform, cloud access, and billing deserve explicit approval. A sandbox reduces the blast radius, but it does not remove the need to understand what the agent can do.

After a successful task, look for repetition. An agent can automate work around a service when that service exposes an API or command-line tool. A video workflow, for example, can download files, retrieve subtitles, cut media with ffmpeg, update metadata, and assemble a playlist. Human checks may remain where an API is limited or the result needs visual inspection.

Write down the process once it works. A document should contain concrete details such as URLs, credentials locations, payload shapes, commands, and failure handling. It gives the next session a starting point and keeps the model from spending tokens rediscovering project-specific knowledge.

A recurring document can become a skill. Claude Code discovers files under `.claude/skills/<skill-name>/SKILL.md`; Codex uses `.codex/skills/<skill-name>/SKILL.md`. YAML frontmatter with a name and description is required. The rest can describe the workflow. Ask the agent to create the skill after you have corrected the process, because the corrections are part of what makes the instruction useful.

Subagents solve a different problem: context size. Keep small work in the main session. For a three-hour transcript, a large repository, or noisy logs, ask a subagent to analyze the material and save a result. The main agent receives the task status and summary rather than the full source. This keeps the main context available for the work that follows.
