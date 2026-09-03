# Creating a Cost Report for Agent-Assisted Development

I wrote this build log as a synthetic style exercise, and the token counts, invoices, and time estimates are fictional. In the invented project, I audited 126 agent-assisted changes across a Ruby monolith and a React dashboard during July 2026.

My monthly invoice told me the total, and the total told me nothing useful. I needed to know which changes consumed tokens, which retries drove the bill, and where agent assistance actually saved engineering time. I gave myself two weeks and a budget of 18 hours.

In this post, I'll share:

- the run metadata I had to add
- how I matched runs to merged changes
- the report fields I settled on
- what the first month showed
- how those numbers changed my workflow

## Missing Run Metadata

The first problem was evidence. Claude Code and Codex both exposed session transcripts, but the sessions didn't share a project ID or change number. I had 239 transcripts and no reliable way to connect them to 126 merged changes.

I changed the kickoff template first. Every agent task now started with a change ID, requested scope, model, and maximum budget.

```text
change_id: RAILS-2187
repo: billing-api
scope: split invoice tax calculation into a service object
model: claude-sonnet-4
max_minutes: 35
```

This small record made later analysis possible. It also reduced scope drift because the agent could reread the change ID and scope in context. I rejected 11 prompts during the first week for omitting one of those fields.

For local runs, I used a `runs/` folder beside the repository. Each attempt stored the original prompt, full transcript, Git diff, and result record.

The result recorded exit status, changed files, test output, and an error class.

## Matching Runs to Changes

I wrote a 210-line Python script to match attempts with changes. It compared Git commit messages to change IDs, checked diff overlap with the requested files, and used commit timestamps plus or minus 12 hours.

The script matched 121 of 126 changes. Four unmatched changes came from interactive fixes outside the normal template.

The fifth had two tickets in one branch. I left all of those changes out of the per-change report and counted them separately as "unstructured work".

Next, I grouped attempts by change ID. A change could have several runs because I stopped an unpromising attempt, hit a test failure, or asked for a narrow revision. The report counted both attempts and completed runs.

For example, `RAILS-2187` had three attempts. The first ran for 11 minutes and produced a design note instead of code. The second failed tests after 19 minutes. The third ran for 24 minutes, changed six files, and passed 43 tests.

## Report Fields

The report needed enough detail to make a decision without turning into telemetry theater. I reduced it to one row per merged change and kept 14 columns.

The important fields were these:

- attempts and total agent minutes
- input tokens, output tokens, and cache hits
- model and measured API cost
- review minutes and rework minutes
- status, test count, and changed-file count
- reviewer judgment on novelty and risk

I measured my own time with Toggl, a time-tracking service. For agent minutes, I used the session transcript rather than wall-clock time, because several sessions sat idle while I attended meetings.

Cost calculation had one deliberate gap. Some providers bundle usage with other platform spending, so I recorded metered model cost and marked bundled platform fees separately. The July metered total was $418.27, and the bundled platform invoice added another $210.

## First Month Results

The metered model cost per merged change had a median of $1.84 and a mean of $3.45. That gap mattered because nine changes consumed $189.60, or 45% of the total.

Retries explained most of the expensive tail. The nine costliest changes needed an average of 4.3 attempts and 94 agent minutes. The other 112 changes needed an average of 1.5 attempts and 27 agent minutes.

Human time told a more surprising story. Median review time was 16 minutes, but rework added another 22 minutes on 37 changes. Four changes generated 11 hours of rework because the reviewer and I had misunderstood the tax rules.

I also compared the result with my manual estimate. Without an agent, I would have needed about 74 hours for the 121 matched changes. The recorded work used 54.3 agent hours, 34.1 hours of my time, and cost $628.27 in total tool spending.

That estimate is generous to the agent. I knew the codebase, and some changes were candidates for deletion rather than implementation. Still, the evidence supported continued use for isolated service extraction and frontend component changes.

## Changes to the Workflow

The report changed how I assigned tasks. I now split work into changes that touch fewer than eight files, require one test path, and have a reviewable design note. Those constraints came directly from the expensive tail.

I stopped using agents for broad migrations. They looked impressive in a diff, but two migrations consumed 28% of the model spend and required the most rework. A small script plus human review handled the next 42-file migration in six hours.

Budget caps became visible at kickoff. For ordinary changes I set 30 agent minutes and 20,000 output tokens. For exploratory work I allowed 90 minutes, but the task had to produce a written decision and a recommendation to continue or stop.

The final adjustment was to review earlier. On changes costing more than $5, I reviewed the first passing draft before polish. That shift caught three wrong assumptions before the agent built additional code on them.

## Lessons

A cost report is useful only when it preserves the decision context. Change ID, attempt count, review time, and rework matter more than a monthly invoice total.

The biggest win came from grouping work by size and novelty. Cheap changes became boring and repeatable. Expensive changes became a prompt for human design discussion before another agent run.

I plan to write about the budget-cap implementation in a future article. Subscribe if you want the report template and the exact SQL I used.
