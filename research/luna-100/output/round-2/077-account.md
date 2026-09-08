# I Started with the Specification

I commit after meaningful decisions. That gives me a known state to return to when an agent takes a project in the wrong direction.

Coding agents write code faster than I can read it. A vague request no longer creates only a small misunderstanding. A capable agent can create several files, connect them, and add passing tests around an interpretation I never intended.

I tested this with a deliberately vague idea: a tool for weekly feedback on projects. When I gave that sentence to Claude Code, it produced `weekly-feedback`, a command-line tool for tracking project status. It recorded wins and issues. It also recorded blockers and next steps, and it had 62 passing tests.

The result worked, but I wanted a web tool for team retrospectives using Start, Stop, and Continue. The problem was my request.

Now I start in ChatGPT's dictation mode and discuss the idea before asking a coding assistant to build anything. I ask one question at a time and keep the answers short. For the retrospective, we clarified who contributes and whether names are visible. We also clarified what people see before the reveal, how cards are clustered, and how the team votes.

A facilitator could add audio, video, or a transcript later. Built-in recording stayed outside the first version.

When the decisions are clear, I ask the assistant to save them as a Markdown file and download it as `plan.md`. I put that file in a new Git repository, commit it, and ask an agent to propose several stacks without writing code. I chose Django because I know it well enough to review. Then I asked the agent to turn the plan into small backlog tasks.

I remove work that doesn't belong in the MVP and move the remaining tasks into GitHub Issues. From that point, the issues are the canonical backlog. The old `_docs/tasks.md` file no longer decides what should be implemented.

The repository also needs context for future sessions, so `AGENTS.md` contains commands and rules. `CLAUDE.md` references it with `@AGENTS.md`, which keeps the process available to different coding assistants.

I keep `process.md`, `testing-guidelines.md`, and `design-system.md` in `_docs` and link them from `AGENTS.md`. The agent reads that entry point at the start of every session and loads detailed documents only when a task needs them.

The workflow has separate roles. A product manager grooms an issue into a goal, checkable acceptance criteria, out-of-scope items, and constraints. A software engineer implements one groomed issue and writes tests. A QA agent checks the running result against the criteria and reports PASS or FAIL without changing code. The product manager then accepts the result.

I also use loops when grooming every issue, and the harness stops after every issue is groomed. "Make the code better" can't tell a harness when to stop because nobody can check it reliably. The specification comes before coding, context persists between sessions, and verification stays independent.
