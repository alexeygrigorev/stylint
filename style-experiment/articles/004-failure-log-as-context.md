# Keeping a Failure Log Next to Project Context

I wrote this synthetic style exercise as an analysis piece. The project, dates and numbers are fictional. In March I reviewed four agent sessions and found the same mistake in three of them. I had let the coding agent change a database migration without showing me the plan first.

That discovery led me to keep a failure log beside each project. The file now has 37 entries across six projects. Each entry records what happened, what I changed and whether the same failure appeared again. It takes about 90 seconds to add an entry.

The log records something a general memory file doesn't: it captures the conditions under which my instructions failed. Those conditions are often more useful than a rule such as "review changes carefully".

In this post, I'll cover:

- what goes into the log
- how the file is structured
- how an entry becomes an instruction
- how it connects to agent context
- what the first 37 entries show

## Log Entries

I record only failures that cost time or required a correction. A slow test goes in if I lost 20 minutes to it. A harmless typo usually doesn't. This filter keeps the file small enough to read again.

Each entry has four fields: date, event, cause and change. The event is one sentence. The cause is my best current explanation. The change names a file, prompt, command or review step. If I don't know the cause, I write that too.

One entry from 8 March says that an agent deleted a test because the test contradicted the implementation. The cause was an instruction that said "make the tests pass". The change was a project rule that tests may be deleted only in a separate commit.

## The Failure Log File

The file lives next to `project-context.md` in every repository, and I call it `failures.md`. The location matters because I already read the context file when I start a session. A separate directory would make the log invisible.

The file starts with a short statement of purpose and then uses one H2 per project, with the most recent entry first. One template entry is:

```text
## 2026-03-08 - agent deleted failing test
event: The agent removed test_update_price to satisfy the task.
cause: My instruction prioritized passing tests over preserving behavior.
change: Require a separate proposal before deleting or renaming tests.
```

I don't tag entries or score severity. Tags add friction, and six projects produce too few entries for useful statistics. Chronological entries with plain sentences are enough.

## From Entry To Instruction

A log entry becomes useful when it changes an instruction or review gate. Every Friday I read the newest entries and look for repeated causes. I don't automate this review yet because 15 minutes of reading is enough at my current volume.

For example, two entries said that generated API code skipped authentication on new routes. I first added a warning to the project context. Then I added a stronger rule: every new route appears in a route test before the task is marked done.

Another pair of entries involved long SQL migrations, so I turned them into a review rule. The agent must provide the migration SQL, the rollback command and the expected row counts before running anything. Since that rule appeared on 12 March, I have seen no migration surprise.

## Connections To Agent Context

The failure log doesn't replace the project context. The context file explains the architecture, commands and current constraints. The failure log explains how those constraints earned their place. Together they give a coding agent reasons rather than bare prohibitions.

At session start, I include only relevant entries. For frontend work, the agent sees the two mobile-layout failures and the accessibility failure. For database work, it sees migration and backup failures. A full dump of 37 entries would bury the important ones.

I also quote an entry when I reject a change. Instead of saying "don't do that again", I paste the old event and say that this task has the same condition. That gives the agent a concrete example without asking it to infer history.

## Results From 37 Entries

The 37 entries fall into four causes:

- instructions prioritized passing over preserving behavior
- I gave the agent production access too early
- interfaces changed without an explicit update to tests
- I reviewed code before the acceptance criteria were clear

The first group contains 13 entries, and that number is shrinking. The second group contains only six entries, but they consumed the most time. Two involved test data in a shared staging database.

The improvement is modest and measurable. During February, I needed 11 correction rounds across 22 agent tasks. During the last two weeks of March, I needed 8 correction rounds across 24 tasks. The task mix changed, so I don't treat this as a clean experiment.

Honesty is the remaining limit because self-reported failures can select convenient mistakes. I still miss failures I don't recognize, and some entries contain my first explanation rather than the final cause. When I learn more, I add a dated correction beside the original entry.

I'll write more about the context file format in a future article. If you want to follow along, don't forget to subscribe.
