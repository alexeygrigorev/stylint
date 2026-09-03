# Creating a Shared Agent Profile for a Small Team

I wrote this synthetic style exercise as a how-to guide. The team, dates and measurements are fictional. In March 2026 the four developers at `fieldnote`, a six-person startup, each brought a coding agent into daily work. Within a month our repos held three commit styles and two formats for the same test command.

The agents amplified whatever conventions already existed, and ours were mostly habit. A review comment fixed one repo while the other three drifted for another sprint. We settled on the setup in April, and copying it into a new team takes about half a day.

In this post, I'll share:

- how to agree on the conventions to encode
- how to add the shared commands
- how to write the review rules
- how to document the exceptions
- which caveats to expect in the first weeks
- what changed after two months

## 1. Agree On The Conventions

We booked one 45-minute meeting and wrote the conventions down as a single page.

We put only rules on the page that an agent can check:

- how branch names are formed
- the commit message format
- the one test command that must pass
- the location of the changelog

Rules nobody can verify mechanically stayed off the page, including the vague request to keep functions small. We kept the page to five rules at first, because nobody finishes reading a longer one. I wrote a one-sentence reason under each rule, because agents follow reasons better than bare prohibitions. Conventional Commits made the list with the reason that release notes are generated from the prefixes. You can find the page at `profile/rules/style.md` in a repo we named `team-agent-profile`.

## 2. Add The Shared Commands

Next we moved the commands every agent should know into the same repo.

The layout stayed flat on purpose:

```text
team-agent-profile/
  rules/style.md
  rules/review.md
  commands/run-tests.md
  commands/check-pr.md
  exceptions.md
  settings.json
```

`run-tests.md`, a command file that runs the test suite and pastes the summary line, replaced three per-developer variants in one afternoon. `check-pr.md` reviews a diff against the rules folder before any human looks at it. The commands are short markdown files, and each one names the tool, the arguments and the output to paste back.

Each developer clones the repo and points the agent at the folder:

```bash
git clone git@github.com:fieldnote/team-agent-profile.git ~/tools/team-agent-profile
```

One line in `settings.json` connects Claude Code to that folder, and the whole step took about 10 minutes per person.

## 3. Write The Review Rules

The review rules tell the agent what must be true before a task counts as done.

We keep them in `rules/review.md` as plain imperative lines:

```text
Before you mark a task done:
- run the test command and paste the summary line
- add a CHANGELOG.md entry under Unreleased
- keep the diff under 400 lines and split larger changes
- name the rule you followed when a reviewer asked for a change
```

The 400-line limit came from a February change that touched 1,100 lines across 19 files and took two days to review. After the limit arrived in April, the average reviewed diff dropped to about 180 lines. The last rule grew out of a May dispute, and writing the reason into the review note ended arguments faster than any meeting. We review the rules file with the same `check-pr.md` command, which kept the rules honest.

## 4. Document The Exceptions

Every rule needs a documented way to bend. `exceptions.md` lists the cases where a rule gives way, and each case names an owner. A database migration may exceed the diff limit when the migration file and its rollback travel in separate commits. A hotfix may skip the changelog for one day, and the entry goes in the next morning. A third exception covers generated files, and the agent may commit them without a changelog entry when the generator owns the folder.

Without this file, agents either enforced the rules into absurdity or ignored them after one pushback. The file made the exceptions reviewable like any other change.

## Caveats From The First Weeks

The profile needs an owner, or it rots like any shared document. I own ours, and I review proposals to it every Friday in a 15-minute slot.

The first weeks added a few more lessons:

- rules an agent can't check will erode, so turn them into commands or drop them
- expect about two weeks of friction while developers unlearn their private variants

We also tag the repo with versions, so an agent can use a known-good tagged profile during a release week. The tag for the June release was `v1.4`, and we reused it unchanged for the July release as well. One developer kept a private profile that overrode the shared one, and we removed the override after three failed reviews in one week.

## Results After Two Months

Between January and March we averaged 11 correction rounds per 20 agent tasks.

Between June and August the same count was 4, on a similar task mix. Two developers still disagree about test naming, and that argument stays human.

The Friday review keeps the rule count honest at 9 rules and 12 commands. The profile repo had 340 commits by August, which is more than some of the product repos.

I'll write about how we choose what gets tagged for a release week in a future post. If you want to follow along, don't forget to subscribe.
