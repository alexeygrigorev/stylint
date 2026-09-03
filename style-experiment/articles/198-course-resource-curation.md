# Curating Resources Without Sending Students into a Rabbit Hole

I wrote this synthetic style exercise as a how-to guide. The course, dates and numbers are fictional. In 2025 I taught two cohorts of a SQL course, 18 students in each. My first reading list sent half of cohort one into a documentation rabbit hole during week one.

One student read 11 articles about indexes before writing her first query. Another installed two database systems because three resources disagreed about setup. The list I use now fixes that, and building it takes about two hours per course.

In this post, I'll share:

- how we write the learning goal first
- how we order resources around that goal
- how we attach honest time estimates
- how we mark optional depth without hiding it
- the mistakes I still see in student-facing lists
- what changed across the two cohorts

## 1. Write The Learning Goal

We start with one sentence that names a skill and an artifact. A goal like "learn SQL" hides the destination, and every resource then looks relevant.

A goal written this way sets up a test any resource either passes or fails:

```text
Goal: by the end, you can write a report query
that joins two tables and uses one window function.
```

You can borrow the sentence structure from any course syllabus: verb, artifact, scope. We reject any candidate resource that doesn't move a student toward the artifact. We write the rejection next to the resource, so the decision survives the month.

## 2. Order Resources Around The Goal

Order caused the rabbit hole in the first cohort. My first list grouped resources by topic, so students finished joins and wandered into a six-part series on storage engines. So I ordered the new list by dependency instead of by topic.

Each entry now names what must come before it. We write the dependency at the end of the line in plain words, and we cap the core list at six resources.

The working list for the current cohort looks like this:

```text
1. Select and where (40 min) - start here
2. Joins tutorial (50 min) - after resource 1
3. Group by and aggregates (45 min) - after resource 2
4. Window functions walkthrough (60 min) - after resource 3
5. Report query exercise (90 min) - after resource 4
6. Query plans explained (40 min) - extra, after your first slow query
```

Five entries form the spine, and the sixth is optional depth. A student who finishes the five core entries can produce the artifact from the goal sentence, and nothing on the list decorates that path.

## 3. Add Time Estimates

Every line needs a number, because students plan their evenings around the list. We estimate each resource honestly, watch one student work through it, and correct. My first estimate for the window functions walkthrough was 30 minutes. The cohort average was closer to 60.

We hedge every estimate, so a line reads "about 45 minutes" rather than a bare number. We sum the core list at the top of the page. The current total reads "about 4.5 hours across two weeks", and that one sentence does more for completion than any motivational line.

## 4. Mark The Optional Depth

Optional depth is where lists usually turn into rabbit holes, so the label has to be loud. We mark optional resources twice: a tag in the line and a condition that names the moment to open it. "Only if you hit a slow query" works better than "advanced", because it ties the resource to an event the student will recognize.

Depth also needs a budget. The extras on the current list add about 2.5 hours, and we say so right under the core total. One student told us that budget line was the reason she skipped the extras during exam week and came back to them after.

## Common Mistakes

Three mistakes still show up in my lists, and each one cost a student real time:

- resources added because they were interesting, with no line to the goal
- estimates copied from the resource's own landing page, which always promises less
- links left unchecked, so 3 of 19 pointed at deleted pages after a year

Each mistake has a cheap check, and we reread the goal sentence before adding anything. We time one student per new resource, and we click every link at the start of each cohort.

The last check runs as a command:

```bash
uv run link-check resources/cohort-3.md
```

Here link-check is a 30-line script that requests every URL in the list and reports the dead ones. It caught 3 broken links in March 2026, all on pages I had trusted for a year.

## Across The Two Cohorts

Cohort one worked from the old topic-grouped list, and 9 of 18 students finished the core path. Cohort two worked from the list in this guide, and 14 of 18 finished. Students also ask fewer "where do I start" questions, and the two hours of curation per course is the cheapest teaching time I spend.

The method has one honest limit: it assumes you already know the territory well enough to judge resources. Where I'm the beginner, I still send students into rabbit holes, and I now mark those sections as exploration on purpose. I'll write about that exploration mode in a future post. If you want to follow along, don't forget to subscribe.
