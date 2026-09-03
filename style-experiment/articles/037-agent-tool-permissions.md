# A Practical Way to Scope Tool Permissions for Agents

This synthetic style exercise uses a fictional project and invented details.

I gave a coding agent write access to an entire repository last year. The task was small, the agent was capable, and the diff still touched 38 files. Nothing dangerous happened, but I spent 90 minutes deciding which changes belonged to the feature.

That experience changed how I configure tools. An agent should start with read-only access, while write access should be explicit, narrow, and tied to a review path.

This exercise uses invented repository and task sizes.

In this post, I'll share:

- the permission levels I use for common tools
- how I define allowed and forbidden paths
- how I test the permission setup
- how the rules work in a small team
- what still requires manual review

## Permission Levels

I use three levels for every tool:

1. read-only
2. scoped write
3. privileged write

Read-only access lets the agent search code, read logs, and query a database view. I allow scoped write only in named directories, a named branch, or one configuration file. I reserve privileged write for deploy, database migration, credential rotation, or a CI definition change.

The mapping is intentionally boring. A test runner can execute code, but it can't publish a package. A documentation generator can edit `docs/`, but it can't edit application code. A database client can read a replica, but it can't alter production tables.

This mapping keeps the blast radius small when a prompt is misunderstood.

I write those rules next to the task instead of hiding them in a global config. The agent sees them, and a reviewer can challenge them before work starts.

## Define Paths Explicitly

For each task, I list allowed paths and forbidden paths in the prompt:

```text
Allowed:
  src/payments/refund_service.py
  tests/payments/test_refund_service.py

Forbidden:
  infra/
  .github/workflows/
  src/payments/legacy_client.py
```

The forbidden list matters more than the allowed list. It encodes the parts of the system that are either risky or under someone else's ownership. `legacy_client.py` was scheduled for deletion, so changes there would have created merge conflicts.

I also state the branch policy. In one fictional service, the agent could push to `agent/refund-flow`, but it couldn't push to `main`. If the task needed a database migration, I added a separate approval step and required the migration file to remain unapplied until I reviewed it.

## Test the Setup

I test permissions with two kinds of cases:

- a canary task that asks the agent to perform an action that should fail
- a normal task followed by a path audit

The canary task asks the agent to edit a forbidden file. I expect a refusal, and I log the reason it gives.

Then I run a normal task and compare the final diff with the allowed paths:

```bash
git diff --name-only main...agent/refund-flow > /tmp/changed-paths.txt
```

The command lists changed paths, so I can look at them with a script or a human review. In one test, the agent modified `src/payments/api.py` even though the task only mentioned the service. The change was reasonable, but it violated the scope, so I split it into a second task.

I repeat the audit after every revision. Agents often make the correct fix in the correct file and then add a small cleanup in a forbidden path.

## Rules in a Small Team

In a small team, the same rules need names. Every scoped write task names an owner, a branch, and a review deadline. Every privileged write requires a second person to approve the run before it starts.

We keep a shared matrix for the common tools:

- search tools: read-only for everyone
- documentation writers: write to `docs/` and `changelog/`
- service coders: write to the service directory and its tests
- deployment tools: privileged, require two approvals

The matrix doesn't replace judgment. It makes the default visible so people can request an exception without inventing a new policy.

We also log tool calls in the agent harness. The log includes tool name, arguments, return status, and duration. It also shows touched paths, so a two-week project becomes easy to audit.

## Manual Review Still Matters

I keep three areas as human decisions:

- database migrations, especially rollback behavior
- new dependencies, for license, maintenance activity, and supply-chain risk
- changes to authentication, authorization, or billing logic

These scope rules reduce accidents, but they don't prove correctness. A patch can stay inside `refund_service.py` and still calculate a refund badly. Tests, code review, and staging checks remain essential.

My principle is simple: start with read-only access and expand only with a named purpose. Make every expansion visible, because agents don't need unlimited access to do useful work.

I'll write more about permission audits in a future article. If you want to follow along, don't forget to subscribe.
