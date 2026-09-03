# Curating FAQ Answers Without Making It a Full-Time Job

I wrote this article as a synthetic style exercise. Although the community and measurements are fictional, the maintenance workflow is one I would test on a real FAQ.

In January 2026, a Python course community I help moderation for had 1,842 unanswered FAQ candidates. Four helpers answered questions in chat, and each person had a private collection of saved replies. The same timeout error could receive three useful answers and one outdated one in the same week.

In this post, I'll share:

- how we deduplicated 1,842 questions into 63 candidates

- the routing rules that reduced repeat questions

- how we built answer templates with evidence

- the freshness review that fits into one hour per month

- what still needs a human helper

## Start with the questions people actually ask

Our first idea was to write a complete FAQ. That idea died after 45 minutes because completeness would have required guessing at future questions. We needed evidence from the existing chat instead.

I exported 12 weeks of messages from three support channels and removed names, email addresses, and enrollment identifiers. The export contained 14,117 messages, of which 2,204 looked like direct requests for help.

I ran a two-step process. First, a small Python script grouped messages by shared phrases such as "deadline", "certificate", and "connection refused". Then I sampled 30 groups and assigned each one a category by hand.

The manual pass changed the categories for 11 of 30 groups. That result convinced us to keep a person in the loop before deleting or merging anything. Automation narrowed the work, while helpers made the final calls.

After two evenings, the 2,204 messages became 63 FAQ candidates:

- 21 questions about deadlines and certificates

- 17 about installation and version conflicts

- 14 about assignment interpretation

- 11 about payment and access

## Route before you answer

Some questions didn't belong in the FAQ. Payment disputes required account access, assignment submissions needed the grading system, and a few questions were course feedback rather than support requests.

We added three routes:

- self-service answers in a public FAQ

- helper review for assignment and account issues

- direct email for payment and privacy requests

Each route has an owner and a response target. Self-service answers should be updated within five working days, while helper reviews target one working day. Email requests target two working days.

We also added a short routing note to the top of every public answer. It tells readers where to go when their situation differs. That one paragraph reduced misrouted email by roughly 35% over the following six weeks.

## Write answers as templates

The public answers share one structure. Each answer names the situation and states the current policy or fix. It also gives the command or link path and says what to do if that path fails. We kept the tone plain because helpers would copy it under time pressure.

For the timeout error, the answer contained four commands and a link to the course environment page. We also explained that the server closes idle connections after 20 minutes. Once readers understood that detail, repeated explanations in chat dropped sharply.

Every template has an owner, a last-reviewed date, and two test questions. The owner knows which course module the answer depends on. The test questions help a new helper decide whether the answer still applies after a course update.

We stored the templates in Markdown files under `faq/answers/`. That choice made diffs visible and let's us review content changes without opening the site editor.

## Keep freshness review small

Freshness review used to mean "look at everything eventually", which meant never. We now review seven answers each month, so the full set gets reviewed every nine months.

The monthly checklist takes about an hour:

- run both test questions for each assigned answer

- check the linked course version

- update commands and dates

- mark the answer `reviewed` in front matter

In April 2026, that review found 11 stale answers. Six needed new command output, three referenced a removed assignment, and two had incorrect deadline policies. Fixes took another 90 minutes because the Markdown diffs were small and reviewable.

We also log every "this didn't work" reaction. Three reactions in 30 days put an answer into the next review batch. That threshold caught a broken installation command within nine days in May.

## The helper still matters

The FAQ handles repeated facts, while helpers handle judgment. A learner may follow the timeout answer and still have a broken local setup. Another may need an extension because of a medical issue, and no public template should make that decision.

We measured the split during one course week. The public answers handled 38% of 412 support requests without a helper. Helpers answered another 49% directly, and 13% went to email or the grading system.

That number doesn't mean the FAQ replaced people. It removed 156 repeated explanations, which gave helpers more time for unclear cases. Median first response time fell from 9 hours to 4 hours.

## Lessons from the backlog

Deduplication made the workload visible, and routing kept unsuitable questions out of the public answers. Templates with owners and tests made monthly review cheap enough to survive a busy month.

The most useful constraint was the seven-answer monthly batch. It converted a frightening backlog into an ordinary maintenance task. I plan to describe our reaction-log schema in a future post. Subscribe if you want to see how the FAQ changes during the next cohort.
