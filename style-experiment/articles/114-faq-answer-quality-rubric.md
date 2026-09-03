# Defining a Quality Rubric for FAQ Answers

I wrote this synthetic style exercise as a how-to guide. The product, numbers and review process are fictional.

In January I reviewed 120 answers for the FAQ system in a fictional library-software product called `shelfline`. The system answers questions from 38 staff members about cataloging, patron accounts and interlibrary loans. A previous model rewrite had improved the tone, but 31 answers still buried the action under caveats.

The problem was that "good answer" meant something different to every reviewer. One person wanted completeness, another wanted brevity, and a third cared most about current policy. We needed one review sheet that could turn those preferences into consistent decisions.

In this post, I'll share:

- how I defined the five review dimensions
- how I worded each score level
- how three reviewers calibrated the rubric
- how to apply the scores to an existing FAQ
- what changed in the answer workflow

## 1. Define The Five Dimensions

We started with the questions staff actually submitted. I sampled 60 threads from December and marked every complaint that appeared more than once. The sample covered account renewals, damaged books, loan periods and holds.

Five dimensions explained most of the disagreements: correct, current, complete, concise and kind. The adjectives came from the reviewers, and each one needed a definition tied to observable details.

The definitions are deliberately narrow:

- correct: the answer follows the library's written policy and the catalog's actual behavior
- current: the answer uses the policy version in force on the answer date
- complete: it names the action, eligibility, deadline and required fields
- concise: a staff member can find the action without reading every caveat
- kind: it respects the reader and avoids blame or unnecessary apology

We treat these dimensions separately because an answer can pass one and fail another. A courteous answer can still cite an expired fee. A technically correct answer can hide the patron's next step.

## 2. Write Score Levels People Can Apply

A score of 1 to 5 without definitions invites disagreement. I wrote one sentence per level for each dimension and tied every sentence to something the reviewer can see in the answer.

The concise scale looked like this:

```text
5: The first sentence states the action, and no unrelated caveat precedes it.
4: The action appears early, with one necessary condition in the same paragraph.
3: The action is present but follows two or more background sentences.
2: The action is mixed into policy discussion and requires rereading.
1: The reader must infer the action from an example.
```

We used the same method for the other four dimensions. "Correct" uses the canonical policy page and the current software build. "Complete" asks whether a staff member could act without opening another document.

Because "Kind" caused the longest discussion, we avoided making it a tone score. An answer qualifies when it addresses the patron's situation, states the reason for a denial and doesn't imply carelessness.

## 3. Calibrate With Three Reviewers

On 29 January, three reviewers scored the same 20 answers independently. They had the rubric, the policy pages, the software version and no information about who wrote each answer.

The first pass gave identical scores on 54% of the 100 dimension ratings. Four dimensions explained the disagreements. Reviewers differed on whether a deadline was mandatory. They also differed on whether a linked policy was sufficient and whether two apology sentences counted as excess.

We resolved the disagreements in one 45-minute meeting. Each revision added an example or removed a judgment call. For example, "complete enough" became "the reviewer can act without opening another page".

The second pass on 31 January matched on 82% of ratings. The remaining disagreement was in the "kind" dimension, so we added two examples of acceptable and unacceptable phrasing. We didn't chase perfect agreement because 80% or higher is enough for triage.

## 4. Apply The Rubric To Existing Answers

We reviewed the remaining 100 answers in two rounds. Each reviewer took 50 answers and scored all five dimensions on a spreadsheet row containing the answer ID, review date and policy link.

The process uses four passes:

- score every dimension without editing the answer
- mark the lowest score as the answer's triage level
- collect the exact policy or UI evidence for scores below 4
- rewrite answers only after a batch of 20 is scored

The spreadsheet made the workload visible, and scores below 4 appeared in 43 answers. Completeness caused 24 of those failures, and conciseness caused 11. Currency caused 5, correctness caused 2 and kindness caused 1.

That distribution changed our plan. Grammar and tone were minor issues, and the main defect was an answer structure that gave background before action.

## 5. Change The Answer Workflow

The rubric now enters before publication. A writer drafts an answer, links the policy version and software build, then runs a short self-check before sending it to review.

The self-check lives in the draft template:

```text
1. Name the action in the first sentence.
2. List eligibility, deadline and required fields.
3. Link the policy version and the relevant screen.
4. Remove background sentences that do not change the action.
5. Read the denial case and confirm the reason is stated.
```

A second reviewer scores only three dimensions for routine updates: correct, current and concise. A full five-dimension review runs after a policy release or a software upgrade. This keeps routine fixes at about 6 minutes per answer instead of 15.

The workflow has one accepted cost. Some answers now begin abruptly because the action arrives in sentence one. Writers can add context after the action, and reviewers can flag an answer that feels abrupt without reducing its conciseness score.

## Lessons From The Review

The rubric works because each adjective became a reviewable condition. Staff no longer argue about whether an answer feels good. They can cite the missing deadline, the expired fee or the sentence that hides the action.

Calibration matters more than the number of levels. Our first pass showed that sensible people read the same adjectives differently. Examples and evidence links closed most of that gap.

The scores still don't measure whether the underlying policy is understandable. That's a separate review of the policy pages, and my next task is to mark the three policies that generate the most disputed answers.

I'll share that review in a future post. If you want to follow along, don't forget to subscribe.
