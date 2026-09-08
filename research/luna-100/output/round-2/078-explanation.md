# Four Layers Around an AI Coding Agent

When a coding agent receives an unclear task, it fills in the missing decisions. A capable agent can produce a convincing implementation that solves a different problem from the one you had in mind. A useful workflow therefore needs a specification, durable context, a way to keep work moving, and separate roles with clear responsibilities.

## Specify the work before coding

Spec-driven development starts with the users, the problem, and the expected behavior. The phrase "weekly feedback for projects" leaves too much open. The result could be a command-line status tracker or a web retrospective using Start, Stop, and Continue. A specification resolves that ambiguity before code exists.

A chat assistant can help with discovery when it asks one question at a time. Clarify contributors, visibility, and reveal behavior. Then clarify clustering, voting, decisions to record, and what stays outside the first version. Save the answers in a plan file, commit it, and ask a coding agent to propose stack options with their trade-offs. Choose a stack you can review.

Turn the plan into a backlog after choosing the stack. Each issue should be small enough to finish in one session and independent enough for someone who hasn't read the other issues. Review the list, merge tasks that are too small, split work that's too large, and remove features outside the MVP. GitHub Issues can then become the canonical backlog.

## Preserve context between sessions

The backlog doesn't tell a new agent how the project is organized. Put commands and project rules in `AGENTS.md`. Link process, testing, API, and design documents from it. Claude Code can read `CLAUDE.md` as a pointer to `AGENTS.md`.

Keep the entry point short. Load the design system only for a UI task and the testing guidance only when writing tests. These documents are living context, so update them when a correction should apply to future sessions. That's context engineering: shaping what an agent knows before it starts and where it can find more detail.

## Make progress checkable

Loop engineering deals with stopping. A harness can resume an agent until a condition such as "every issue is groomed" or "all tests pass" becomes true. The condition must be checkable. "Make the code better" can't tell the harness whether the work is finished, so it can stop too early or run forever.

A software engineer agent follows the same discipline during implementation. It reads one groomed issue, works within its files and constraints, writes tests, and leaves the issue open. Its own tests are useful, but they don't prove that the acceptance criteria are satisfied.

## Separate responsibility

Graph engineering assigns different jobs to different agents. A product manager grooms the issue and makes its acceptance criteria checkable. A software engineer implements the task and tests the new behavior. A QA engineer runs the code against every criterion and reports PASS or FAIL without changing the code.

An orchestrator can run this lifecycle. It chooses the next issue and sends it to the PM. Then it sends the groomed issue to the engineer, and the result goes to QA.

After FAIL, the engineer gets another turn, and the orchestrator closes the issue only after PASS. The roles make responsibility visible, and the QA agent doesn't quietly accept its own assumptions.

This process takes more time and tokens than a direct loop with one engineer, so many projects need only a simple prompt or loop. The extra layers are useful when the cost of an unclear specification or an unreviewed result is higher than the coordination needed to catch it.
