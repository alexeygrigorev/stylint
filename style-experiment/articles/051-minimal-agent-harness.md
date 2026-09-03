# Building a Minimal Harness Around a Coding Agent

I wrote this build log as a synthetic style exercise, and I invented every project detail. In the fictional project, I used a coding agent to migrate 38 small Flask routes from an old internal service to FastAPI.

The first sessions went badly. The agent edited files on three unrelated tickets and started a development server that blocked my terminal. It also deleted a migration I had forgotten to commit. None of that exposed a weakness in the model.

It exposed the absence of a harness. In this project, I used that word for the code and permissions around the agent.

It also covered the logs and checks.

In this post, I'll share:

- the first harness I assembled from shell commands
- why I replaced ad hoc checks with a run manifest
- how the input queue and result folder work
- the measured effect on review time and retries
- what still needs a human

## First Version

I started with a directory named `agent-jobs` and a text file for each task. Each file had the ticket number, the files the agent could change, and the acceptance checks. I opened one terminal for the agent and another for `git status`.

That arrangement worked for an initial task. On the second task, I lost track of which agent had created a temporary test database. I also forgot to revoke write access to a config file before a third run.

My conclusion after that week was blunt: if a boundary lives only in my memory, the agent doesn't have a boundary.

I fixed that with a wrapper script. It copied the repository into a temporary directory and exported a read-only token.

It then ran the same tests after every attempt:

```bash
uv run pytest -q tests/routes
git diff --check
```

The tests covered route status codes and JSON fields. `git diff --check` caught whitespace damage before review, so every run had the same minimum exit condition.

## Run Manifest

The shell history couldn't answer later questions. I couldn't tell whether a successful run had used the same prompt as a failed run. I also couldn't tell whether a test had passed before or after the agent changed a schema.

So I replaced the informal notes with a `manifest.json` file generated at the start of every run.

Each manifest recorded the ticket ID, model endpoint, and prompt file. It also recorded allowed paths and the retry limit. The wrapper refused to start when a manifest was incomplete.

It also wrote a `result.json` file at the end. That file stored the status and elapsed seconds, and it recorded the test output as well.

It recorded the test output, changed files, and a short error class as well.

```json
{
  "ticket": "ROUTES-118",
  "allowed_paths": ["src/api/orders.py", "tests/test_orders.py"],
  "timeout_seconds": 900,
  "max_retries": 2
}
```

The file was deliberately boring. Its value came from being machine-readable and immutable after the run. I stopped pasting prompts into chat history and started treating each job as something I could compare with the previous job.

## Input Queue

Once the wrapper was stable, I put 38 route tickets into a queue. A small Python program read tickets from `queue/`, copied each one into `active/`, and invoked the wrapper. On completion, it moved the manifest and result into `runs/2026-08-14/`. Nothing else wrote to the queue.

I gave the queue three states. I marked a ticket `ready` when it had acceptance checks and no unfinished dependency. I marked it `blocked` when the result file named a missing prerequisite.

The final `done` state recorded a passing run. I initially tried to model more complex dependencies, but the migration only needed these three.

I also capped concurrent jobs at two. The repository was small enough that eight parallel agents would have competed over shared test fixtures. Two workers finished 24 tickets on the first evening, while I reviewed completed diffs in another window.

## Review Results

The raw success count was 29 of 38 tickets. Inspection made that number look weaker because four successful diffs had unnecessary changes. They replaced a shared serializer with a local function, so I rejected them and re-ran the jobs.

The review time also improved. I used to spend about 22 minutes on each accepted route change before the harness existed.

With the manifest and restricted diff beside each change, my average dropped to around 13 minutes.

Total wall-clock time was about 31 hours across nine days, including my reviews.

The most useful output was the error summary. Seven runs ended with a missing fixture, five with a timeout, and four with an unchanged ticket. That distribution told me where to improve the prompt. I added one fixture path and a hard instruction to stop after the ticket's acceptance checks.

## Human Review Boundaries

The harness made common failures visible, but it didn't judge design. It couldn't tell whether the new API belonged beside the old service or in a separate deployment. I made that decision after reading the first five accepted diffs.

Security review also stayed manual. The permission list prevented the agent from editing deployment files, yet I still looked for secrets in every diff. For this project, that took about 90 seconds per change because the paths and test suite were narrow.

The remaining nine tickets involved shared authentication behavior. The agent could make individual tests pass, but its solutions diverged. I grouped those tickets into one human-written spec, then let it implement the spec against 11 test cases.

## Lessons From the Migration

I used an input queue, a run manifest, a result record, and automated checks in the minimal harness. I didn't need an orchestration framework for a 38-ticket migration. I needed reproducible inputs and evidence I could review quickly.

I would start with this structure again. A project with several concurrent agents, heterogeneous services, or deployments would need more work in the wrapper.

I reduced the rule to three instructions. Give the agent a narrow job, write down what success means, and keep the evidence after the run.

I plan to describe the permission model in more detail in a future article. Subscribe if you want to follow along.
