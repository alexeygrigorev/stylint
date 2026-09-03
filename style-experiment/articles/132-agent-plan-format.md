# A Plan Format That Makes Agent Work Easier to Review

I reviewed 38 coding-agent changes in February while maintaining a fictional invoice service called `ledgerline`. The service processed about 6,400 invoices per month for 90 small companies. Nine changes touched payment code, and I looked at each plan before the agent edited code.

I wrote this piece as a synthetic style exercise. Every repository, plan, customer, measurement and failure below is fictional.

The best changes weren't the ones with the most detailed prompts. They followed a written plan that said what the agent could change, what evidence it would provide and when it should stop. I could review those changes in minutes instead of reconstructing intent from a large diff.

In this post, I'll share a five-part plan format:

- goal
- constraints
- steps
- evidence
- stop rule

## 1. State the Goal as an Observable Outcome

The goal has to describe a result a reviewer can check. "Improve the invoice parser" is a topic. "Add IBAN validation so malformed payment records fail before persistence" tells me what the finished behavior should look like.

I ask the agent to include the affected user path and the current failure.

Here are two goals from the February work:

- let an administrator retry a failed bank export without reloading the invoice page
- stop duplicate webhook imports when the provider sends the same event twice within 24 hours

Both goals name the actor and the result, but neither says which files to edit. That decision belongs to the next two sections.

A goal that starts with a technology often hides the real outcome. I once accepted "add a Redis queue" as a goal and got a queue with no retry path. The invoice export still failed, so I had to rewrite the task.

## 2. List the Constraints Before Choosing Steps

Constraints keep a plan reviewable. They also make some solutions cheaper to reject before code exists.

For `ledgerline`, the recurring constraints look like this:

- preserve the existing PostgreSQL transaction boundary
- don't add a new service to the payment path
- keep endpoint request and response schemas unchanged
- store all retry state in the database
- finish the task without writing to customer records

The first version of my prompt had only the goal. An agent chose to move export handling into a worker process. That would have solved the timeout and added an operational dependency I didn't want in a small product.

After that run, I wrote the constraints down in the plan. The next plan selected a database-backed `retry_at` column. The diff stayed in `services/exports.py`, `models/export.py` and one Alembic migration.

Constraints should include the review boundary too. For payment work, the agent must propose a diff and stop before I run a migration. That boundary lets me look at destructive changes before anything executes.

## 3. Break the Work Into Ordered Steps

Each step should produce something I can read. I don't ask for time estimates because they rarely help a coding agent. I do ask for touched files and a completion check.

A useful plan for the duplicate webhook task had five steps:

1. add a unique event identifier to the provider payload model
2. write a test with the same event arriving 40 minutes apart
3. add a database constraint for that identifier and provider
4. catch the conflict and return the stored import result
5. run the payment-path tests and print the test command output

These five steps stayed in one area of the service. When a step discovers a second area, the agent should revise the plan instead of expanding the change quietly.

For larger work, I allow three to five steps per request. If the plan reaches nine, I split it into a new request after the first diff passes review.

## 4. Require Evidence for Every Decision

The plan should say what evidence will demonstrate progress. Test names and command output are usually enough, but code summaries tell me what the agent believes rather than what the system does.

For each step, I ask for:

- the test command and its result
- the relevant diff hunk
- the database migration or schema change
- a manual check for a path without automated coverage
- known follow-up work

The webhook change included a test named `test_duplicate_provider_event_returns_original_import`. The evidence block showed the command, the two passing assertions and the SQL constraint. That made it easy to connect the behavior to the schema.

The manual check can be short. In the export-retry case, the agent pasted an administrator session's request and response. It also included the log line showing that the second attempt reused the original file checksum.

Evidence should be ordered by review priority. I read the acceptance test first, then the schema, then the implementation.

## 5. Define the Stop Rule

The stop rule protects the reviewer's attention. It tells the agent when to stop editing and return a result even if the code could be improved.

Our payment-task stop rule has three clauses:

- stop when all listed tests pass
- stop after two failed implementation attempts and report the errors
- stop immediately if a change would touch the balance ledger

The second clause matters more than it looks. On 12 February, an agent tried twice to implement idempotency with a provider event ID that arrived only on some events. It stopped, showed both failures and asked for a decision. I changed the plan to calculate a checksum from amount, timestamp and provider reference.

Without the stop rule, the agent would probably have added a fallback provider, another table and a configuration field. The final solution needed one migration and 62 changed lines.

I also tell the agent not to update documentation in the same change unless the plan says so. Separate documentation edits keep the behavioral diff readable.

## Plan Review in Practice

We now store plan files in `plans/ledgerline`, with a name that includes the date and task. On 26 February I measured 17 completed agent tasks over one week. The eight tasks with full plans averaged 11 minutes of review and 83 changed lines. The nine tasks with goal-only prompts averaged 27 minutes and 219 lines.

That comparison is small and biased because I gave harder free-form tasks to the agent on quieter days. Still, the difference matched what I saw in the diffs: full plans produced fewer exploratory files and clearer acceptance tests.

The remaining weakness is stale context. An agent can reuse an old plan after the code changes behind it. Each plan now includes the current commit and the date of the last schema check. If either is more than two days old, I ask the agent to refresh the relevant section.

I'll publish the `ledgerline` plan template after we use it through one release cycle. If you want to follow along, don't forget to subscribe.
