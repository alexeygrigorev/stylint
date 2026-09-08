# Start With One Task, Then Add Agent Machinery

People often approach coding agents through a long list of configuration questions. They wonder which model to choose and how to set permissions. They also wonder about MCP servers, plugins, and local or remote execution. That list can make a first experiment feel like a systems project.

The sequence I use is smaller:

- choose an assistant
- use it on one real task
- try automation
- document repeated work
- turn useful documents into skills
- add subagents when context becomes a problem

Each step gives the next one a reason to exist.

Begin with a tool that fits the immediate budget and access needs.

Possible starting points include:

- Claude Code, Codex, and OpenCode
- GitHub Copilot, Antigravity, and Cline

ChatGPT Plus includes Codex at $20 per month. Claude Code is included in Claude Pro and Max plans with different limits. Tools change, so a completed task teaches more than an endless comparison of current plans.

Make the first task small enough to check from beginning to end. A Python or Bash script works. So does a course exercise, a small game, or a contained bug fix.

At this stage, you need to learn whether the assistant understands the request and whether you can review what it does. Custom skills, plugins, MCP servers, and subagents can wait.

Permissions should reflect the cost of an error. An allow-list lets you approve useful commands and remember those approvals. Skip-permissions mode removes the prompts and gives the agent broad terminal authority.

That can suit an isolated project. Production infrastructure, Terraform, cloud access, and billing need explicit care. A sandbox limits the possible damage. It doesn't replace understanding the commands.

Once a task works, look for an activity that repeats. An API or command-line tool gives an agent something concrete to operate. In one video workflow, an agent downloaded files and fetched subtitles. It cut media with ffmpeg, updated metadata, and assembled a playlist. Human checks remained where the API was limited or the result needed visual review.

Write the process down after the successful run. A useful document records the production URL and the location of credentials. It also records available operations, payload shapes, commands, and failure handling. That context prevents a later session from rediscovering project-specific facts and spending tokens on the same investigation.

When you use that document repeatedly, make it a skill. Claude Code discovers `.claude/skills/<skill-name>/SKILL.md`. Codex discovers `.codex/skills/<skill-name>/SKILL.md`. Both expect YAML frontmatter with a name and description. The rest of the file can explain the workflow and its limits.

Subagents address a different problem: an overloaded context. A long transcript, a large repository, or noisy logs can consume the space needed for the main task.

Ask a separate session to summarize the transcript, look at the repository, review the logs, or find exact files. Keep its focused result and let the main agent continue with a clean working context.
