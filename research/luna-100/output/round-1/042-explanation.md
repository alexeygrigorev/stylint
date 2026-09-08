# Giving coding agents a process to follow

An agent can write code quickly, but complex software work contains another problem: how do you know that the task is understood, implemented, tested, and accepted? A useful answer is to split the work into roles and make the transitions explicit. The setup I use has a main orchestrator and four specialized agents.

The Product Manager starts with a raw request. It produces a specification containing user stories, acceptance criteria, and test scenarios. This gives the engineer something concrete to implement and gives QA something concrete to verify. After implementation, the same role returns for a final review from the user’s perspective.

The Software Engineer writes the code and tests. QA is a separate agent. It runs the tests, checks every acceptance criterion, and reports pass or fail with evidence. Keeping these roles separate makes it harder for the agent that produced a change to approve its own assumptions. The On-Call Engineer watches the CI/CD system after code is pushed and handles pipeline failures.

The pipeline is deliberately repetitive:

1. Add the request to a backlog.
2. Have the PM groom it.
3. Let the SWE implement the specification.
4. Ask QA to test the result and check the criteria.
5. Return rejected work to the SWE.
6. Send accepted work to the PM for final acceptance.
7. Commit and close the task only after that review.

The final PM step matters because a feature can pass technical tests and still miss the user story. The process itself should live in the repository. Role definitions describe responsibilities, a process document records the sequence, project instructions provide local constraints, and an execution skill starts the pipeline. A written process is easier to inspect than a long instruction repeated in a chat.

Parallelism is useful once the sequence is stable. I run two tasks at a time and ask the orchestrator to pull the next batch when both finish. A recurring task-list instruction keeps that cycle going until the backlog is empty. Tracking can use GitHub Issues when visibility and reports are useful, or a lighter file tracker where filename states record progress.

The approach worked on several different projects. For a community website, requirements were consolidated before agents created GitHub tasks. For a task tracker, a short dictated specification included AWS Lambda and DynamoDB as constraints. For a Mermaid renderer, filenames in a repository tracked the task states. For Rustkyll, comparing generated output with Jekyll provided a concrete optimization target.

The process also exposes its own weaknesses. An orchestrator may stop and wait, skip grooming, or report completion while tasks remain. Subagents may be hard to observe, and a provider limit can interrupt the run. These problems led to Codehive, an orchestrator intended to enforce the pipeline in the application itself, support several agent backends, continue non-blocking work, expose subagent activity, and import GitHub issues.

Roles and checklists do not make supervision disappear. They make supervision specific: look at the acceptance evidence, the test report, the final user-facing review, and the task state before committing.
