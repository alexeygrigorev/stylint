# What I Changed When 2026 04 03 I Built An Ai Agent Team For Software Became Too Much

I started working on 2026 04 03 i built an ai agent team for software because there was a concrete problem in front of me. The first version was useful enough to try, but it also showed where the workflow was becoming uncomfortable. This is what I changed, and what I learned from the result.

I did not begin with a large architecture. I followed the friction in the existing process. When one step became expensive, confusing, or repetitive, I looked for a smaller change that would remove that particular problem.

At one point, Over the past few weeks, I’ve been trying out a new way of working with agent teams for software development using Claude Code. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. Instead of just seeing it as a single tool, I’ve started thinking of the main session as an orchestrator that directs a small team of agents. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. I’ve tested this setup on a few projects now, and while it’s still a work in progress, I can already see what works, what doesn’t, and what controls are needed to let the agents build real projects with minimal oversight. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. In this post, I’ll share what my setup looks like: how I describe the agents, how they interact, how it all fits into a single-team workflow, and how I used this approach to build five different projects. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. Background For small tools, I usually dump my idea into my [Telegram Writing Assistant] or [talk to ChatGPT] to refine it (or both). I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. I iterate with Claude until the concept works. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. This approach is sufficient for smaller utilities or projects that I can easily manage. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. But it falls short for more complex projects with too many moving parts and tasks at different stages. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. For example, it doesn’t provide a way to verify the agent’s claims that a task is complete or test that it was implemented correctly according to the plan. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. That’s why I decided to try building a team of agents, each with their own role, with the main session serving as the orchestrator: it launches agents, assigns tasks among them, ensures compliance with the process, and only commits the work after the final acceptance step is completed. I kept this part visible because it explains the decision rather than only describing the final shape.

This sequence also explains what the approach does not promise. A working example can be appropriate for its context without becoming a universal recipe. The constraints, inputs, and evaluation method still matter, so I would keep them next to any claim about the result.

I prefer this kind of workflow because it leaves a trace of the reasoning. Someone reading it can see what was fixed, what remained manual, and which parts can be changed independently. That is more useful than a polished description that hides the tradeoffs.

There is no need to add a dramatic conclusion here. The useful result is concrete: the source describes a particular problem, a set of decisions, and an outcome with limits. Those details are enough to reproduce the idea or decide that a different approach fits better.
