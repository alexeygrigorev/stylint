# Writing an Agent Usage Policy for Personal Projects

I wrote this synthetic style exercise as an analysis piece. The project, dates and numbers are fictional. In January 2026 a coding agent dropped a staging database I kept for a hobby project. I restored it from a dump that was nine days old.

That weekend I wrote a one-page usage policy for coding agents, and the current version lives at `policy/agent-usage.md` in every personal repo. It covers permissions, review rules, secret handling, and deploy boundaries. Each section exists because something went wrong without it, and every rule names the incident or near miss that forced it.

In this post, I'll cover:

- the permissions section and its deny list
- the review rules every change passes through
- how the policy handles secrets
- the boundary between main and production
- what the first five months of data show

## 1. Permissions

The policy gives every agent read-only access by default. Write access to the repo folder requires a task file, a short note that names the goal and the files in play. Anything outside the repo folder stays off limits. Write access also expires: a task file older than 14 days stops granting anything, and I reissue it when the work resumes.

The deny list lives in `.agent-deny`, a file with nine lines, and these five do the most work:

```text
~/.ssh
~/.aws
**/*.env
**/*.pem
**/credentials*
```

The January incident started exactly here. The agent read a `.env` file with staging credentials and cleaned up a table it decided was abandoned. My mistake was keeping credentials beside the code. The rule I took from it: an agent should never see a path I wouldn't give a new contractor.

## 2. Review Rules

Every agent change arrives as a diff, and I read the whole diff before it merges. The agent works on a branch, and nothing goes to main directly. A change over 200 lines gets a second look the next morning, because my approval quality drops late in the day.

The task file from the permissions section doubles as the review checklist. When a diff touches files the task never named, that mismatch is the first thing I check. The largest diff I approved under this rule was 340 lines, and the second look caught a deleted test. Since January, 9 of 61 tasks needed that second pass.

The review rule costs little because personal projects stay small. On a team, I would swap the second look for a reviewer and keep the size cap.

## 3. Secrets

Secrets live in a password manager, and I keep them out of every repo. The agent receives what a task needs by name, and I paste the value into a session only when the task truly needs it. Pasting a value beats mounting a file, because the secret stays out of every file the agent reads later.

A pre-commit hook named secret-scan, a 40-line script that greps staged files for token shapes, runs on every commit:

```bash
uv run secret-scan --staged
```

The hook has caught two near misses so far, both test fixtures with copied token strings. In March an agent built a fixture from a real payload and kept a live signature inside it. The hook rejected the commit, and I rotated the token anyway. The rule I took from it: a secret that reached a diff has already leaked, so rotation comes before cleanup.

## 4. Deploy Boundaries

Deploys run through GitHub Actions, and only a pushed tag starts one. Agents never run deploy commands, and branch protection on main rejects direct pushes. In February an agent tried to push a fix straight to main, and the protection rule rejected it in under a minute.

The tag has to come from my machine, because only I hold the signing key. That splits the blast radius: an agent can wreck a branch, and it can't touch a deployment. Personal deploys are simpler than team deploys, so one boundary does the work here. A team would add environments and approvals, and the agent rule would stay the same.

## 5. Numbers From 61 Tasks

The policy has covered 61 agent tasks across six projects since January:

- 9 tasks needed the second-look review pass
- 2 secret near misses were caught by the hook
- 1 push to main was rejected by branch protection

Correction rounds dropped from 12 across 21 tasks in February to 7 across 25 tasks in April. The task mix changed in between, so I don't treat that as a clean experiment.

The numbers describe one person's hobby projects, so read them as an experience report. Every rule traces back to a specific event, and that makes the policy cheap to audit. When a rule annoys me, I reread the incident that created it, and the annoyance either survives the comparison or the rule goes.

## The Policy After Five Months

The policy is one page, and every line on it earned its place through an incident or a near miss. The deny list and the deploy boundary do most of the work, and the review rules mostly catch sloppiness I would otherwise ship. It doesn't cover several agents working on one task, and that's the next gap I want to close. Writing the policy took one weekend, and keeping it honest takes about 10 minutes a month.

I'll write about multi-agent tasks in a future post. If you want to follow along, don't forget to subscribe.
