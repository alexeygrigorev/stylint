# Skills, Subagents, and the Orchestrator

These are small abstractions, but they solve different sources of friction. Skills preserve a procedure, subagents isolate judgment, and the orchestrator keeps a multi-step workflow moving. Treating them as separate pieces makes the setup easier to change.

None of them removes the need to review results.

The orchestrator still has to understand which issues are independent, create isolated worktrees, and merge only approved changes. A clean graph makes those decisions explicit instead of relying on a single context to remember every task.

A coding assistant becomes easier to direct when repeated procedures and specialized roles are made explicit. A skill is a discoverable document that describes a sequence of actions. A subagent is a separate session with a narrow responsibility. The main session can orchestrate both.

Use a skill when the same steps happen repeatedly. A release procedure might run tests, bump a version, create a tag, and verify CI. Put those instructions in a Markdown file with a name and description in frontmatter. Store it in the convention used by the assistant, such as `.agents/skills/name/SKILL.md`. The assistant can discover the skill from the request, while an explicit instruction remains possible.

Global skills belong on the machine when multiple projects need them: package release, library initialization, repository creation, transcript retrieval, or diagram generation. Project skills belong in the repository when they depend on local data or rules. A canonical repository with symlinks can keep several coding assistants aligned. Claude may use a separate directory, so account for that when sharing project skills.

Create the skill after doing the work. First observe the decisions and corrections an agent needs. Then ask it to record the process, including the constraints. This produces a more useful procedure than writing a generic document before anyone has tried it. Update the skill after the next intervention.

Use a subagent when context separation matters. A PM can turn intake into checkable acceptance criteria, an SWE can implement one groomed task, and QA can run the result without inheriting the implementer’s confidence. Define each role in a discoverable Markdown file and give it a narrow definition of done.

The main session acts as an orchestrator. It launches PM, SWE, and QA in sequence, returns failures to the implementer, and accepts only a passing result. Independent work can run concurrently, but isolation is required. Create one Git worktree per task, complete the full review cycle there, and merge approved work back one task at a time.

This arrangement is not about adding agents for its own sake. Skills reduce repeated explanation. Subagents make a fresh review possible. The orchestrator manages order, state, conflicts, and promotion. Together they turn a collection of prompts into a process that can scale without hiding responsibility.
