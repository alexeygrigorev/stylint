# Choosing Between Starter Code and a Blank Repository

I wrote this piece as a synthetic style exercise, so I invented every cohort number and student story in it. Last autumn I mentored 48 students through a six-week course project, and half of them started from my starter repo. The other half started from a blank repository with only a README and a Python version file.

Both groups built the same expense tracker API with FastAPI and SQLite. Both groups had the same deadlines, the same office hours, and the same grading rubric. By week six the two groups had diverged in ways I wanted to measure.

The starter group shipped faster and asked fewer setup questions. The blank group asked more questions early and rewrote less code late. Neither outcome surprised me alone, and the size of the gap surprised me a lot.

In this post, I'll share:

- what the starter repo gave students in week one
- where starter students paid for it in week four
- what blank-repo students did differently from day one
- how I now pick a starting setup
- what this small sample can't prove

## 1. Starters Win the First Weekend

The starter repo contained a working FastAPI app with login, a SQLite database, and 3 passing tests. Students cloned it, ran one install command, and saw green output within 20 minutes. The median time to first passing test was 34 minutes in the starter group.

The blank group spent its first weekend on setup friction. Median time to first passing test was 4 hours and 10 minutes, spread across Python versions, virtual environments, and editor configs. Support threads in week one ran 61 messages for the blank group against 17 for the starter group.

That early gap felt decisive at the time. Starter students demoed login flows in week two while blank students were still structuring folders.

A student who sees green tests on day one returns on day two, and the starter earned exactly that return. I measured it in commit counts: starter students averaged 9 commits in week one against 4 for the blank group.

## 2. Starters Tax the Second Month

Week four reversed the story in a way the commit graph shows clearly. Starter students began fighting my folder layout, my auth helpers, and my choice of query builder. Twelve of the 24 starter students asked how to remove parts of the starter without breaking the rest.

The starter had made three opinions look like requirements. My auth helper assumed session cookies, my folder layout assumed one app module, and my tests assumed my fixtures. Each assumption cost a starter student an evening once their design diverged from mine.

Blank-repo students hit no such wall because every line was theirs. Their week-four questions were about their own code, and those questions resolved faster with no translation layer. Median time from question to merged fix was 6 hours in the blank group against 14 in the starter group.

The rule I took from week four: every opinion in a starter becomes a support ticket the moment a student outgrows it. Starters lend momentum at interest, and week four collects the debt with evening-sized payments.

## 3. Blank Repos Reward Boring Choices

The blank group converged on simpler designs without any instruction from me. Eighteen of the 24 blank projects used a single app file past week three, and 15 kept SQLite to the end. Their stacks looked plain because each addition had to justify its own existence.

The starter group kept my dependencies whether they needed them or not. All 24 starter projects kept my query builder, and only 6 of them used features beyond plain selects. The rest paid import time, docs reading, and config surface for power they never touched.

Final grades slightly favored the blank group, though the margin was thin. Blank projects averaged 83 points against 79 for starter projects on the same rubric. Code review scores drove the gap: reviewers rated blank code easier to follow by nearly a full point.

For example, one blank project stored receipts as flat files with an index table, and the reviewer called it the clearest design in the cohort. A starter project with the same feature buried it under my service layer, and the reviewer asked for a rewrite. Same feature, same rubric, different starting constraints.

## 4. My Rule for Picking a Start

I now pick the starting setup from the course plan instead of defaulting to the starter. When students must ship a feature on a fixed stack, they get the starter with my opinions stated up front. When students must learn to structure an app, they get the blank repo with a checklist.

The checklist I give blank starters covers the setup traps from week one:

- the exact Python version and install command
- virtual environment creation before any package install
- the test command that must stay green
- the folder layout I recommend with one sentence each
- office hours slots reserved for setup help

That checklist recovered most of the week-one gap in the spring rerun. Blank starters in spring reached first green tests in a median of 95 minutes, down from 250 in autumn. Setup support threads dropped from 61 messages to 23, which my evenings appreciated.

In the README I name the three decisions students will most likely revisit, with the week they usually revisit them. Naming the debt in advance cut week-four removal questions from 12 to 5 in the spring cohort.

## Limits of This Comparison

This comparison rests on 48 students in one course I designed myself. The sample is small, the students knew which group they were in, and I graded half the projects. Any of those facts could tilt the numbers, so I treat the margins as hints rather than proof.

The students also differ from working engineers in an important way. Course projects end after six weeks, so late-stage maintenance pain never arrives. A starter that taxes week four might still win across a year of stable production use.

What survived into my own work is the smaller lesson. I keep a starter for client demos where week-one speed decides everything, and I start blank for tools I'll maintain for years. I treat the starting setup as a bet on which week matters most, and I now place that bet on purpose.

I'll write up the spring rerun numbers in a future post on this blog. If you want to follow along, don't forget to subscribe.
