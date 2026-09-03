# Using an Agent as an Article Outline Reviewer

I wrote this synthetic style exercise as a build log, and all project details are fictional. In February 2026 I finished a draft about Postgres connection pooling with 1,840 words and no clear promise in the opening. A coding agent reviewed the outline and found three gaps in 40 seconds that I had missed during two evenings of editing.

I had relied on outline reviews from friends for two years. I sent a markdown file to two readers and waited three days for comments about structure and missing evidence. The feedback helped, but the delay broke my drafting flow and left weak sections in place for too long.

In this post, I'll share:

- why my outlines hid weak promises
- how I built an outline reviewer with a coding agent
- what the first review caught in a Postgres draft
- how I changed the reviewer after false alarms
- where the reviewer fits in my current drafting flow

## Outlines That Hid Weak Promises

My old outlines listed topics without stating what the reader would learn. A heading said Postgres pooling without saying whether the section covered configuration values or failure behavior. I filled the gaps while drafting and discovered the missing promise too late.

The February draft had six sections and 1,840 words. The opening promised practical settings, but two middle sections described connection errors without giving a single timeout value. I noticed the mismatch only after a friend marked two paragraphs as unclear.

I asked Claude Code, a coding assistant, to read the outline. I asked for the audience, the promise, and the evidence for each section. The first attempt returned generic comments about clarity that I couldn't act on. I needed concrete checks tied to the text rather than general advice.

My mistake was asking for broad feedback in one request. The rule I took from it: a reviewer needs narrow checks with visible output for each check.

## First Reviewer Version

I created a folder called `outline-review` with a prompt file and a Python script. The prompt asks for audience, promise, evidence, and objections for every heading. The script sends the outline markdown to the coding agent and saves the response as a review file.

The prompt file lives at `review/prompt.md` and runs through the same four checks for each section:

- who the section helps
- what the section promises
- what evidence supports the promise
- what objection a skeptical reader would raise

I ran the reviewer on the Postgres draft with one command:

```bash
uv run python review_outline.py drafts/postgres-pooling-outline.md
```

The command sends the outline text to the coding agent and writes `reviews/postgres-pooling-review.md` with one block per heading. The run took 40 seconds and used about 8,000 tokens.

The output named the audience for four sections as backend developers running Postgres 15. It flagged two sections with no promise beyond background and one section with no evidence beyond a single log line. That list gave me specific places to fix.

## Gaps The Review Caught

The reviewer flagged the opening as promising timeout values that never appeared later. The outline mentioned `statement_timeout` and `idle_in_transaction_session_timeout` in the intro, but no later section included a value or a test result. I had planned to add numbers during drafting and never did.

It also caught a section on connection errors with only one log excerpt as support. The log showed a timeout after 30 seconds, but the outline drew a general claim about pool exhaustion from that single case. The reviewer asked for a second source, such as a metric from `pg_stat_activity` or a retry count from the application logs.

The third catch involved a missing objection about PgBouncer. The draft recommended transaction pooling for a Django application without mentioning prepared statements. The reviewer noted that readers using prepared statements would hit errors under that mode and would need a note about statement handling.

I fixed all three gaps in one evening. I added timeout values with the 25-second and 45-second settings from January tests. I placed a second log sample with 14 queued connections in the error section. I wrote a note about prepared statements that lists the limitation for Django users.

## Tuning After False Alarms

The second run produced five warnings, and two of them were false alarms. The reviewer asked for benchmarks in a section that only needed a definition of pool sizing. It also asked for an objection in a closing section that summarized earlier points.

I changed the prompt to skip evidence checks for definition sections. I added a label called `type` with values like concept, guide, and recap. The script reads the label and applies only the checks that fit the section type.

The updated prompt lives in the same file and starts with an instruction:

```text
Review each heading using its type label.
Concept sections need audience and objection checks only.
Guide sections need all four checks.
Recap sections need promise and objection checks only.
```

The change cut false alarms to about one per three reviews. I tracked 11 reviews in March, and only four had a warning I ignored. The rest pointed at real gaps in promises or support.

I also added a style check for headings that state topics without promises. The reviewer marks headings like background or overview as weak and suggests a promise-led rewrite. That check improved my headings more than the other three combined.

## Current Place In My Drafting Flow

The reviewer runs before I write any draft text. I write a 200-word outline with headings and two bullets per section. I run the script, read the review file, and revise the outline until every section has a clear audience and promise.

A recent outline about SQLite backups had four sections and 230 words. The reviewer flagged one section with no evidence and one heading with no promise. I fixed both in 20 minutes and wrote the draft the next morning in 90 minutes.

The flow still has limits. The reviewer misses gaps that require domain knowledge beyond the outline text. It approved a section on vacuum settings without asking for Postgres version numbers, and I caught that omission myself during drafting.

I keep the reviewer because it shortens the wait for feedback from three days to one minute. It doesn't replace reader comments about tone or emphasis, and I still send finished drafts to two friends before publishing.

I'll write about my drafting checklist in a future post. If you want to follow along, don't forget to subscribe.
