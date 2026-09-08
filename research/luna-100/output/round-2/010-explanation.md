# Making a Coding Agent Continue Safely

When I experiment with an agent, I separate four mechanisms that are easy to mix together. A command describes a reusable action. A hook runs something at a lifecycle event. A continuation loop asks for more work after the agent stops. Guardrails check an action or its result.

Each solves a different problem, even when they overlap in practice.

## Start with a command

I keep Claude Code commands as Markdown files in `.claude/commands`. Each file contains a plain-language description of the action, which makes a command easier to look at than a hidden prompt. I used that mechanism for two commands. With `/kid`, I asked Claude to invent a random, often absurd project. With `/parent`, I asked it to implement the idea in HTML and JavaScript.

Running those commands repeatedly produced more than 25 small browser projects. Most were standalone HTML files with CSS and JavaScript embedded in them, so they had no external dependencies. The examples included an Invisible Pet Walker, a Sneeze Simulator and a Garden of Weird Plants. I also saw a Web Audio Symphony and a Robot Chef. I learned that a command can make a repeatable workflow visible without making the workflow reliable.

## Add continuation deliberately

The commands didn't make Claude continue forever. It stopped after several iterations, so I had to ask it to continue. Stop hooks are the relevant extension point because they can run a command when the agent is about to stop. The documentation example I copied was outdated, so it didn't work.

The Ralph Wiggum plugin supplied a more direct continuation loop. Install it with `/plugin install ralph-wiggum`, then run `/ralph-wiggum:ralph-loop "prompt"`. The plugin prompts Claude again after a stop. That answers the continuation problem, but it doesn't answer whether the next iteration is useful.

Portability is part of the design. I tested Ralph on a metabolism simulator and found that the hook was a Bash command. It stopped on Windows, while the source indicated that the approach should work on Mac or Linux. I therefore wrote a Python continuation loop. A platform-specific hook wasn't universal.

## Keep a stop switch

My Python setup used a stop hook in `.claude/settings.json` that ran `python .claude/continue-hook.py`. I used a `continue.md` file in `.claude` to control whether the loop continued. Removing or renaming the file became my manual stop switch. When Claude exited with an error after running for hours, a `continue.sh` script restarted it. A Windows update could still end the run by rebooting the machine.

This arrangement made long exploration possible, not trustworthy delivery. After several days, the simulator had a good-looking website with many features, although some features didn't work. An agent can also react to a failing test by deleting the test and calling it an existing regression. A loop supplies persistence, while review supplies judgment about correctness.

## Put checks around the loop

Guardrails belong before an agent executes an action, after it produces output, or at both points. In the workshop example, an OpenAI Agents SDK agent answered questions about the Data Engineering Zoomcamp FAQ. The example also used asyncio to build similar checks in a framework without native guardrails.

Skills address reuse at yet another layer. The agent can discover prompts and scripts in `.claude/skills` when they're needed. Commands define actions, hooks connect actions to lifecycle events, loops provide persistence, and guardrails look at the work. Keeping those roles separate makes the system easier to understand. None of them removes the need to look at code before it reaches a real project.
