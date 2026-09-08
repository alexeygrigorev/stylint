# Turning Project Notes into Agent Building Blocks

During the AI Dev Tools Zoomcamp I used Markdown files to describe process and agent roles. I wrote `_docs/process.md` to explain how work moved through the project.

PM, software-engineer, and QA documents described specialized responsibilities, and I wanted to make two concepts explicit. A skill is a repeatable procedure, and a subagent is an agent running in a separate context with a defined task.

I use a release skill for my Python libraries. Publishing a version means running tests, changing the source version, pushing a tag, and verifying that CI publishes it. I keep those instructions in `SKILL.md`, so I can say "release a new version" without repeating the procedure.

Skills have frontmatter with a name and description. They live in a discoverable skills directory, so the assistant can find the procedure when a request matches it. This makes the release steps reusable without hiding what they do.

Some skills are global because many projects need them, including release, library scaffolding, and repository creation. Transcript fetching and diagram creation are useful too.

I keep canonical copies in my agents repository and link them into assistant-specific directories.

Other skills are local to a project. An incident-response skill or FAQ curation skill belongs with the project that needs it. Claude uses a separate directory, so I link the project convention there too.

I create a skill after completing a task with an agent. I use the document to record corrections I actually made instead of an imagined process. For a local skill, I state explicitly that it must not be installed globally.

Updating a skill follows the same sequence. Use it, notice an intervention, and add the missing instruction. The next run then starts with the correction already documented.

Subagents solve a different problem. A new session has a fresh task context, so an implementation agent doesn't bring its assumptions into a review. In the agent team, a product manager grooms an issue, a software engineer implements it, and QA checks the result.

QA can look at the running application independently because its context didn't contain the implementation history. This separation makes the review less dependent on what the implementer remembers or believes.

The main session orchestrates the graph. It starts roles in order and sends failed QA work back to engineering. Independent issues can run in parallel, but each needs its own Git worktree.

The orchestrator tracks status, schedules tasks, prevents file conflicts, and merges approved work. These building blocks give repeated work a stable procedure and give review a clean context.
