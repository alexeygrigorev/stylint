# Creating a Progress Board for Parallel Agent Work

This synthetic style exercise follows a fictional practitioner with invented numbers and events. Nothing here describes a real project. In June I ran four coding agents against a backlog of thirty tasks.

The idea looked efficient on paper with each agent owning a slice. Within two days I lost track of who owned what. Two agents edited the same billing module and produced conflicting patches.

I first tracked ownership in my head plus scattered chat transcripts. Each agent reported progress in its own session log. Reconstructing the state of all four took twenty minutes every morning.

The collision wasted most of a Friday afternoon because both agents rewrote the refund function from different assumptions. I discarded one patch entirely and kept twelve lines from the other.

In this post, I'll share:

- why four parallel agents outran my memory
- how I built a shared progress board
- how tasks move across ownership and status
- how artifacts and the merge queue stay ordered
- what the board costs and where it still falls short

## Four Agents Outran Memory

One agent is easy to supervise because its log tells one story. Four agents tell four stories with overlapping files and silent assumptions. I reviewed 400 lines of agent output daily without a map.

The first collision came from vague task text, and two tasks both mentioned refunds without naming files. Each agent reasonably claimed the billing module and started editing.

I tried a spreadsheet with task rows and owner columns. It rotted within a day because only I updated it. The agents never read it, so their claims diverged from my rows by evening.

The rule I took from that week: ownership must live in one file, and every agent must read that file before editing.

## Building the Shared Board

I keep the board as a single Markdown file at the repo root. Each row holds an ID plus title, owner, status, and artifact link. Four agents plus me read the same thirty rows.

I wrote Steward, a small script for this task, to validate the board on every update. It rejects unknown owners, illegal status jumps, and rows without artifact links when status says done.

Claiming a task takes one command:

```bash
uv run python scripts/claim.py T014
```

The command stamps the caller name and the current time into the row. It refuses the claim when another owner holds the task in progress.

Status values stay small on purpose with five allowed words:

- backlog for unclaimed work
- claimed for reserved tasks
- in-progress for active edits
- review for finished patches awaiting checks
- done for merged work with artifacts linked

Board validation runs in CI on every push in about nine seconds. A bad edit fails fast with the row number and the reason. That check caught seven malformed updates in the first fortnight.

## Ownership and Status in Motion

Tasks move forward through the statuses toward done without skipping stages. Skipping from claimed to review is rejected because nobody saw active work. The restriction sounds rigid and it prevented two silent drops.

Each agent reads the board at session start and claims a task. The claim command prints the task text plus the files from the last similar task. That context cut wrong-file edits from six to one per week.

Handoffs happen through the board with no direct messages. An agent stuck for more than an hour marks its row blocked with a note. I reassign blocked rows each evening in about ten minutes.

The evening triage follows the same order daily:

- release rows blocked longer than a day
- split rows that grew past a 200-line diff
- merge reviewed rows with green checks

One habit matters more than the rest of the process. Agents update the row before writing code and after tests pass. The board then reflects intent first and evidence second.

## Artifacts and the Merge Queue

A status of done means nothing without the linked evidence. Each finished row points at its diff, test log, and a two-line note. I review the note first and open the diff second.

Artifact links follow one layout so scanning stays fast:

```text
artifacts/T014-diff.patch
artifacts/T014-tests.txt
artifacts/T014-note.md
```

The note says what changed and how the agent verified it in plain sentences. Notes longer than six lines get sent back for trimming.

Merging runs through a strict queue with the oldest reviewed row first. I merge the row, run the full suite of 214 tests, and mark it done. The suite takes six minutes, so I batch a few merges per session.

Queue discipline survived a stressful Thursday with nine rows in review. I merged five, sent three back for missing tests, and split one oversized diff. No patch waited longer than a day.

The [GitHub flow guide](https://docs.github.com/en/get-started/using-github/github-flow) shaped the queue rules. We kept branches short-lived with one merge at a time, and conflicts stayed near zero.

## Lessons From the Board Trial

The board paid off across three weeks of parallel work. Twenty-six of thirty tasks merged with linked artifacts. Task collisions dropped from three per week to zero after the board arrived.

One gap remains around ambiguous task text. Two tasks still overlapped on notifications because neither named the module. I now require file paths in every task title before agents start.

I keep three habits from this trial for any multi-agent stretch. I store ownership in one file every worker reads. I reject status jumps that skip visible work. I merge through a queue of one with tests each time.

Four hours of building saved roughly fifteen hours of reconstruction and rework. That trade looks fine to me, and I'd repeat it whenever more than two agents share a repo.

I'll write more about supervising parallel coding agents without losing the plot in a future post. If you want to follow along, don't forget to subscribe.
