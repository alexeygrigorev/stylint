# FAQ assistant is the system that we use in

I’m documenting one concrete piece of work here. The original material describes what was tried, what changed, and which parts remained useful. The important details are the decisions and the reasons behind them.

FAQ assistant is the system that we use in DataTalks.Club to help thousands of our students find the answers to their questions faster.

It lives in  and runs on AWS Lambda.

When it occasionally breaks down, There are to pull in Alex and ask him to fix the issue.

I always felt bad that he uses his own money to pay for the project, so I offered to take it over and run it in the DataTalks.Club infra.

This setup makes many sense, but I couldn’t port it easily to the DataTalks.Club infra.

It’s been running for years now and I never had to pay for it: it was always under the free tier for AWS Lambda usage.

As a result, I had to redesign the Slack bot.

## Part 1: The FAQ Dataset

The FAQ dataset is .

It was convenient, but this approach had a few problems:

* It was frequently vandalized, so I had to manually roll the documents back.

I described the migration process in .

* A GitHub Actions workflow indexes the entire dataset with minsearch.

* For `NEW` or `UPDATE`, it opens a pull request.

I mostly relied on my gut feeling.

For creating it, The practical choice isd those incorrect decisions.

If the agent makes a mistake in a `NEW` or `UPDATE` decision, it’s easy to correct.

In this case, I will not even have a chance to review them.

There’s also a problem with collecting the evals data from historical decisions.

As a result, if we run it with the same issue again, it will say `DUPLICATE` instead of `NEW`.

Leave-one-out evaluation for a historical NEW decision

When I analyzed all my past corrections, the most common error turned out to be incorrect section placement.

Right now There are 61 cases:

* 38 expecting `NEW`
* 10 expecting `DUPLICATE`
* 7 expecting `WRONG_COURSE`
* 4 not expecting `WRONG_COURSE`
* 2 expecting `UPDATE`

In addition to testing the whole flow, There are a retrieval-only evaluation set.

You can read more about it in the .

Starting a bulk FAQ review with the clear-backlog skill

If I come across an interesting error, I ask the assistant to add it to our evals set.

If some cases can’t be fixed easily, I don’t sweat over it.

However, I do want to know that these corner cases exist.

In many cases, these discussions are worth saving in the FAQ dataset.

Also, for each course I run a few live YouTube sessions, for example:

* pre-course Q&A session
* course launch streams
* occasional office hours

I get the transcript and use AI assistant to extract potential Q&A candidates.

I review all the PRs that our FAQ automation creates in batches, and use AI to turn Slack discussions and YouTube videos into focused FAQ records.

## Part 2: Slack Bot

When you mention `@Au-Tomator` (my bot) or `@ZoomcampQABot` from Alex, both would perform RAG:

* Use search to fetch the candidate FAQ records
* Pass them to OpenAI
* Return the answer from the LLM and post it in the thread as a reply

`ZoomcampQABot` has many moving parts though.

The result is specific to this project. Some parts worked, some became too complicated, and some ideas survived in a smaller form. That is enough to make the experiment useful without turning it into a universal recommendation.
