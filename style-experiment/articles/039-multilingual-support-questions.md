# Handling Multilingual Support Questions in a Course FAQ

This synthetic style exercise uses a fictional project and invented details.

Our fictional online course had 4,310 active students, and 27% wrote support questions in a language other than English. The FAQ existed only in English. Volunteers answered translated questions well, but response time rose to 19 hours, compared with 3 hours for English questions.

I didn't want a separate FAQ for every language. I wanted one canonical answer set, consistent retrieval across languages, and a clear path to a human when the model or search failed.

The support counts and response times in this article are invented examples.

In this post, I'll share:

- how I detected language without creating routing chaos
- how the multilingual index works
- how answers stay consistent across languages
- what the first six weeks showed
- when questions still go to volunteers

## Language Detection

The first version detected language on every message and routed Spanish, Portuguese, and Indonesian questions to separate flows. It created three silos and made maintenance worse.

I simplified the design, and detection still records the language code. All questions enter the same queue and retrieve from the same index. The language code affects only the preferred rendering language and the threshold for offering human support.

Detection isn't perfect because short questions such as `404` or `CSV error` have almost no language evidence. For messages under 12 characters, the system skips detection and uses the student's course profile as a weak hint. It doesn't translate based on that hint alone.

## One Multilingual Index

We used a multilingual embedding model to encode 143 FAQ answers and 412 course-policy snippets. The source of each answer is stored with its version, owner, and last review date. Student questions are embedded with the same model, so retrieval doesn't require translation first.

This design avoids one common failure. If a system translates a question into English and then searches English text, translation errors change retrieval. Our index compares meaning in a shared vector space and leaves translation for the answer step.

For evaluation, we built 96 test questions:

1. 32 in English
2. 32 in Spanish or Portuguese
3. 32 in Indonesian

Each question lists the expected FAQ answer and the expected course-policy snippet. The multilingual index reached 84% top-1 accuracy and 91% top-3 accuracy. The previous English-only flow reached 58% top-1 accuracy for non-English questions, but only because volunteers had manually tagged many of them.

## Consistent Answers

Retrieval returns canonical English text. The answer layer can render it in the student's language when confidence is high. The rendered answer always shows the original FAQ title and a link to the English version.

We use three confidence checks before rendering:

```text
retrieval score above 0.72
policy version reviewed within 90 days
no billing, account-access, or harassment flag
```

All checks must pass, and if any check fails, the system shows the best-matching English answer. It marks the answer as a suggestion and offers a volunteer. It doesn't invent a translated policy.

Volunteers can edit suggested translations, and their edits return to the answer library. This keeps language quality connected to human review instead of living only in a model.

## Six Weeks of Results

During the six-week fictional trial, the multilingual flow handled 1,538 non-English questions. Volunteers reviewed 289 of them. Average first response time fell from 19 hours to 42 minutes.

Student feedback was mixed in a useful way. Of 514 students who rated the answer, 78% found it clear. Another 11% said the answer was clear but used unnatural wording. Those comments led us to add a human translation review for the 20 most frequent answers.

The system missed some cultural context. A question about "group work" might mean a graded team assignment in one country and an optional study group in another. We added location-neutral phrasing to seven answers and linked both policy versions when both existed.

We also found a versioning bug. Three Spanish answers still referenced a deadline rule from the previous term. The answer library now hides any answer whose policy version is stale, even if retrieval ranks it first.

## Escalation to Volunteers

Some questions always go to a person:

- billing disputes
- account-access problems
- certificates and identity requests
- reports of harassment or unsafe behavior

The assistant may provide general policy text, but it can't close the issue. Volunteers see the full conversation, detected language, retrieved snippets, and the reason for escalation. That context reduces repeated questions from students.

The multilingual flow didn't replace support. It removed the translation tax from common questions so volunteers could spend time on judgment.

I'll write next about how we review stale policy answers. If you want to follow along, don't forget to subscribe.
