# The Project Retro Template I Reuse After Every Build

In August 2026 I finished a CSV validator, a documentation linter, a course search tool, and a Telegram reminder bot. All four side projects ran in ten weeks. Only the documentation linter became part of my weekly work.

I wrote this as a synthetic style exercise with invented projects and numbers. I still use the same retrospective template to decide which experiments deserve more time.

In this post, I'll share:

- the five fields I record for every project
- how I gather evidence before writing a retro
- how I separate surprises from ordinary delays
- how I choose the next rule to record
- what this template revealed across the four builds

## Five Stable Fields

Every retrospective starts with the same five fields:

- outcome
- evidence
- surprises
- time and cost
- next rule

The outcome field says what shipped and who uses it. Evidence can include command output, a repository tag, a screenshot, or a usage count. I write the evidence before the judgment, because a project can feel finished without a working path.

For the Telegram bot, the outcome took two sentences. The bot sent 312 reminders for four recurring commitments over 30 days. It still can't handle a change to a recurring schedule without manual deletion and recreation.

The CSV validator had a narrower outcome. It validated 18,000 rows on demand and found 64 malformed dates. I used it five times, then stopped after fixing the source export.

## Gather Evidence First

Before writing judgments, I collect the artifacts in one folder.

Each project folder includes the final commit, test output, README, and local notes.

I also gather any logs that show real use.

A simple file layout keeps the evidence comparable:

```text
retros/2026-08/
  csv-validator/
    commit.txt
    test-output.txt
    usage.log
    retro.md
  doc-linter/
    commit.txt
    test-output.txt
    usage.log
    retro.md
```

I spend 20 to 30 minutes per project on this step. It sounds heavy for side work, but it prevents a retrospective from turning into a story about however I felt that day.

For the documentation linter, `usage.log` showed 41 runs over six weeks. Twenty-eight runs found at least one banned phrase or broken command. That evidence made the decision to keep the tool easy.

For the course search tool, the log showed only 11 searches after launch. That number led to a different conclusion than "the implementation works".

## Separate Surprises from Delays

I record delays and surprises in separate sections. A delay often has an ordinary cause, such as a package upgrade or a week of travel. A surprise changes what I believe about the problem.

The reminder bot had one surprise. Recurring events looked simple until daylight-saving time entered the test data. I had to distinguish between a user's fixed local time and an absolute UTC moment, which added six hours and 120 lines of code.

The course search tool had an ordinary delay. Switching from SQLite full-text search to a small embedding index took two extra days. The search worked either way, so the extra work didn't reveal a false assumption.

This separation keeps the useful lessons visible. A delay may disappear next time, while a surprise usually deserves a written rule or a new test.

## Record One Rule

The template ends with a single next rule. One rule is small enough to remember and concrete enough to test during the next build.

After these four projects, I chose this rule for September.

Before building a search interface, log a dummy query endpoint and ask three likely users to try it.

That rule came directly from the course search project. Eleven searches was too few to justify polishing the interface, and I had built the full UI before checking how colleagues would phrase their questions.

For the reminder bot, I wrote a smaller maintenance rule. It requires the recurring-event schema in `scheduler-schema.md` and a test around every timezone change. For the CSV validator, I recorded the opposite decision. I archived the tool because the source data improved and the problem went away.

The documentation linter already had a standing rule. Every banned phrase needs a test example and a suggested replacement. That rule kept the linter useful without making it preachy.

## Four Projects Compared

The comparison looked like this after ten weeks:

- documentation linter: 41 uses, kept
- CSV validator: 5 uses, archived
- Telegram reminder bot: 312 reminders, kept with maintenance
- course search tool: 11 searches, paused

Total build time was 94 hours. The documentation linter took 22 hours and became a weekly tool. The course search took 31 hours and exposed a demand question rather than a coding problem.

The reminder bot cost $2.40 in hosting over the month. The other three ran locally and had no direct monthly cost. Those numbers show the tradeoffs directly.

Without the template, I would probably have remembered the bot's timezone bug and the search tool's polished interface. I would have forgotten that the linter found real issues in 68% of its runs.

## Final Lessons

The template doesn't guarantee success for every project, but it forces every retrospective into a small action set:

- keep
- maintain
- pause
- archive

Evidence comes first, surprises get separated from ordinary delays, and each project leaves at most one reusable rule. That structure is enough for side work without becoming another project to maintain.

I plan to publish the blank template and a filled example next month. Subscribe if you want to reuse it.
