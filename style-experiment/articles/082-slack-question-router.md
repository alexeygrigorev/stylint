# Adding a Router to a Slack Question Queue

Our 4,200-member Slack community sends me roughly 70 answerable questions each week. By April 2026, triage ate three hours of my Sunday, and 11 questions had aged past 48 hours without a reply.

I wrote this piece as a synthetic style exercise, and every community name and measurement is invented.

Writing more answers during the week looked obvious, so I tried it for two weeks. The backlog reappeared every weekend. Then I built a small router to classify each question, draft a reply, and decide whether a human needed to look.

In this post, I'll share:

- how the intake queue works
- how I classified questions without perfect labels
- how the router answers, escalates, and archives
- what the first month changed
- where I still intervene

## The Intake Queue

The queue starts as a saved Slack workflow. A helper adds `question` to a private intake channel, and a webhook writes the message to a local SQLite table. The row records the thread link, timestamp, and helper name.

The schema stays boring:

```sql
create table questions (
    id integer primary key,
    slack_permalink text,
    body text,
    category text,
    status text,
    created_at text
);
```

SQLite was enough because only one script writes to the table every 10 minutes. I considered Postgres, but I didn't need concurrent traffic, and I wanted a single file I could copy to my laptop.

## Classify Without Perfect Labels

I started with a rule that searched for words such as "install", "error", or "homework". It put 58% of messages into the right category over a sample of 120. The rest sat in a generic pool, which meant the rule only moved work around.

Next, I asked a small model to choose one of five classes. I wrote the class definitions in the prompt and gave two examples for each class. The fifth class covered research questions.

The first model run handled 81% of a 140-message validation set correctly. It confused assignment questions with course-content questions most often, so I added one instruction: an assignment class wins when a deadline or submission is named.

The router also returns a confidence score. Above 0.85, it continues, and below 0.85 it marks `needs-human` and stops. I picked the threshold by sorting 80 predictions and reading the middle. The review log makes that judgment call safe.

## Answer and Escalate

The router has three outcomes. It can answer, escalate, or archive a question as a duplicate. A question gets an answer only when the model can cite one of 26 curated course pages and the confidence is high enough.

The prompt asks for three fields:

- `answer`: two sentences at most
- `source`: one canonical page URL
- `next_step`: one concrete action for the member

If a field is missing, the router writes a draft to the review channel instead of Slack. Helpers approve or edit it with two Slack buttons. The approved reply goes back into the original thread, with a line naming the helper who reviewed it.

Escalation rules came directly from mistakes. In week one, the router drafted an answer to an account-access question, which should always go to two named admins. I changed the classifier to send credentials, payment, and conduct questions to humans without drafting anything.

Archiving took longer to get right. If the classifier reports duplicate and links a thread with an accepted answer, the router posts a short pointer in the old thread. If the linked answer is older than six months, it escalates instead, because course versions change.

## The First Month

The router processed 289 questions between May 4 and June 1. It answered 122 directly, sent 101 drafts to helpers, and escalated 44. It marked 22 as duplicates. Median first response fell from 19 hours to 4 hours.

The headline number needs a correction: helper time fell from about three hours on Sunday to about 90 minutes across the week, rather than disappearing. Eight drafts still needed a substantial rewrite because the cited page answered a neighboring question.

That failure produced a new check. Before posting, the router compares key nouns in the question and source page. If fewer than two nouns match, it downgrades to review. This removed another six weak answers in the following two weeks.

The classifier also drifts, so the weekly labeling stays on the calendar. Every Friday, I label 20 random results and append disagreements to the prompt examples. Four weeks produced 31 new examples, and validation accuracy moved from 81% to 88%.

## The Human Part

I approve every answer that mentions pricing, access, or a deadline. Those answers affect money, enrollment, or a person's ability to submit work, and one wrong sentence costs more than the time saved.

I also review the duplicate report each week. Two threads sometimes look identical because members use the same course term for different errors. A bad duplicate hides the new question from search, so false negatives are safer than false positives.

Finally, helpers still own tone. The router can name the next command, but it doesn't know that a member has asked three times and sounds discouraged. A helper's short human sentence often prevents a fourth attempt.

## Lessons Learned

The router worked because it had boring limits. It answered only what it could cite, and it preferred a review queue over a confident guess. The system improved because the helpers' edits became training examples instead of disappearing into Slack.

I plan to give helpers a weekly digest of misclassified questions and write about that loop after another month. Subscribe if you want to see whether the extra feedback layer survives contact with a real cohort.
