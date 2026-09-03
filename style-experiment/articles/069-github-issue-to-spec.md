# Turning a GitHub Issue into a Testable Specification

I wrote this synthetic style exercise as a how-to guide. The project, dates and measurements are fictional. In February an agent spent three hours implementing a GitHub issue titled "improve exports", and the result matched nobody's expectation.

The issue held two sentences and zero acceptance criteria. The agent built a new CSV format, the requester had wanted faster Excel downloads, and I reviewed a diff that solved the wrong problem well.

In this post, I'll share:

- how I rewrite the issue as a user outcome
- how I collect boundary cases before coding
- how I write acceptance checks the agent can run
- how I keep the spec next to the code
- what specs changed in my rework rate

## Vague Issues And Their Cost

The February issue asked for better exports from a reporting dashboard. It named no user, no format and no deadline, and three people read three different requests into it.

The agent chose the most literal reading and produced a polished CSV exporter. The requester replied within an hour that Excel files took 40 seconds to generate, and speed was the actual complaint.

The rule I took from February is simple. I convert every issue above a half-hour estimate into a one-page spec before any agent touches it.

## 1. Rewrite The Issue As A User Outcome

I open the spec with one paragraph that names the user, the situation and the observable result. For the export issue I wrote that a finance reviewer downloads the monthly report as Excel in under ten seconds.

That sentence forced three decisions the issue had dodged. It named the user, fixed the format and set a number on speed, and each decision removed a branch the agent might have wandered down.

I keep the outcome paragraph under 40 words, and I read it aloud before continuing. If it mentions two users or two results, I split the issue before writing another line.

## 2. Collect Boundary Cases Before Coding

Boundary cases are the inputs where reasonable people disagree, and I list them before the agent starts. For exports those cases included empty reports, 100,000-row tables and non-Latin customer names.

The February spec listed five boundary cases:

- an empty report still downloads as a valid file
- a 100,000-row report finishes within the ten-second budget
- customer names in Cyrillic and CJK scripts render correctly
- a reviewer with viewer-only permissions sees no export button
- a second click during generation never starts a duplicate job

I gathered those cases in 25 minutes by asking the requester three targeted questions. Each answer became one or two cases, and the requester confirmed the full list the same day.

## 3. Write Acceptance Checks The Agent Can Run

Each boundary case becomes one automated check with a command attached. I write the checks as `pytest` tests against fixtures, and the agent runs them before declaring the work done.

The export spec pointed at an existing test file:

```bash
pytest app/tests/test_exports.py -q
```

That file held 14 tests after I added the five boundary cases. Nine covered the previous behavior, and five encoded the new expectations from the spec.

I require the full file green before review, and I state that requirement in the spec. The agent ran the suite four times during the March reimplementation, and each red run caught a real deviation.

## 4. Keep The Spec Next To The Code

Specs rot when they live far from the code they describe. I store each spec at `docs/specs/` under the issue number, and the filename never changes after merge.

The export spec lives at this path:

```text
docs/specs/1042-export-speed.md
```

That file holds the outcome paragraph, the boundary cases and the acceptance commands. When the behavior changes deliberately, the same pull request updates the spec and the tests together.

I link the spec from the issue with one comment after merging. The issue thread keeps the discussion, and the spec file keeps the decisions, so neither fills with the other's content.

## 5. Review Against The Spec

Review compares three things in a fixed order. I read the spec outcome first, run the acceptance checks second, and read the diff last.

My review routine fits on four lines:

- the outcome paragraph still describes the merged behavior
- every acceptance check passes on my machine
- the diff touches only the files the spec names
- boundary behavior matches the spec wording exactly

That order matters because diffs seduce reviewers into line-level reading. When I start from the outcome, I judge the work against the request instead of admiring the implementation.

The March reimplementation passed all four lines on the first review. The reviewer spent 15 minutes against three hours for the February version, and the requester confirmed the fix the same afternoon.

## Rework Fell By Two Thirds

Since February I have written 23 specs for agent-implemented issues. Seventeen passed review on the first attempt, five needed one correction round, and one exposed a disagreement the spec had missed.

Rework rate fell from roughly two rounds per issue to under half a round. Spec writing takes 30 to 45 minutes, and each avoided rework round saves about two hours.

The specs also settled scope arguments before coding started. Four issues split into smaller pieces during spec writing, and each piece shipped faster than the original bundle would have.

I'll cover the spec template file in detail in a future post. If you want to follow along, don't forget to subscribe.
