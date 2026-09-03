# Testing Whether a Long Context Actually Helps My Workflow

I wrote this synthetic style exercise as a build log. The project, dates and measurements are fictional. In May I upgraded my coding agent to a 200,000-token context window, and my review time stayed exactly flat.

I had expected the larger window to end the constant file re-reads. Instead the agent used the extra room to consider more files, and its answers grew longer without growing more correct.

In this post, I'll share:

- how I designed the comparison
- what the three context sizes were
- how I timed review rather than vibes
- what the numbers showed per task type
- where my context budget goes now

## A Bigger Window, Same Review Time

The May upgrade moved my agent from 32,000 to 200,000 tokens of context. I replayed five familiar tasks in the first week, and each one took the same review effort as before.

Token usage tripled across those five tasks, since the agent read entire directories I would never have pointed it at. It cited files unrelated to the change in three of the five summaries.

The rule I took from May is simple. I measure context spend against review minutes, and I keep whichever size minimizes the review rather than the typing.

## Designing A Fair Comparison

Comparisons of agent setups usually vary everything at the same time, so I fixed the task list first.

I chose 12 tasks I had completed before, drawn from different corners of the repo:

- bug fixes
- small features
- refactors

Each task already had a merged diff for reference. I scored each agent attempt against that reference on a scale I defined before starting.

I scored each agent attempt on this scale:

- 2 points for a diff matching the reference behavior
- 1 point for correct behavior with extra unrelated changes
- 0 points for wrong behavior or a failed run

I ran the full task list at each context size in June. That schedule cost 36 runs over two weeks, and I reviewed every diff the same evening to keep judgments consistent. I randomized the run order across sizes, so morning freshness never favored one setup.

## Small, Medium And Large

The small size gave the agent 8,000 tokens with three named files. I chose the files by hand for each task, exactly as I did before the large-window era.

The medium size allowed 32,000 tokens with a file glob per task. I wrote one glob per task, and the agent read whatever matched, averaging 11 files per run.

The large size opened 200,000 tokens with the repository root attached. I gave no file guidance at all, and the agent averaged 47 files per run.

The run command stayed identical apart from the flag:

```bash
uv run agent --context 32k --task refactor-auth.py
```

I logged tokens, files read and wall-clock minutes for every run. The log file holds 36 rows, and each row links to the produced diff.

## Timing Review Instead Of Vibes

Review minutes are the metric I trust, so I timed them with a stopwatch app. I started the timer when I opened the diff, and I stopped it when I wrote the verdict.

The small size averaged nine review minutes per task. Diffs stayed narrow, and failures looked like missing context I could name in one sentence.

The medium size averaged 11 review minutes per task. Diffs included two extra files on average, and I spent the extra minutes verifying those files were harmless.

The large size averaged 17 review minutes per task. Diffs touched a median of six files, and two runs edited shared utilities for reasons the summaries never explained.

## Scores And Review Minutes

Scores favored the small size by a narrow margin, and the large size trailed badly. Small averaged 1.6 points, medium averaged 1.5, and large averaged 1.1 across the 12 tasks.

The gap concentrated in bug fixes. Small scored 1.9 on the four bug tasks, while large scored 0.8, because the large runs kept refactoring neighbors of the bug. I reran two bug tasks to confirm the gap, and both reruns reproduced the same ordering.

Refactors reversed the order slightly. Large scored 1.7 against 1.4 for small, since the extra files helped in exactly the two tasks where the refactor crossed module lines.

I kept the per-task table in the experiment log:

```text
experiments/context-sizes-2026-06.md
```

That file records every score with its diff link and review minutes. When anyone asks why I cap context, I point at the bug-fix rows.

## My Context Budget Today

I run the small size by default and escalate deliberately. Four of five weekly tasks stay at 8,000 tokens with files I choose myself, and the fifth gets the medium size with a glob.

Large context now requires a written reason before the run. Cross-module refactors qualify, and everything else needs to earn the extra review minutes first. The written reason takes one sentence, and the bar stays deliberately high.

Two habits keep the budget honest:

- I name the input files for every run under 32,000 tokens
- I log tokens and review minutes for anything larger

New tasks inherit the small default from my agent config. I raise the budget only after a small run fails for clearly visible lack of context.

I'll cover the file-picking heuristic in detail in a future post. If you want to follow along, don't forget to subscribe.
