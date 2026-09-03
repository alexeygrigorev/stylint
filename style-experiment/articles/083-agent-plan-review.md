# Reviewing an Agent Plan Before Letting It Edit Code

In February 2026, I let a coding agent turn a one-page plan into 214 changed lines. The code ran, and three days later I found that it had replaced a public API response without telling me. That diff cost a full afternoon to unwind.

I wrote this piece as a synthetic style exercise, and every project and measurement is invented.

After that week, I stopped accepting "I'm ready to start" as the first agent milestone. I started asking for a plan I could review before any file changed. The plan fits on one screen and forces the agent to name its interfaces, tests, and rollback path.

In this post, I'll share:

- the plan format I now request
- how I review goals and interfaces
- how I test the plan before code exists
- how I set the rollback rule
- what changed over six weeks

## The Plan Format

I now keep each plan as a small Markdown file in the repository. I ask the agent to store it at `plans/2026-02-18-public-api.md` so the next session can read it too.

The template contains six fields:

```text
goal:
in_scope:
out_of_scope:
interfaces_touched:
tests:
rollback:
```

I also set editor rules. The agent may change only files listed under `in_scope`, and it stops to update the plan if it discovers a necessary change outside that list.

My first version used a long paragraph instead of these fields. The agent summarized it back accurately, but I missed a database migration because no line asked for changed files. Flat fields made the omission obvious.

## Review Goal and Interfaces

I read the goal first and look for a user-visible result. A plan saying "Refactor the parser" fails because I can't tell what will improve. A plan saying "Return validation errors with field names" passes because I can judge whether that matches my request.

Then I read the `interfaces_touched` field. The plan should name every HTTP response, database table, event payload, and function signature there. It should also say which of them might change. I want exact names such as `GET /courses/{id}` rather than "the course code".

One plan claimed it would only touch internal helpers. The file list showed `models/course.py`, which another project imported through a convenience function. I asked the agent to add the import path to the plan. It then chose a private helper and avoided the breaking change.

I also ask for a small data example for each changed interface. Seeing one input and one output takes two minutes and catches assumptions about missing values, empty lists, and Unicode names.

## Test the Plan Before Code Exists

A plan review can stop at reading, but I get better results when I ask for tests first. The agent writes failing tests from the plan before implementation. I run them once, confirm the failures describe the goal, and commit them.

I apply three checks to the tests section:

- at least one test covers the main user path
- at least one test covers an empty, missing, or invalid input
- the tests fail for the planned reason before implementation

If the agent writes tests after the implementation, they often encode the code's behavior. That's why I treat the first red test run as a review gate. In one change, the planned error message used `courseId` while our API used `course_id`, and the test exposed it immediately.

For risky changes, I ask for a temporary wrapper rather than a broad rewrite. The old function stays available, and the new implementation runs behind a local flag. That gives me a way to compare outputs on real requests before I delete the old path.

## Set the Rollback Rule

Every plan ends with a rollback section. I reject "revert the commit" unless the agent also says what reverts safely. The answer has to cover database changes, queued jobs, cached responses, and runtime-created files.

A useful rollback has numbered steps, and the order matters for a migration. Stop the job, restore the table, then run the old code path. After that, verify a known response and remove the new code. A vague plan can't tell me which of those steps is reversible.

I now require a backup command even for SQLite files on my laptop. Copying `app.db` takes seconds and makes an experimental migration boring. For services with queues, I ask the agent to name the exact dashboard or log query that shows the queue draining.

This sounds heavy for a side project, but most plans need only two rollback lines. The discipline matters more than the document length.

## Six Weeks of Plans

The review covered my work between February 24 and April 3. Of 17 agent tasks, 11 shipped after one plan revision, and another four needed a second revision because the tests found an interface mismatch. I rejected the remaining pair before code review.

Median review time was 11 minutes, and the largest accepted diff was 165 lines. Across the same kinds of tasks, my post-merge fixes fell from seven in January to two in March. The count is small and personal, so I treat it as directional evidence.

The process also changed the plans themselves. Agents began proposing smaller diffs because the interface and test fields made a broad rewrite hard to justify. One agent split a 40-point feature into two pull requests after it had to name every changed response.

## Lessons Learned

The plan review works because it happens while changing direction is cheap. Reading exact interfaces is less exciting than reading code, but it catches the changes people forget to mention. A failing test gives the plan evidence, and a rollback line gives me permission to run it.

I plan to write next about the task sizes that fit this format. If you want to follow along, subscribe for the next build log.
