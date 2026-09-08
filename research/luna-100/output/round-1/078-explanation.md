# Four Layers Around an AI Coding Agent

Each role can be described in ordinary Markdown. The useful part is the narrow definition of done and visible acceptance criteria.

That structure keeps responsibility visible while the backlog changes.

When a coding agent receives an unclear task, it fills in the missing decisions. The more capable the agent, the more convincing the wrong implementation can look. An AI-native development workflow therefore needs more than a good prompt. It needs a specification, durable context, a way to keep work moving, and separate agents with clear responsibilities.

Start with spec-driven development. Write down the users, the problem, and the expected behavior before code exists. A phrase such as “weekly feedback for projects” leaves too much open. The intended application might be a command-line status tracker or a web retrospective using Start, Stop, and Continue. The specification resolves that ambiguity and gives the agent something concrete to implement.

A chat assistant is useful for discovery because it can ask one question at a time. Clarify contributors, visibility, reveal behavior, clustering, voting, decisions, and what is outside the first version. Save the result in a plan file and commit it. Ask a coding agent to propose stack options and explain tradeoffs, then choose a stack you can review.

Turn the plan into a backlog of tasks small enough for one session. Each issue should be understandable without reading another task. Review the backlog, merge pieces that are too small, split work that is too large, and remove features outside the MVP. GitHub Issues can then become the canonical backlog.

The backlog alone is not enough context. Put commands and project rules in AGENTS.md. Link a process document, testing guidance, API description, or design system from there. Claude Code can read CLAUDE.md as a pointer to AGENTS.md. Keep the entry point short and load detailed documents only when relevant. This is context engineering: shaping what an agent knows before it begins.

Loop engineering addresses stopping. A harness can resume an agent until a checkable condition is true, such as every issue being groomed or all tests passing. A vague condition cannot work because the harness cannot decide whether it has been met.

Graph engineering addresses responsibility. A product manager turns a rough issue into acceptance criteria and constraints. A software engineer implements one issue and tests it. A QA engineer runs the code against every criterion and reports a verdict. A final acceptance step closes the loop. Separate roles reduce the chance that the same agent quietly accepts its own assumptions.

This structure does not guarantee a perfect application. It makes misunderstandings cheaper to catch, keeps project knowledge available between sessions, and gives the agent a defined place in a larger development process.
