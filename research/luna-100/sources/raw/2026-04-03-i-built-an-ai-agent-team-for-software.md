Over the past few weeks, I’ve been trying out a new way of working with agent teams for software development using Claude Code. Instead of just seeing it as a single tool, I’ve started thinking of the main session as an orchestrator that directs a small team of agents.


I’ve tested this setup on a few projects now, and while it’s still a work in progress, I can already see what works, what doesn’t, and what controls are needed to let the agents build real projects with minimal oversight.

In this post, I’ll share what my setup looks like: how I describe the agents, how they interact, how it all fits into a single-team workflow, and how I used this approach to build five different projects.

## Background

For small tools, I usually dump my idea into my [Telegram Writing Assistant](https://alexeyondata.substack.com/p/telegram-assistant) or [talk to ChatGPT](https://alexeyondata.substack.com/p/how-i-built-sqlitesearch-a-lightweight) to refine it (or both). I iterate with Claude until the concept works. This approach is sufficient for smaller utilities or projects that I can easily manage.

But it falls short for more complex projects with too many moving parts and tasks at different stages. For example, it doesn’t provide a way to verify the agent’s claims that a task is complete or test that it was implemented correctly according to the plan.


That’s why I decided to try building a team of agents, each with their own role, with the main session serving as the orchestrator: it launches agents, assigns tasks among them, ensures compliance with the process, and only commits the work after the final acceptance step is completed.

## The Team and the Process


The agent roles: PM, Software Engineer, Tester, and On-Call Engineer

In my current setup, the work is split across four roles.

* The [Product Manager](https://github.com/AI-Shipping-Labs/website/blob/main/.claude/agents/product-manager.md) (PM) takes a raw task and turns it into something implementable: a spec with user stories, acceptance criteria, and test scenarios. Later, after implementation and QA, the PM reviews the result from the user’s perspective and decides whether the task is actually complete.
* The [Software Engineer](https://github.com/AI-Shipping-Labs/website/blob/main/.claude/agents/software-engineer.md) (SWE) implements the code and writes tests.
* The [Tester](https://github.com/AI-Shipping-Labs/website/blob/main/.claude/agents/tester.md) (QA) runs those tests, checks each acceptance criterion, and reports pass or fail with evidence.
* The [On-Call Engineer](https://github.com/AI-Shipping-Labs/website/blob/main/.claude/agents/oncall-engineer.md) monitors CI/CD after code is pushed and fixes pipeline failures.

Each role has a narrow set of responsibilities, which makes it harder to skip steps and easier to see where something went wrong. For example, this task distribution allows me to avoid a situation in which the same agent writes the code and decides whether it’s correct.


### Pipeline

Every task moves through the same sequence. I ask the orchestrator to create the task and add it to the backlog. The PM picks it up and grooms it. The SWE implements it. QA verifies it. If QA rejects the task, it goes back to the SWE for fixes. If QA accepts it, the PM does a final acceptance review. Only after the PM accepts does the orchestrator commit the code and close the task.


The pipeline: every task goes through PM, SWE, QA, and back to PM before commit

The final PM review is important for making sure the result aligns with the user story, which is a key requirement beyond just passing tests. A feature might seem done from an engineering standpoint, but can still flop in real-life situations.

The process is written down in the repository so the agents can follow it consistently:

* [.claude/agents/](https://github.com/AI-Shipping-Labs/website/tree/main/.claude/agents) contains the role definitions
* [PROCESS.md](https://github.com/AI-Shipping-Labs/website/blob/main/_docs/PROCESS.md) describes the development workflow
* [CLAUDE.md](https://github.com/AI-Shipping-Labs/website/blob/main/CLAUDE.md) contains project-level instructions
* The [execute](https://github.com/AI-Shipping-Labs/website/blob/main/.claude/skills/execute/SKILL.md) skill starts the pipeline

### Parallel Batches

I usually run two tasks in parallel. When that batch is finished, the orchestrator pulls the next two from the backlog.


Two tasks processed in parallel, then the next batch is pulled from the backlog

To keep the loop going without manual intervention, I keep a recurring instruction in the task list that tells the orchestrator to fetch the next batch and then add the same instruction again. That way, the process continues until the backlog is empty, rather than stopping after each batch is completed.


Task list with agents running in parallel

## Task Tracking

For tracking, I use either GitHub Issues or a file-based tracker/ folder. GitHub Issues work well when I want visible coordination and agent reports attached to each task. The file-based approach is lighter: task status is encoded in the filename, moving from .todo.md to .groomed.md to .in-progress.md, and eventually into done/.


GitHub issues as the task tracker

In the following sections, I describe the projects I implemented using the agent team approach. For task tracking, I used GitHub for some projects and a file-based version control system for others.

The tool itself matters less than the workflow around it. In both cases, the same PM -> SWE -> QA -> PM loop stays in place.


## 1) AI Shipping Labs Website

My first serious attempt at this approach was the [AI Shipping Labs community platform](https://github.com/AI-Shipping-Labs/website). I will describe it in more detail in a separate article, but here I want to focus on how the process worked.


When Valeriia and I decided to create a new community, we started by collecting requirements for the platform that would host it. We recorded a lot of voice messages and had multiple sessions with ChatGPT, and eventually it became clear that no existing platform matched what we wanted, so building our own made more sense.

At that point, the requirements already existed, but they were spread across multiple sources. I pulled everything into one file, asked Claude Code to turn it into specifications and then into tasks, and used [GitHub Issues](https://github.com/AI-Shipping-Labs/website/issues) as the tracker.

Once the setup was ready, I let the agents run through the night. The next morning, 41 out of 46 tasks were already done.


Morning after: 41 out of 46 tasks completed overnight without intervention

That was the first time I saw that this workflow could handle a non-trivial project. Since then, I have iterated on the methodology many times, but the structure stayed the same: I talk to the orchestrator, it creates an issue, and then it launches the implementation pipeline of grooming, implementation, testing, and acceptance.

If you want to see how these issues look in practice, check this one about [adding comments](https://github.com/AI-Shipping-Labs/website/issues/147). The PM described the requirements, acceptance criteria, and test scenarios, the SWE reported that the feature was implemented, QA verified it, and the issue includes screenshots of the final result.


## 2) DataTasks for DataTalks.Club

After AI Shipping Labs, I wanted to see whether the same methodology would work on a different kind of project.

The first candidate was a task tracker for the DataTalks.Club team. At the moment, our work is split across a Trello board, different spreadsheets, and a Telegram channel with a TODO bot.

This setup works, but it creates a lot of cognitive load. I’ve been planning to replace it with a custom solution, but I haven’t had the time to build one. With coding agents, that became realistic.


Our current task tracking in a Telegram channel with a TODO bot

I dictated the requirements through the Telegram bot, added one technical constraint, that the application had to be serverless and run on AWS Lambda with DynamoDB, and let the team choose the rest.

The result is [DataTasks](https://github.com/alexeygrigorev/datatasks). I spent about 20 minutes dictating the requirements, another 20 minutes starting the Claude Code session, and another 20 minutes giving some feedback the next day.


DataTasks dashboard showing Active Bundles on the left and Today’s Tasks on the right

I paused the project for now because I do not have time to evaluate it properly, and our current task-tracking setup still works well enough. But as an experiment, it proved useful, showing that the methodology can be applied beyond a single project.


## 3) Merm (Mermaid Diagrams)

The next project came from a more specific technical need.

While working on the [AI Engineering Buildcamp course](https://maven.com/alexey-grigorev/from-rag-to-agents), I needed to include diagrams in one of the lessons, and Mermaid was the obvious format for that.

When I tried to render Mermaid diagrams to images from Python, I ran into two limitations. I could not find a Python library that rendered them directly, and the available Node.js solution launched a full browser under the hood. For something as common as Mermaid, that felt unnecessarily heavy.


Mermaid diagrams

So I asked Claude Code to implement a pure Python renderer.

I followed the same overall methodology, but used the file system instead of GitHub Issues because I did not yet know whether the project would be useful enough to justify a full setup. I created a folder, initialized a Git repository, asked the agent to put all tasks into a tracker folder, and let the filenames encode the state of each task, from .todo.md to .groomed.md to .in-progress.md, and finally into done/.

My role here was mostly to check in occasionally, point out what I did not like, and define clearer criteria when needed. Toward the end, I [also asked for benchmarks](https://github.com/alexeygrigorev/merm/tree/main/benchmark), because it was not enough for the renderer to work; it also needed to be fast enough to justify using it.


Merm performance benchmarks

The results were good enough that I published them as [merm](https://github.com/alexeygrigorev/merm), and now I use it to generate diagrams, including the ones in this article.


Here are a few examples from the [gallery](https://github.com/alexeygrigorev/merm/tree/main/docs/examples):


[CI pipeline diagram](https://github.com/alexeygrigorev/merm/tree/main/docs/examples#ci-pipeline) with Build, Test, and Deploy stages rendered by Merm


[Sequence diagram](https://github.com/alexeygrigorev/merm/tree/main/docs/examples#mermaid-readme-6) with three participants, a loop fragment, and notes rendered by Merm

## 4) Rustkyll (Jekyll to Rust)

Our [DataTalks.Club](https://datatalks.club/) website uses [Jekyll](https://github.com/DataTalksClub/datatalksclub.github.io), a static site generator written in Ruby. I still think it is a good choice for small sites, but the DataTalks.Club website has been growing for more than five years, and at this point, building it takes more than a minute on my computer.


DataTalks.Club website

That delay is long enough to interrupt the workflow. I make a small change, wait more than a minute, check the result, and repeat. Recently, I was adding a new sponsor logo, Snowplow, and even that small edit reminded me how much friction had accumulated.


Snowplow logo added as a new sponsor on DataTalks.Club

I had wanted to rewrite Jekyll in Rust for months, and this seemed like a good project to further test the methodology, so I started [Rustkyll](https://github.com/alexeygrigorev/rustkyll/).


Here, I skipped the requirements step, which turned out to be a mistake. I simply pointed Claude to our website and said, “Reimplement it in Rust using this methodology.”

The next day, I checked the output and saw that the result was tailored to our site rather than a generic engine that could support other Jekyll websites. So I had to correct the direction and ask it to find other Jekyll sites and make the implementation work for those too.


The project has now been running for three weeks, and it is far more complex than I expected. What makes it a good fit for the methodology is that the optimization target is very clear: minimize the differences between Jekyll’s output and Rustkyll’s. Once the backlog is exhausted, the agents can compare the results, identify mismatches, and create new tasks from them.


Median time over 3 runs, clean builds, no caching with Jekyll and Rustkyll compared. You can check out the full results in [docs/benchmark/results.md](https://github.com/alexeygrigorev/rustkyll/blob/main/docs/benchmark/results.md).

It is still a work in progress, but for the DataTalks.Club website is already much faster, and the visible differences between Jekyll and Rustkyll are now very small.

Here’s a video of the website running on Rustkyll. I recorded it last week, and since then I’ve improved it to roughly 2x the speed shown here:

My role is mostly to check in occasionally, make sure the agents are not idle, and push them forward when needed.


Comparing DOM trees across multiple sites to find differences between Jekyll and Rustkyll output

## 5) Codehive (Coding Orchestrator)

After running several projects using this methodology, I started seeing the same problems repeatedly.

The most common one is that the Claude Code orchestrator stops when it should continue. It can ask “shall we proceed?” and wait for hours, or report that the work is done even though there are still items in its task widget.


Claude Code stopping and waiting for input instead of continuing autonomously

Another limitation is visibility. A subagent can spend an hour doing something, and I have no way to see whether it is making progress or is stuck.

And sometimes the orchestrator ignores the process altogether. Instead of sending a task through PM grooming and QA verification, it launches the SWE directly. I had to notice that and force it back into the intended workflow.


Claude Code skipping the process and launching SWE directly without PM grooming or QA verification

On top of that, I started hitting Claude Code usage limits, which made me want a setup where I can switch between tools rather than relying on a single provider.


Claude Code session at 100%, even on a simple task

That is why I started building [Codehive](https://github.com/alexeygrigorev/codehive), a coding orchestrator that follows the methodology outlined in this article but enforces it more rigorously.


Right now, the methodology lives in markdown files, which means the agent can ignore parts of it. What I want instead is an orchestrator in which the pipeline itself is built into the application: PM grooms, SWE implements, QA verifies, PM accepts, and the role responsibilities, grooming process, acceptance criteria, and definition of done are enforced by the tool rather than through prompts.

There are a few things I want Codehive to provide:

* hard-coded methodology instead of prompt-based discipline
* multiple agent backends, including Claude Code, Codex, GitHub Copilot, and Z.ai
* non-blocking workflow, so if one task is waiting for my input, the system continues with others
* visibility into subagents, so I can inspect what they are doing and intervene when needed
* GitHub integration, so new issues automatically enter the task pool

I only started working on it recently. Right now, my main focus is still the AI Shipping Labs website, but eventually I want to invest much more into this project and write about it separately.


Summary of Codehive project: 96 issues done, ~2,195 tests across backend, web, mobile

## What I’ve Learned

Over the past month, I tried this approach on five different projects, and the main thing I learned is that complex projects benefit a lot from explicit specifications, assigned agent roles, and a defined process. Without those three elements, agents drift, skip steps, and declare things finished too early.

It still requires supervision, and I want to keep reducing my involvement so I only step in when the agents actually need me. That is the direction I am working toward now.

I will write more about this in future articles. If you want to follow along, don’t forget to subscribe.

If you want to learn about building projects with agents, we will also have a course on this as part of the [AI Shipping Labs](https://github.com/AI-Shipping-Labs/website) community.
