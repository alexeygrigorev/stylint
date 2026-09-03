# Creating a Regression Pack for a Prompt I Reuse Weekly

I keep a weekly recommendation prompt for a small reading club. In March 2026, a small wording change cut its useful output from nine suggestions to four. The prompt still sounded fine, and that was the problem.

I wrote this piece as a synthetic style exercise, and every project and measurement is invented.

After that bad week, I built a regression pack. It stores saved inputs, expected outcomes, and diff checks, and it now runs before every prompt release.

In this post, I'll cover:

- how I selected the weekly cases
- how I wrote outcome and diff expectations
- how I run the pack without making it expensive
- what changed after six weeks
- what I still review by hand

## The Weekly Prompt

The prompt reads a list of 18 to 24 articles and returns a message for 40 club members. It must pick five articles, order them, explain each pick in one sentence, and avoid articles members read in the last month.

For months, I edited the prompt in a chat window. If the output looked good, I copied it into the sender. That worked until March 14, when I added a line about avoiding duplicates.

The ambiguous line made the model treat a broad article and a narrow article on the same topic as duplicates, so it removed both. Four people replied within an hour, and the club message arrived late.

My first fix was another sentence. It raised the count to six suggestions, but two picks still repeated the same source. I needed a way to compare prompt versions on the cases I already knew.

## Select the Weekly Cases

I exported the prior 12 club messages into `reading-club/history/`. Each message already had the article list, the sent picks, and two follow-up notes. That gave me a realistic sample without inventing inputs.

I selected 12 cases rather than all 86 weeks. Six came from normal weeks, three from holiday weeks with only 18 articles, and three from weeks where members had complained. I kept one copy of every complaint because those inputs exposed the duplicate behavior.

Each case lives in one folder:

```text
cases/
  2025-11-08/
    input.md
    read-last-month.txt
    expected.md
    notes.txt
```

The input in each old case stays frozen. When the source feed adds a field, I create a new case rather than overwrite the old one. That keeps a prompt change separate from the input change.

I also added two tiny edge cases. One has exactly five eligible articles, and another has five articles where three share an author. They don't cover every possible failure, but they catch the mistakes I had already made.

## Define Outcomes and Diffs

The expected file records behavior, not exact wording. Requiring identical sentences would make every useful edit look like a failure.

Each case has three checks:

- the result contains five unique article IDs
- at least four IDs match the human-approved picks
- no excluded ID appears in the result

I store the IDs in `expected.md`, followed by a short reason.

The format looks like this:

```text
ids: a18, b04, c22, d09, e31
approved: 5/5
reason: two long reads, two practical guides, one community pick
```

After the checks, I run the old and new prompts on the same input. A script produces a unified diff of the two outputs. I don't gate release on an empty diff because I often want wording to change.

While reading the diff, I check these risks:

- changed picks
- order changes
- dropped caveats
- changed audience
- added claims

The pack caught my next mistake immediately. I shortened "explain why this helps the member" to "explain the benefit". Nine outputs became sales copy, and four invented a benefit that the article never stated. The rule I took from it: a prompt word that names evidence should stay in the prompt.

## Run It Before Every Change

The runner is 90 lines of Python. It reads each case folder, calls the model twice, writes outputs to `runs/`, and prints a one-line summary. A release passes only when all 12 outcome checks pass.

I used to run all 12 cases on every edit. That cost about $0.42 per run and took 11 minutes, which was too slow while writing. Now I use four cases during editing and all 12 before I save a prompt version.

The full run takes 8 to 14 minutes and costs around $1.80. That sounds expensive for a weekly message. But a bad send costs me an evening of replies, so the pack pays for its tokens in avoided rework. I recognize that a hobby project can tolerate more risk than a paid product.

I keep three prompt versions in Git, each with the pack summary in its commit message. If a new model produces different formatting, the same cases separate model drift from prompt drift.

Six weeks later, the pack has caught five regressions. Two were duplicate picks, two lost the reading-time caveat, and one changed the tone from plain advice to urgent recommendations. It missed one issue: the club name appeared as "Reading club" instead of its real mixed-case name. Exact capitalization now belongs to the sender, where I can test it deterministically.

## The Human Review Pass

The pack checks agreement with old decisions, but it can't decide whether those decisions still make sense. Every month, I read the three most recent outputs and mark picks I would change.

Those marks do two jobs. They become new expected outcomes when the reason is stable. They become a note in the prompt when the model misread the article. I added one sentence about preferring recent articles after three months of old picks.

The pack also assumes the input files are clean. When an article lacks a description, the prompt may guess, so I reject inputs with fewer than 80 description characters before they reach the model.

## Lessons Learned

The regression pack didn't make the prompt clever, but it made prompt changes reviewable. It let me accept a small loss on one case and reject a rewrite that sounded good but hid evidence.

The useful size was 12 cases, not 100: enough variety to catch known failures and small enough to run while I remember the edit. I plan to add a seasonal case next quarter and write more about the runner in a future article. If that sounds useful, subscribe for the follow-up.
