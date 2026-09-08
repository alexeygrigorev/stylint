# A Practical Way to Think About 2026 03 20 I Turned My Telegram Bot Into A Multi

When people talk about 2026 03 20 i turned my telegram bot into a multi, the implementation can sound more complicated than it is. The useful way to understand it is to start with the job the system has to do, then separate the pieces that make that job reliable. I will walk through the approach described in the source and the reasons behind its choices.

The important part is the connection between a constraint and a design decision. A component is there because something else needs it. If that reason disappears, the component may no longer be necessary.

Start with this fact: In one of my previous newsletters, I wrote about my [Telegram Writing Assistant], a bot that takes raw voice notes, text messages, and links sent to a private Telegram channel and turns them into structured Markdown drafts.​ Over time, the system expanded. For the reader, the practical implication is to keep this step explicit and check it before adding another layer.

The same pattern appears here. It fetched external links, summarized long articles, organized research topics, and prepared newsletter resources. For the reader, the practical implication is to keep this step explicit and check it before adding another layer.

The same pattern appears here. All of this happened inside a single context window.​ When multiple URLs or messages were processed together, the context filled up quickly. For the reader, the practical implication is to keep this step explicit and check it before adding another layer.

The same pattern appears here. That led to compaction, slower responses, and occasional loss of detail. For the reader, the practical implication is to keep this step explicit and check it before adding another layer.

The same pattern appears here. To address this, I refactored the workflow using Claude Code subagents. For the reader, the practical implication is to keep this step explicit and check it before adding another layer.

The same pattern appears here. Instead of a single overloaded process, the system is now split into specialized agents with defined roles. For the reader, the practical implication is to keep this step explicit and check it before adding another layer.

The same pattern appears here. The main agent coordinates and processes voice messages. For the reader, the practical implication is to keep this step explicit and check it before adding another layer.

The same pattern appears here. Separate subagents handle research, link curation, and verification. For the reader, the practical implication is to keep this step explicit and check it before adding another layer.

The same pattern appears here. In this newsletter, I describe the subagents and new capabilities that I introduced to my Telegram Assistant. For the reader, the practical implication is to keep this step explicit and check it before adding another layer.

The same pattern appears here. Creating Subagents and Their Benefits Claude Code allows you to create subagents via the /agents command. For the reader, the practical implication is to keep this step explicit and check it before adding another layer.

This sequence also explains what the approach does not promise. A working example can be appropriate for its context without becoming a universal recipe. The constraints, inputs, and evaluation method still matter, so I would keep them next to any claim about the result.

I prefer this kind of workflow because it leaves a trace of the reasoning. Someone reading it can see what was fixed, what remained manual, and which parts can be changed independently. That is more useful than a polished description that hides the tradeoffs.

There is no need to add a dramatic conclusion here. The useful result is concrete: the source describes a particular problem, a set of decisions, and an outcome with limits. Those details are enough to reproduce the idea or decide that a different approach fits better.
