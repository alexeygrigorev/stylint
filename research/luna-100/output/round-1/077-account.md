# I Started with the Specification

I commit after meaningful decisions, so I can inspect what changed and return to a known state when an agent takes the project in the wrong direction.

Coding agents now write code faster than I can read it. That changes where I spend time. A vague request no longer produces a small misunderstanding that is easy to repair. A capable agent can create several files, connect them, and add passing tests around an interpretation I never intended.

I used a deliberately vague idea for a project: a tool for weekly feedback for projects. When I gave that sentence directly to Claude Code, it produced a command-line application called weekly-feedback. It recorded wins, issues, blockers, and next steps, and it had 62 passing tests. The result worked, but I wanted a web tool for team retrospectives using Start, Stop, and Continue. The problem was my request.

I now start in a chat assistant and dictate the idea. I ask one question at a time and keep the answers short. For the retrospective, we clarified who contributes, whether names are visible, what people see before a reveal, how cards are clustered, and how the team votes. We also decided that the facilitator could add audio, video, or a transcript later, while built-in recording was outside the first version. At the end I save the decisions as plan.md.

I put the plan in a new Git repository, commit it, and ask an agent to propose several stacks without writing code. I chose Django because I know it well enough to review. Then I asked the agent to turn the plan into small backlog tasks. I remove work that does not belong in the MVP and move the remaining tasks into GitHub Issues, which becomes the active backlog.

The repository also needs context for future sessions. AGENTS.md contains commands and rules, while CLAUDE.md points to it for Claude Code. I keep process.md and documents such as testing-guidelines.md or design-system.md in _docs, and link them from AGENTS.md. The agent reads the short entry point every time and loads detailed documents only when a task needs them.

The next change was procedural. A product manager agent grooms each issue into a goal, checkable acceptance criteria, out-of-scope items, and constraints. A software engineer implements one groomed issue and writes tests. A QA agent checks the running result against the acceptance criteria and reports PASS or FAIL without changing code. The PM then accepts the result.

I also use loops. If the goal is to groom every issue, the stop condition is that every issue is groomed. “Make the code better” is not checkable, so it cannot safely tell a harness when to stop. The point of the process is simple: specify the work before coding, provide context between sessions, and make verification an independent step.
