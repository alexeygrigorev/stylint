# Writing a Comment Policy for AI-Generated Code

I wrote this synthetic style exercise as an analysis piece, and the projects, dates and counts are fictional. In March 2026 I reviewed 240 merged commits across three agent-assisted projects and collected the 1,900 comments a coding agent had written along the way. About six in ten only restated the line sitting under them.

That count pushed me to write a five-line comment policy for AI-generated code and to measure whether it changes anything. Two months of commits later, I have an answer with caveats.

In this post, I'll share:

- the four claims the policy rests on
- the audit numbers behind the narration complaint
- the policy text I added to the agent instructions
- how agents and reviewers complied over two months
- the lessons I'd keep for the next project

## 1. A Comment Earns Its Place With A Reason

The comments I chose to keep all explained a decision the code couldn't show. One read `# retry twice because the payment API returns 502 during deploys`, and it saved me an hour of guessing in April. A reason names a constraint or a trade-off the code can't show on its own.

Reason comments also aged well across refactors. The retry comment stayed true after three rewrites because the 502 behavior never changed, while the code around it changed twice. It even worked as onboarding material. A new contributor joined one project in May and read the deploy script top to bottom. The two constraint comments answered his only question before he finished the file.

Comments that explain a decision transfer to a new reader, while narration transfers to nobody.

## 2. Narration Restates The Code

Narration comments describe the next line in English: `# increment the counter` above `counter += 1`. The reader gets a second copy of the same fact with zero added information. In my audit, 61 percent of the 1,900 comments were narration and 22 percent gave reasons. The remaining 17 percent marked warnings.

I classified the comments by hand in a spreadsheet, so the buckets overlap at the edges. Every number here includes one pass of my own judgment.

The warning bucket was the smallest and the least useful. Warnings like `# careful, this runs on prod` expressed worry without naming the mechanism. Six of those nine described limits that a test could have enforced instead.

## 3. Temporary Code Needs The Most Words

Workarounds and temporary branches need comments with dates and ticket names. My policy asks for a removal condition in the same line, like `# rollback path for the March schema change; delete after ticket 412 ships`.

TODO comments without dates survived past the release in 14 of 17 cases. Comments with dates got cleaned up in 8 of 10, so the date does most of the work. A comment that names its own expiry turns cleanup into a searchable task instead of an archaeology project.

The ticket-name half matters as much as the date. A named ticket links the comment to a discussion with the full reasoning, and `git blame` then finds that context in one step.

## 4. The Policy Works Best Inside The Agent Prompt

I first added the policy to `CONTRIBUTING.md`, where it changed review comments but left the generated code untouched. Moving the same five lines into the agent instructions file changed the generated code within a week. That file lives at `.claude/CLAUDE.md` in each repo, next to the test commands and project conventions.

My first draft banned narration with one blanket sentence, and the agent stopped writing workaround comments in the same week. The rule I took from it: ban a category with examples, never with a single word.

The final policy reads:

```text
1. Explain decisions the code can't show.
2. Skip narration that restates the next line.
3. Workarounds need a date and a ticket name.
4. Temporary code needs a removal condition.
5. Reviewers reject comments that fail the first four.
```

Line 5 gives reviewers a concrete rejection reason, which mattered more than I expected. Review comments like 'trim this comment' became 'line 2 applies here'.

## After Two Months

Across 190 agent-written commits since April, narration fell from 61 percent to about 30 percent, and reason comments doubled to 45 percent of the total. The agent still writes narration in roughly one commit in ten, mostly inside test files where the assertion names already read like plain sentences.

Reviewers are the remaining gap. Under deadline pressure they still approve vague comments, and I have no number for how often that happens, because approval says nothing about comment quality. The audit took me two evenings, and I plan to repeat it every quarter with the same spreadsheet.

A second limitation concerns the sample. Two of the three projects shipped mostly Python, so my data underrepresents frontend code, where JSX tends to need fewer comments anyway. I don't treat the percentages as universal constants. They describe three small backend projects with one reviewer, and that reviewer was me.

The arc compressed: count, write the rule with examples, then count again. Comments still can't be tested the way code can, so the policy stays a review tool with measured and modest effects.

I'll write about review checklists for agent diffs in a future post. If you want to follow along, don't forget to subscribe.
