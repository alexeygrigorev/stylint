# Turning Course Feedback into Next-Cohort Changes

In May, the fictional `Data Tools Sprint` course collected 87 feedback forms from 103 students. The overall rating was 4.4 out of 5, but 31 comments mentioned the same homework bottleneck. I spent two afternoons turning those comments into a curriculum plan.

I invented the course, cohort, and numbers for a synthetic style exercise. The process connects comments to specific modules, chooses a small number of changes, and records the reason for every rejection.

In this post, I'll share the review process:

- how I prepared the raw comments
- the five labels I used for clustering
- how comments became module-level decisions
- the five changes I chose for the next cohort
- what I rejected and why
- how I'll check whether the changes helped

## Prepare the raw comments

The survey export contained a rating, a cohort week, a role field, and a free-text comment. Forty-one students left comments, so I removed eight comments that named other students before the review. I also replaced four email addresses with generic placeholders in the working copy.

I put the remaining 33 usable comments in `feedback/2026-05/comments.csv`. Each row kept its original ID so I could trace every decision back to a source comment. I also copied the five lowest ratings into a separate file, even though three of them repeated a common complaint.

My first mistake was reading comments in survey order. The order followed submission time, so week-three complaints arrived early and dominated my impression. The rule I took from that mistake: cluster after reading, and make the decision from counts.

## Label comments once

I used five labels and allowed two labels per comment:

- `setup`: local tools, accounts, and installation
- `workload`: time estimates and assignment volume
- `examples`: sample code and walkthroughs
- `review`: feedback delay and grading clarity
- `content`: missing topics or material depth

I labeled in one pass and forced myself to choose the closest label. When a comment mixed two concerns, I added the secondary label. One comment read, "I spent four hours installing PostgreSQL, then the homework still assumed it was running". That received `setup` and `examples`.

The labels produced a clearer distribution than the raw reading had suggested. Seventeen comments mentioned `examples`, 14 mentioned `setup`, and 11 mentioned `workload`. Another 8 mentioned `review`, and 5 mentioned `content`. Since 41 students produced 48 labels, some overlap was expected.

I also checked who wrote each comment. Beginners produced most `setup` comments, while experienced developers produced most `content` comments. That made the issue structural rather than a reason to chase one persona.

## Map clusters to modules

The course had six modules. I created `feedback/2026-05/module-map.md` and connected each cluster to a module owner, even though I was the only owner in this fictional exercise.

The mapping looked like this:

- Module 1: `setup`, environment checks, and starter scripts
- Module 2: `examples`, database walkthrough
- Module 3: `workload`, data-cleaning assignment
- Module 4: `examples`, API pagination exercise
- Module 5: `review`, project checkpoint
- Module 6: `content`, optional scheduling topic

Some clusters pointed at more than one module. I found `setup` in Modules 1 and 3 because the third assignment introduced a container. Rather than adding another environment lecture, I treated the second occurrence as a reuse problem.

The mapping exposed a second mistake. I had assumed the low ratings came from workload, but they mostly came from week one when students couldn't run the starter code. The curriculum change therefore had to remove friction before it added content.

## Choose five changes

The next cohort would last six weeks, and I wanted enough time to test each adjustment, so I set a limit of five changes in `curriculum/next-cohort-plan.md`:

- add a five-minute preflight script before Module 1
- record a 12-minute database setup walkthrough
- raise the Module 3 estimate from 4 to 6 hours
- publish a worked solution for the pagination exercise
- add an optional 20-minute scheduling clinic in Module 6

The preflight script checks Python, Docker, database connectivity, and write access to the course folder. It prints one line per check and exits with a single remediation hint. I expect it to prevent the most common first-night failures.

The recorded walkthrough covers the same setup path as the script. Some students want to see the terminal, while others prefer a checklist. The extra work was about 3 hours, and it reused the existing homework repository.

The workload change was deliberately small. I didn't reduce the assignment because the learning objective depended on cleaning messy data. A more honest estimate gave students room to stop and return the next day.

## Record rejected ideas

Twenty-two comments suggested a live session, but I still rejected it for the next cohort. The cohort had students in four time zones, and the same students rarely attended synchronous events. A recorded walkthrough plus forum office hours covered the need with less scheduling cost.

Seven comments asked for orchestration content. That topic deserves a separate course, and adding it to week six would exceed the project deadline. I added it to a future-course note instead.

Five comments requested a private code review for every homework. The fictional course budget allowed two reviews per student, so I kept the existing rubric and added anonymous exemplars before submission.

I saved every rejected request in `feedback/2026-05/decisions.md`. Each row contains the request, count, and final reason, and that record helps me defend uncomfortable tradeoffs later.

## Check the next cohort

For the next cohort, I'll track five measurements:

- first-night setup completion rate
- median time to first successful homework run
- Module 3 on-time submission rate
- forum questions containing the word "pagination"
- week-six course rating

The baseline cohort had a 78 percent first-night completion rate and 61 percent on-time Module 3 submissions. Those numbers are synthetic, but they give the exercise a way to distinguish luck from improvement.

I'll also ask two direct questions in the week-two survey. One asks whether the preflight script caught an issue. The other asks whether the new time estimate changed how the student scheduled the assignment. Those answers should reveal causes behind the numbers.

The useful discipline was limiting the change set. Feedback can justify a hundred improvements, and a course can absorb only a few in six weeks. The next version should make one frustrating path shorter, then measure whether students actually feel the difference. If I write the follow-up, I'll compare these numbers with the next cohort. Subscribe if you want to see the results.
