# Preparing a Student Project Show Without Overclaiming

This synthetic style exercise follows a fictional practitioner. The course, projects, and measurements are fictional and illustrate a student demo day. Last June I supervised 16 student projects in a six-week ML course with 84 enrolled learners.

The demos were strong and the claims ran ahead of the evidence. One team reported 94 percent accuracy without naming the test split. Another team showed a polished UI backed by hard-coded responses. I liked their energy and I worried about publishing those claims.

In this post, I'll share:

- the demo day pressures I saw
- the evidence requests that worked
- the review pass I ran before publishing
- how I published limits alongside results
- lessons I'll take into the next cohort

## Demo Day Pressures

Students demoed after six weeks of evening work alongside jobs and exams. Each team had eight minutes on stage plus four minutes for questions. The audience included peers, two teaching assistants, and three guest engineers from local firms.

The format rewarded confidence over caution. Teams saw prior cohorts get praise for big numbers and smooth recordings. Three teams told me they felt they needed a breakthrough to earn attention.

I reviewed the slide decks the night before the show. Nine decks reported a metric without a dataset size. Five decks showed a live demo without noting the fallback path. Two decks listed a model name I knew they hadn't called during the build.

The rule I took from that evening: students optimize for the room they see, so I needed to change what the room rewarded. I announced that the published recap would include methods, limits, and next steps for every team.

## Evidence Requests That Worked

I sent a one-page evidence form the morning after demos. I asked for the dataset size, the evaluation split, and the command that produced the headline number. I also asked for a 60-second screen recording with no edits.

The form used plain fields in a shared document:

```text
team_name
dataset_size
eval_split
headline_metric
command
demo_video_link
known_limits
```

Fourteen of 16 teams returned the form within four days. Two teams needed a reminder and a 20-minute call to locate their evaluation logs. One team discovered their accuracy came from 42 validation rows, which changed how they described the result.

I kept the requests small enough to finish in one evening. Teams pasted commands from their history and linked existing recordings. The form took a median of 35 minutes, according to four teams that timed the work.

The evidence changed the conversation from ranking to review. Instead of debating which demo felt stronger, we discussed which claim had support. That shift lowered tension and raised the quality of questions.

## Review Pass Before Publishing

I reviewed each submission with a teaching assistant over three evenings. We ran the listed command when the repository included data and dependencies. We watched each recording at normal speed and noted any cut between action and result.

We grouped findings into three buckets:

- confirmed claims with runnable evidence
- plausible claims with missing logs
- claims that needed a rewrite before publishing

Six teams ended up in the first bucket with no changes. Seven teams needed one clarification, usually the split size or the random seed. Three teams rewrote their headline after we found leakage, a tiny test set, or a manual step.

One team had trained on the test split by accident. They were embarrassed and offered to withdraw from the recap. I told them the mistake was common and the fix was instructive, so we published their corrected score with a note about the error.

That review took about 11 hours across both reviewers. It felt slow during the week, but it prevented publishing three numbers I couldn't defend. The teams said the comments read like code review rather than grading.

## Publishing Limits Alongside Results

The published recap gave each team one section with the same parts:

- the team name
- the problem statement
- the evidence
- the limits

Every section linked the repository and the demo recording.

A typical entry read like this in my draft file:

```text
Team Atlas, a course search helper, reported 71 percent recall at five
on 380 labeled questions, with code and video linked, and it still
fails on multilingual queries and long PDFs.
```

Readers responded most to the limits section. I asked each team for two concrete limits and one next step. Hiring managers later told me those lines helped them assess junior work fairly.

The recap covered all 16 teams and ran about 2,400 words. It took six hours to edit because I standardized verbs and checked every metric against the forms. Page views reached 1,900 in the first month, which doubled the prior cohort recap.

Two teams asked to update their sections after fixing bugs. I added dated notes rather than rewriting history. That choice kept the record honest and showed progress without hiding the earlier state.

## Lessons For The Next Cohort

The show worked because evidence became part of the grade. Teams earned points for runnable commands, labeled splits, and honest limits. The final demo counted for 30 percent, while the evidence form counted for 20 percent.

I'll keep the form shorter next time and send it before demo day. Teams should collect commands and recordings during the build, not after the applause. Early collection will cut the reminder round I ran this year.

I kept the deeper lesson well beyond logistics. Students write stronger claims when reviewers ask for artifacts instead of adjectives. A command, a split, and a video teach more than a score alone.

I'll run the same review pass in the autumn cohort and publish the template alongside the recap. If you want to follow along, don't forget to subscribe.
