# Creating a Context Manifest for a Long Agent Job

I wrote this synthetic style exercise as a how-to guide, and the project details are fictional. In May 2026 I gave a coding agent a job that touched 41 files and was supposed to run for six hours. By hour two it had reread the same files three times and mixed up two database columns.

Long jobs fail in a boring way. The agent finishes a step, drops the working set from memory, and starts rereading the repository to rebuild it. Each rebuild costs tokens, and the rebuilds compound until the run drifts.

What worked was a context manifest, a single markdown file that describes everything the agent is allowed to forget. The file lists the working set, each file's role, the limits, and the refresh instructions.

I now write one for every job expected to run longer than an hour. You can build the file in about 30 minutes.

In this post, I'll share:

- what the manifest contains and where it lives
- how I list the files and assign roles
- how limits keep the agent from rereading everything
- how refresh instructions work mid-run
- what three long jobs changed in my numbers

## 1. List The Files That Matter

Walk the job end to end before you open the editor, and write down every file the agent may read or change. You want the working set rather than the whole tree.

A rough list takes one command:

```bash
git ls-files src migrations scripts
```

That prints 61 paths on my current project, and I expect to prune about a third of them in the next step. Keep the list rough at this stage.

The list also changes less often than you'd expect. My June manifest kept 38 of its 41 files through the whole run, and only the migrations moved.

## 2. Assign A Role To Every File

Each file gets exactly one role, and the role states what the agent may do with it.

We use four roles in practice:

- read only, for stable code the job must consult
- read and extend, for files the job will change
- apply once, for migrations and one-shot scripts
- ignore, for anything the job should never open

The roles live at the top of `context-manifest.md`, the file every step starts from:

```text
files:
  - path: src/pipeline/ingest.py
    role: read and extend
  - path: src/pipeline/normalize.py
    role: read only
  - path: migrations/0042_add_batch_table.sql
    role: apply once, then never edit
```

A role of read only saves real tokens, because the agent stops reopening files it can't change. On the May job, the 14 read-only files were never reopened after I added their roles.

Roles also make review faster. I can grep the manifest for `role: read and extend` and see the whole blast radius of the job in one line.

## 3. Set Limits For Tokens And Time

The manifest also states the budget, and the budget needs numbers. Without them, the agent rereads whatever it likes, and a six-hour job drifts toward twelve.

The limits block sits under the file list:

```text
limits:
  context_budget_tokens: 100000
  max_rereads_per_file: 1
  checkpoint_every_minutes: 30
```

A 100,000-token budget covers the 41-file job with room to spare, and the 30-minute checkpoint splits the run into 12 verifiable pieces. When the clock hits a checkpoint, the agent rereads the manifest before it touches anything else.

## 4. Write The Refresh Instructions

The refresh block tells the agent what to do when its context runs thin.

We keep it at the bottom of the manifest, addressed to the agent in plain sentences:

```text
When your context window passes 80 percent:
1. Finish the current file and commit your work.
2. Reread context-manifest.md from the top.
3. Write one line per completed step into progress.md.
4. Continue from the first step without a checkmark.
```

Test the refresh path before you need it. We rehearse with a five-file job that finishes in about 20 minutes, which exercises the checkpoint logic without burning a full run.

On the rehearsal, one instruction was ambiguous, and the agent wrote three progress lines instead of one per step. I reworded it to say exactly one line per completed step, and the next rehearsal behaved.

## Caveats From Three Long Jobs

My first manifest listed 60 files because I pasted the whole tree into it. The agent spent its first 20,000 tokens rereading files no step needed. The rule I took from it: a file without a role is a file to delete.

A manifest also goes stale. After you rename a file mid-job, update the manifest in the same commit, or the next checkpoint rereads a path that no longer exists.

Keep the two files apart in your head, because each one has a reader. The manifest is for the agent, and `progress.md` is for me. I read the progress file at every checkpoint, and the agent rereads the manifest.

Don't overthink the format, because the file works when it's short. Mine have stayed under 90 lines.

## Changes In My Long Runs

The May job finished in five hours and 40 minutes, about 20 minutes under its estimate. Across three jobs in June, correction rounds fell from about nine per job to three. I still check `progress.md` at every checkpoint, which takes about two minutes of reading.

The manifest doesn't make the agent smarter. It removes the decisions the agent was making badly, which is most of what I used to fix by hand.

The format has stayed the same since May, and that stability makes the reviews quick.

I'll write about the checkpoint audit in a future post. If you want to follow along, don't forget to subscribe.
