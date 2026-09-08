# An agent team for projects with too many moving parts

For a small utility, I can describe an idea, iterate with Claude, and keep the whole project in one session. That stops working when requirements, implementation, testing, and deployment all move at different speeds. The agent can claim a task is complete without checking it, or the same session can write code and decide that the code is correct. I started experimenting with a team of agents to make those responsibilities explicit.

The main session acts as an orchestrator. It creates tasks, launches agents, assigns work, checks the process, and commits only after acceptance. The team has four roles. The Product Manager turns a raw request into user stories, acceptance criteria, and test scenarios, then reviews the finished work from the user’s perspective. The Software Engineer implements the code and tests. QA runs the tests and checks every acceptance criterion with evidence. The On-Call Engineer watches CI/CD after a push and fixes pipeline failures.

Every task follows the same path: backlog, PM grooming, implementation, QA, and a final PM review. If QA rejects the work, it returns to the engineer. If QA accepts it, the PM decides whether the result satisfies the user story. Only then does the orchestrator commit and close the task. I wanted this separation because passing tests alone does not prove that a feature works for the user.

I usually run two tasks in parallel, then pull the next two when that batch finishes. A recurring instruction tells the orchestrator to fetch another batch and add the instruction again, so the process can continue while the backlog remains. Tasks can be tracked with GitHub Issues or with files whose names move from `.todo.md` to `.groomed.md`, `.in-progress.md`, and `done/`.

The first serious test was the AI Shipping Labs website. Requirements from voice messages and ChatGPT sessions were collected into one file, turned into specifications and tasks, and tracked in GitHub Issues. After I let the agents work overnight, 41 of 46 tasks were complete. That result showed me the workflow could handle a non-trivial project, although it still needed supervision.

I also tried the method on DataTasks, a serverless AWS Lambda and DynamoDB tracker for the DataTalks.Club team. I dictated requirements, added the technical constraint, and gave feedback the next day. I paused the project because the existing tracker still worked and I did not have time to evaluate it properly.

For Mermaid diagrams, a file-based tracker was enough. The resulting pure Python renderer became `merm` after I asked for benchmarks. Rustkyll had a clearer optimization target: reduce differences between Jekyll and a Rust implementation while improving build speed. Codehive grew from repeated failures in the orchestrator, including stopping for input, skipping QA, poor visibility, and provider usage limits.

Across these projects, specifications, roles, and a written process reduced drift. They did not eliminate supervision, but they made it clearer where a task was waiting and what evidence was still missing.
