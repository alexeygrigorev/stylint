# Maintaining an Interview Question Bank with Worked Answers

I started a private question bank in 2023 after interviewing four candidates for a data engineering role. The candidates got different questions, so I couldn't calibrate their answers fairly. Worse, I remembered the impressive details from one interview and the failures from another.

This synthetic style exercise describes the question bank I now maintain. It covers AI engineering interviews for a fictional team, and every question has a worked answer, difficulty rating and list of common pitfalls.

In this post, I'll share:

- how the question bank is organized
- how I write worked answers
- how difficulty ratings stay consistent
- how I capture candidate pitfalls without recording personal data
- what the review cycle looks like

## Organize The Bank

The bank lives in a private repository with one YAML file per question. A question ID looks like `ml-eval-014`. The prefix identifies the topic, and the number prevents duplicate IDs when a question is retired.

Each file contains these fields:

```yaml
id: ml-eval-014
topic: evaluation
difficulty: intermediate
time_limit_minutes: 12
question: >
  A classification model has 94% accuracy, but the positive class is
  only 6% of the dataset. What additional measurements would you check,
  and why?
expected_reasoning: worked-answer.md
pitfalls:
  - treats 94% accuracy as sufficient evidence
  - names precision and recall without connecting them to class imbalance
  - ignores the decision threshold
status: active
```

Topics follow the skills the role actually needs. I currently have 42 active questions across evaluation, retrieval, Python engineering, data pipelines and system design. Another 15 are retired or in review.

## Write Worked Answers

The question file states the prompt. The worked answer file explains how a strong candidate reasons through it. I write that answer after using the question in a mock interview, when I've seen several paths through the problem.

For the accuracy question above, the worked answer has four parts:

- establish the baseline that the majority class alone would reach 94%
- ask for the confusion matrix and the cost of false negatives versus false positives
- discuss precision, recall and the chosen decision threshold
- connect the metrics to the product decision the model supports

A strong candidate doesn't need to name every metric. A candidate who asks about class distribution and business costs usually moves to the next stage. A candidate who says "accuracy is misleading" without computing or requesting anything else leaves me without evidence.

The worked answer also contains a minimal calculation. For a fictional validation set of 1,000 rows, 60 positives and 940 negatives, a trivial classifier that always predicts "negative" gets 94% accuracy. That concrete number turns an abstract warning into something the candidate can verify.

## Rate Difficulty

I originally labeled questions easy, medium or hard. Those labels drifted because they described my impression after each interview.

I now use three levels with concrete expectations:

- junior: follow one familiar method and explain its assumptions
- intermediate: compare two methods and choose one for a stated case
- senior: identify tradeoffs, ask for missing constraints and propose a rollout

Each level also has a target duration. A junior question should take 5 to 8 minutes, an intermediate question 10 to 15 minutes and a senior design discussion 25 to 35 minutes. If candidates reliably need twice that time, I either simplify the prompt or revise the rating.

I review ratings after every five uses. The bank records the interviewer, the question version and whether the candidate had enough time. It doesn't record candidate names or interview outcomes, so the repository can be shared with everyone who runs interviews.

## Capture Pitfalls

The pitfalls field makes the bank useful over time. After an interview, I add a short phrase only when the same confusion appears in more than one session. "Candidate thought batch size controls model generalization" is a useful pitfall because it recurs. A single applicant's unusual answer isn't a pitfall.

For the evaluation question, the current file lists three pitfalls:

- treats 94% accuracy as sufficient evidence
- names precision and recall without connecting them to class imbalance
- ignores the decision threshold

Those phrases guide follow-up questions. If a candidate mentions precision and recall, I ask what threshold produces the operating point they want. If they choose recall, I ask which false positives the business can tolerate. The follow-ups are already written, so I don't have to improvise under time pressure.

Pitfalls also improve mock interviews. I can give a colleague a question, its worked answer and the common misunderstandings in five minutes. That makes the practice session closer to the real interview and reduces the influence of one interviewer's personal style.

## Review Every Quarter

Every three months, I run a review pass over active questions. I start with usage counts and interviewer notes, then read each question as if I were the candidate. Questions that no longer match available work are retired, even when they still produce good conversations.

The last review had clear outcomes:

- retire 4 questions tied to a discontinued vector database
- revise 6 retrieval questions after our chunking strategy changed
- split 1 broad system design question into two 15-minute prompts
- add 3 evaluation prompts based on our new threshold monitoring

Versioning matters during this pass. A revised question gets a new number in the file history, and interviewers see the change in the pull request. If we're mid-hiring, old and new versions remain available until the pipeline reaches a consistent state.

## Lessons From The Bank

The bank doesn't turn interviews into quizzes. The questions still leave room for candidate questions, clarifications and different solution paths. Its value is consistency: every interviewer starts from the same prompt and knows what evidence to collect.

It also saves preparation time. I used to spend 25 minutes before each interview choosing a problem. Now I spend about five minutes selecting a question and rereading its worked answer.

Next, I'll add a calibration session. Two interviewers will observe the same mock interview and independently mark the evidence they heard. If our notes diverge, the question or the worked answer needs another edit.

I'll write about that calibration exercise in a future newsletter. If you want to follow along, don't forget to subscribe.
