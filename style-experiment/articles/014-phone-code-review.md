# A Phone-First Code Review Workflow That Doesn't Feel Punishing

I wrote this piece as a synthetic style exercise. The project, dates, and measurements are fictional, while the workflow describes a mobile review setup I would actually test.

Last August, I reviewed 61 pull requests and missed an important migration bug in one named `billing-split`. I had opened the diff on a laptop during a train ride, skimmed 780 changed lines, and approved it between two station stops. The bug reached staging and cost us two days of cleanup.

In this post, I'll share:

- why I stopped reviewing large diffs on a phone

- how I split changes before they reach review

- the mobile screen I keep open

- how CI output and screenshots support the review

- what still belongs to a laptop session

## The train incident

The initial mistake wasn't phone review, but the assumption that all diffs are equally reviewable. After the billing bug, I imported our merge data for six months and grouped the 214 pull requests by size.

The distribution was uncomfortable:

- 118 pull requests changed fewer than 120 lines

- 61 changed between 120 and 399 lines

- 35 changed more than 400 lines

I found 14 of 16 defects I personally reported in the first group. In the largest group, I found 2 of 11. That sample is small and biased toward my own attention, but it explained the billing failure better than any general claim about phones.

The rule I took from the data: a phone can handle a small, well-presented review. A system change hidden behind 400 lines of edits should wait.

## Make the slice small

The next change happened before review. I asked our team to split changes by risk rather than by commit history. A pull request may touch the API, database, UI, or deployment. Each diff should explain one decision.

The `billing-split` work would now look different. The schema migration would come first in a 90-line change with a rollback command. The pricing rules would follow in a separate 170-line request. A third pull request would update the invoice screen without changing calculation logic.

We added one sentence to our definition of done: every request needs a "how to reverse this" note. For configuration, that can mean the previous value. For migrations, it has to include the tested rollback path.

The effect took two sprints to appear. Median changed lines fell from 210 to 135, while change volume stayed roughly level. Four people complained about the extra branches, and two changed their minds after their own reviews got faster.

## Give the phone context

I use a 6.4-inch phone, a foldable keyboard, and a private instance of our CI dashboard.

The phone shows four fixed panels in this order:

- request summary

- checks

- diff

- comments

I don't browse the repository from scratch on a small screen.

The request summary comes from the author and has four fields:

- user outcome

- interfaces touched

- reverse path

- evidence

If any field is empty, the review waits. This sounds rigid, but it removes the guesswork that makes mobile review exhausting. On a train, I don't want to reconstruct intent from 40 file renames.

The diff view also ignores whitespace and generated files by default. Our CI publishes a text artifact with `git diff --stat` and a list of test names. That artifact helps me understand scope without opening each generated bundle.

## Use CI evidence

The phone review starts with checks, and I read them before code. Red tests, failed lint, and slow jobs tell me whether the author already knows about an issue. On one 160-line request, CI found a migration that locked a table for 4.8 seconds in staging.

That result was enough to move the review to a laptop. I needed to look at query plans and staging data, and a 6-inch screen would have hidden the context.

For front-end changes, authors attach screenshots at 360, 768, and 1280 pixels wide. The screenshots go into the request description, with captions naming viewport and state. I once caught a truncated "Save invoice" button at 360 pixels before the branch reached staging.

CI can't catch all layout problems. Dark mode, long German text, and empty states still need human review. But the screenshots give me a starting point while I stand in a queue.

Screenshot discipline improved only after we defined three states. Every front-end request now shows the default, loading, and error states at 360 pixels. That requirement added about ten minutes to authoring, and it caught four layout defects during one sprint.

## Keep comments short

On a phone, I write one of three kinds of comments:

- a blocking issue with the failing requirement

- a question about an unstated assumption

- approval after checks and evidence look right

I save style suggestions for the laptop session or a follow-up commit. Autocorrect and small touch targets make nuanced comments risky. One of my old phone comments read "don't mutate state her", which was unhelpful even after I corrected it.

Voice dictation helps with descriptions but makes code identifiers miserable. Saying "Dollar s quote bracket open" produces text that nobody should have to read. I type identifiers, and I dictate only explanatory text.

I also limit phone reviews to 20 minutes. After that, I either approve a small request or mark it "reviewed on mobile" and continue on a laptop. A review queue shouldn't turn a commute into a second workday.

## Desk work and results

I still perform large migrations, security reviews, and performance work at a desk. Those reviews need logs, database state, profiles, and space to run commands. My phone is a review terminal for bounded decisions.

The current split works like this. Requests under 150 lines and with complete evidence get a phone review. Requests between 150 and 400 lines get a phone pass, then a laptop session. Anything larger waits.

Since September, I have reviewed 47 requests on a phone and escalated 9 to a desk. Our median review time fell from 17 to 11 hours. The missed-defect number is too small to call a trend, but no new mobile-approved request has needed a rollback.

## Lessons from mobile review

Phone review became useful when we changed the diff before it reached the phone. Small slices, declared reversibility, and machine-readable evidence matter more than a better mobile app.

The workflow respects attention instead of demanding heroics. It gives me enough context for bounded decisions and tells me when to stop. I plan to write about our review definition of done next. Subscribe if you want that follow-up.
