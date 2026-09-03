# Classifying the Ways a Coding Agent Fails

I wrote this synthetic style exercise as an analysis essay. The project, dates and measurements are fictional. Since March I log every failed coding-agent run in a review file, and the log holds 142 failures across nine projects.

Four shapes repeat through those failures. Instruction errors, context errors, tool errors and judgment errors cover 131 of the 142 cases, and the remaining 11 split across infrastructure flakes. I review the log on the first Monday of each month, and each session takes about 40 minutes.

In this post, I'll share:

- the four error classes, stated bare
- how instruction errors look in practice
- how context errors differ from instructions
- how tool errors masquerade as reasoning
- how judgment errors survive good inputs
- what the classification changed in my prompts

## Four Classes, Stated Bare

The taxonomy holds four classes, and each class points at a different fix. I list them here once, then cover each in more detail below.

1. Instruction errors, where the brief allowed the failure
2. Context errors, where the agent missed files it needed
3. Tool errors, where the harness broke the run
4. Judgment errors, where good inputs still produced bad calls

Those classes emerged from tagging 60 failures by hand in April. I tried six classes first, and two of them never collected more than five cases each.

## 1. Instruction Errors

Instruction errors are mine, not the model's. The brief omitted a constraint, named two goals, or described the done state in adjectives instead of checks.

The classic case asked for "faster exports" without a number. The agent optimized memory usage from 400 MB to 90 MB while runtime stayed at 40 seconds, and the requester had wanted speed.

These errors dominate my log at 58 of 142 cases. They also cost the least per case, since a tightened sentence in the brief prevents the entire class. A March brief asked for a cleaner dashboard with no definition of clean. The agent removed three panels the team used daily, and the fix was one sentence naming the panels to keep.

## 2. Context Errors

Context errors mean the agent never saw the deciding file. It read the caller but not the config, the tests but not the fixtures, or the new module but not its two siblings.

One May run rewrote an auth helper while missing the middleware that constrained it. The helper passed its unit tests, failed integration, and wasted 90 minutes of review before I spotted the absent file.

These errors account for 34 of 142 cases. They cluster in repos above 50 files, where my manually chosen file lists thin out fastest. I now attach middleware and config files to every auth-area brief by default. That habit cut auth-area context errors from nine to one across the spring.

## 3. Tool Errors

Tool errors break the run outside the reasoning layer. Timeouts kill long generations, truncated outputs cut diffs mid-file, and stale caches serve yesterday's test results as today's.

An April run failed three times on the same task before I checked the harness. The sandbox had frozen the system clock, every timestamp assertion failed, and the model had debugged its own correct code for an hour.

These errors total 21 of 142 cases. They look like stupidity in the transcript, and the fix always lives in the runner rather than the prompt. I now run a five-minute harness check before any overnight job. The check asserts clock sanity, cache freshness and disk space, and it has caught two bad sandboxes since May.

## 4. Judgment Errors

Judgment errors are the residue after instructions, context and tools check out. The agent saw the right files, understood the brief and still chose the worse of two reasonable designs.

A June run faced a genuine fork in a queue design. It chose at-least-once delivery with dedup logic over exactly-once semantics, doubling the code for no stated reason.

These errors number 18 of 142 cases. They concentrate in design-heavy tasks, and they resist prompt tweaks more stubbornly than the other three classes. I handle these by narrowing the decision before the run. When I spot a genuine fork, I choose the design myself and brief the agent on implementation only.

## Debugging In Fixed Order

The classification redirected my debugging order. I now check the brief first, the file list second and the harness third, and I consider judgment explanations only after those three pass.

That order cut my debugging time roughly in half. Instruction fixes take minutes, context fixes take one more file, and tool fixes take a config change. Judgment cases earn a careful re-brief or a manual implementation.

The counts also settled a debate with myself about model quality. Four of five failures trace to my inputs or my harness, so switching models would have addressed about 13 percent of the log.

I retag the log monthly in a single sitting. New failures join their class in minutes, and a class that doubles in a month earns a dedicated fix the same week. The log also tracks fix time per class, and that data justified the kickoff template I now write for every task.

I'll publish the tagging guide and the log schema in a future post. If you want to follow along, don't forget to subscribe.
