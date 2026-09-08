# What I Changed When 2026 03 20 I Turned My Telegram Bot Into A Multi Became Too Much

I started working on 2026 03 20 i turned my telegram bot into a multi because there was a concrete problem in front of me. The first version was useful enough to try, but it also showed where the workflow was becoming uncomfortable. This is what I changed, and what I learned from the result.

I did not begin with a large architecture. I followed the friction in the existing process. When one step became expensive, confusing, or repetitive, I looked for a smaller change that would remove that particular problem.

At one point, In one of my previous newsletters, I wrote about my [Telegram Writing Assistant], a bot that takes raw voice notes, text messages, and links sent to a private Telegram channel and turns them into structured Markdown drafts.​ Over time, the system expanded. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. It fetched external links, summarized long articles, organized research topics, and prepared newsletter resources. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. All of this happened inside a single context window.​ When multiple URLs or messages were processed together, the context filled up quickly. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. That led to compaction, slower responses, and occasional loss of detail. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. To address this, I refactored the workflow using Claude Code subagents. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. Instead of a single overloaded process, the system is now split into specialized agents with defined roles. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. The main agent coordinates and processes voice messages. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. Separate subagents handle research, link curation, and verification. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. In this newsletter, I describe the subagents and new capabilities that I introduced to my Telegram Assistant. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. Creating Subagents and Their Benefits Claude Code allows you to create subagents via the /agents command. I kept this part visible because it explains the decision rather than only describing the final shape.

This sequence also explains what the approach does not promise. A working example can be appropriate for its context without becoming a universal recipe. The constraints, inputs, and evaluation method still matter, so I would keep them next to any claim about the result.

I prefer this kind of workflow because it leaves a trace of the reasoning. Someone reading it can see what was fixed, what remained manual, and which parts can be changed independently. That is more useful than a polished description that hides the tradeoffs.

There is no need to add a dramatic conclusion here. The useful result is concrete: the source describes a particular problem, a set of decisions, and an outcome with limits. Those details are enough to reproduce the idea or decide that a different approach fits better.
