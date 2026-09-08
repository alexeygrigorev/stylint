# Five Projects Built With an Agent Team

I wanted to see whether an agent team could handle software too involved for a single coding session. I used Claude Code with a main session acting as an orchestrator.

The orchestrator launches agents, assigns work, checks that the process is followed, and commits only after acceptance. The roles are Product Manager, Software Engineer, Tester, and On-Call Engineer. Each has a separate responsibility.

The PM turns a raw request into user stories, acceptance criteria, and test scenarios. The SWE writes implementation and tests.

QA runs those tests and checks each criterion with evidence. The On-Call role watches CI/CD after a push.

After QA accepts a task, the PM reviews it from the user's perspective. If QA rejects it, it returns to the SWE.

This division keeps implementation and judgment separate.

I first tested the process on the AI Shipping Labs community platform. Valeriia and I had gathered requirements in voice messages and ChatGPT sessions, but they were spread across several places.

I put them into one file, asked Claude Code to create specifications and tasks, and used GitHub Issues for tracking. After letting the agents work overnight, I found that 41 of 46 tasks were done.

That didn't prove the process was finished, but it showed the loop could handle a non-trivial project.

Next I tried DataTasks for the DataTalks.Club team. Our work was split between Trello, spreadsheets, and a Telegram TODO bot.

I dictated the requirements and added one constraint. The application had to be serverless with AWS Lambda and DynamoDB. DataTasks was working after about 20 minutes of requirements, 20 minutes starting Claude Code, and 20 minutes of feedback the next day.

I paused it because I lacked time to evaluate it, and the existing system was still good enough.

Merm came from a course need. I wanted Mermaid diagrams, but the Python options I found didn't render them directly, and the Node solution started a full browser.

Claude Code built a pure Python renderer. I used a file-based tracker because I didn't know whether the project would be useful.

Benchmarks mattered as much as correctness, and the results were good enough to publish Merm and use it for diagrams.

Rustkyll exposed a mistake when I pointed Claude at the DataTalks.Club website and asked for a Rust implementation without first writing requirements.

Claude tailored the first result to that site instead of making a general Jekyll engine. I had to redirect the work toward other Jekyll sites.

After three weeks, it was still in progress. Our website was already much faster, with small visible differences.

Finally, Codehive grew out of repeated failures. Agents stopped for input, while others claimed work was done too early, skipped QA, or hit provider limits. Codehive is intended to enforce the pipeline and support several agent backends. It should continue when one task waits, expose subagent progress, and pull GitHub Issues into the pool.

The experiment taught me that roles, specifications, and supervision remain necessary even when implementation is delegated. 
