# Turning Project Notes into Agent Building Blocks

The distinction became useful after I had repeated the same work often enough to notice what should be stable. I did not want a role description to disappear in a long session, or a release procedure to depend on remembering every command.

The document becomes part of the working interface.

During the AI Dev Tools Zoomcamp I used Markdown files to describe process and agent roles. `_docs/process.md` explained how work moved through the project, while PM, software-engineer, and QA documents described specialized responsibilities. That worked, but I wanted to make the two concepts explicit: a skill is a repeatable procedure, and a subagent is an agent running in a separate context with a defined task.

I use a release skill for my Python libraries. Publishing a version means running tests, changing the source version, pushing a tag, and verifying that CI publishes it. Rather than repeat those instructions, I keep them in `SKILL.md` and can say “release a new version.” Skills have frontmatter with a name and description and live in a discoverable skills directory. The important difference from an ordinary Markdown file is that the assistant can find the procedure when a request matches it.

Some skills are global. Release, library scaffolding, repository creation, transcript fetching, and diagram creation are useful across projects, so I keep canonical copies in my agents repository and link them into the assistant-specific directories. Other skills are local. An incident-response skill or FAQ curation skill belongs with the project that needs it. Claude uses a separate directory, so I link the project convention there too.

I create a skill after completing a task with an agent. That way the document records the corrections I actually made instead of an imagined process. For a local skill, I state explicitly that it must not be installed globally. Updating a skill follows the same pattern: use it, notice an intervention, then add the missing instruction.

Subagents solve a different problem. A new session has a fresh task context, so an implementation agent does not carry its assumptions into a review. In the agent team, a PM grooms an issue, an SWE implements it, and QA checks the result. QA can inspect the running application independently because its context did not contain the implementation history.

The main session orchestrates the graph. It starts roles in order and sends failed QA work back to engineering. Independent issues can run in parallel, but each needs its own Git worktree. The orchestrator tracks status, schedules tasks, prevents file conflicts, and merges approved work. The building blocks are simple, but their value comes from giving repeated work a stable procedure and giving review a clean context.
