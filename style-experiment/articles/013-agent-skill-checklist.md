# The Checklist I Use Before Turning a Workflow into a Skill

I wrote this article as a synthetic style exercise with a fictional team, repository, dates, and measurements. The checklist reflects how I decide when an agent workflow is ready to become a skill.

In March 2026, our five-person operations team had 23 documented agent prompts. Three were brilliant, nine worked on Tuesdays, and the rest depended on context that lived inside one person's chat history. I reviewed every prompt and turned four workflows into skills, a structured set of instructions and supporting files that an agent can load consistently.

In this post, I'll share:

- the repeat-use threshold I apply before writing a skill

- why I demand stable inputs and examples

- how I test whether the output is verifiable

- the two failures that stopped a promotion

- what changed after four workflows became skills

## Repetition proves the workflow

The obvious criterion was frequency, and I got it wrong at first. I promoted two prompts after five uses, and both had too little history. One was a release-notes helper for `ops-tools`, while the other was an incident summary template for our on-call rotation.

Both had too little history. On the sixth use, a prompt met an unusual release with two database migrations, and the output omitted the rollback steps. The incident prompt collapsed when a ticket contained three unrelated alerts.

So I changed the threshold. A workflow needs ten real uses across at least three people before I turn it into a skill. It also needs to survive one unusual input without a person rewriting the instruction in chat.

The release-notes workflow now has 17 logged uses, while the incident summary has 31. Both meet the bar, but I still treat each skill as a draft until its output survives a review.

## Stable inputs come first

Frequency proves demand, but it says nothing about whether the task has a stable input structure. I review the inputs next. A skill without predictable inputs turns every run into a new prompt.

For each candidate, I collect the last ten runs in a spreadsheet. I record the requester, source files, missing context, and corrections made by the reviewer. The corrections matter most because they expose assumptions the prompt never stated.

The release-notes workflow looked good. Every run began with a Git tag range and ended with a markdown file in `release-notes/`. The only variation was whether the requester wanted customer-facing language.

The incident workflow looked good until I read the corrections. Three people supplied timelines in different formats. One used a ticket ID as the timestamp, another pasted chat excerpts without authors, and a third entered times in local Berlin time. Those differences made review slow.

I now require five input entries before promotion:

```text
required inputs:
- source location
- schema or example
- reviewer role
- forbidden actions
- expected output path
```

If a candidate can't satisfy those five entries, it stays as a prompt. We can still improve the process manually. Promotion to a skill would freeze the ambiguity into the tool.

## The output has to be verifiable

The third test asks whether a reviewer can check success without guessing. I don't demand certainty, but I need enough evidence to accept or reject a run.

For release notes, the test is concrete. The output has to mention every conventional commit between two tags, classify each change, and exclude commits marked `chore(internal)`. A 60-line Python script compares the note against `git log` and prints missing commit subjects.

That script reduced review time from 25 minutes to about six. It also caught an interesting miss: the prompt had skipped a revert commit because its subject looked like a feature. We added a rule for `Revert` and a test case.

For the incident summary, verification is softer. A reviewer checks timeline order, owners, customer impact, and follow-up actions. We still reduced disagreements by requiring each action to name one owner and one due date.

## The failures that stayed prompts

Two workflows failed the review. The first tried to assign incoming support tickets to an engineer. It reached 72% agreement with humans over 43 tickets, which looked acceptable until I grouped the errors.

Nineteen of the twenty disagreements involved tickets with mixed billing and technical problems. The model chose one category, while humans wrote two actions. The issue was the mixed-ticket structure, and no prompt polish would repair it.

The second candidate summarized customer interviews. It worked beautifully with recordings under 20 minutes and invented plausible themes on a 52-minute recording. The failure appeared only twice, but both transcripts influenced a roadmap decision.

We kept both as ordinary prompts with tighter review. Until we split mixed tickets and force interview summaries to cite timestamped evidence, they don't belong in a reusable skill.

## After promotion

Four skills now live in `.agent/skills/`, and each has a `SKILL.md` file plus examples. Onboarding a new agent takes about 15 minutes instead of a 45-minute chat-history archaeology session.

The team also argues less about wording. When output disappoints us, we edit the skill and rerun the evaluation set. The conversation moves from "the agent misunderstood me" to "the instructions missed this case".

The maintenance cost is real. We spent another 11 hours during the first month clarifying examples and removing one unreliable web tool. I would rather spend that time in a file under review than in an unrepeatable prompt.

Version control made that cost manageable. Each skill file sits in the operations repository, and every edit appears in a pull request. A helper can propose a wording change without asking a person to paste the current prompt into chat.

## Lessons from the checklist

A skill is a reviewed instruction file. Repetition shows that the work matters, stable inputs make it teachable, and verifiable output makes review possible.

Two of four candidates failed, and that failure rate convinced me to keep the checklist. The tests cost about three hours per candidate. The alternative was shipping another instruction that worked only inside one person's memory.

I plan to describe the release-note evaluation script in a future post. Subscribe if you want the next update on how these skills hold up.
