# A Playbook for Community Helpers

I wrote this synthetic style exercise as a how-to guide, and the community, members and messages below are fictional. In January 2026 the coding community I help moderate passed 6,000 members. The five volunteer helpers kept asking me what to do with a borderline post.

The helpers had enthusiasm and no shared procedure. Each of them improvised, answers drifted in tone, and escalations arrived without the context a moderator needs. So we wrote a one-page playbook, and this post walks you through its four moves.

In this post, I'll share:

- how we welcome a new helper in the first week
- how to diagnose a report before answering it
- how to answer with evidence and named limits
- when and how to escalate to the moderation channel
- the mistakes the five of us kept making
- where the playbook stands after six months

## 1. Welcome And Set Expectations

Every new helper gets a 20-minute call and one page of context. We spend the first 10 minutes on the tags we answer and the last 10 on the escalation channel. The one-pager sets a weekly budget of one to two hours, three tags in scope, and two tags we ignore.

The welcome message goes out right after the call:

```text
Hi NAME, thanks for stepping up as a helper.
Your scope: threads tagged #help, one to two hours a week.
You are never on duty alone - #mod has three people in it.
When unsure, say so in the thread and ping the mod on call.
```

The message does two jobs at the start: it sets the time budget before enthusiasm takes over. It also names a person to ask, so no helper sits alone with a hard thread.

## 2. Diagnose Before Answering

Most posts miss one of three details. The reporter skips the exact command they ran, the full error text, or the version numbers of the tools involved. A helper's first reply asks for the missing piece and nothing else.

That single move resolves about a third of threads without a second round.

The template I paste looks like this:

```text
Thanks for the report. To reproduce it I need:
1. the exact command you ran
2. the full error text, not a screenshot
3. the version from `app --version`
```

You don't need the perfect answer in the first reply. You need a reproduction path, and the numbered list makes the request feel routine instead of demanding. The list also protects the helper, because a missing-detail request reads as procedure rather than as criticism.

## 3. Answer With Evidence

An answer includes a docs link, a code snippet, or a named page from the community FAQ. When we lack all three, the honest reply says so and estimates when someone will check. Guessing from memory reads faster and costs more later, because a wrong answer travels further than no answer.

A partial answer works when it names its own limits:

```text
This fails on Python 3.12 because libA dropped the sync API.
Pass use_async=False to keep the old behavior.
The migration note in docs/migrations.md lists two more changes.
```

The reply gives a working fix, names the version boundary, and mentions a file the reporter can read. Three sentences, no hedging vocabulary, and nothing invented.

## 4. Escalate With Full Context

Escalation goes to the #mod channel, and a good escalation post has three parts.

It includes the thread link, the steps you already tried, and your suspicion in one line:

```text
Escalation: thread 4482
Tried: asked for versions, suggested a rollback
Suspect: banned link added in an edit
```

The playbook sets two escalation triggers. A helper escalates after two of their own replies failed, or when the thread involves money, harassment, or deletion. Everything else stays with the helper, because a moderator with 40 pings stops reading them.

We learned the link rule the hard way. In February a helper escalated by description, the moderator found the wrong thread, and the reply went to an innocent post. The rule I took from it: no escalation without a link.

## Common Mistakes

The five of us keep making the same four mistakes:

- answering from memory without opening the linked docs
- staying polite at the cost of a concrete next step
- escalating without the thread link or the suspect line
- spending 40 minutes on one thread when the budget is 20

The playbook says nothing about tone on purpose. A plain, short reply did better than a friendly vague one in every thread we reviewed. We reread the list every quarter, and each helper adds their own recurring slip to it.

## The Playbook In Practice

Four helpers joined since January, and all four started with the call and the page. Median time to a first useful answer dropped from about 6 hours in January to about 2 hours in June. The question mix changed too, so I don't claim full credit for the drop.

The playbook stays one page long on purpose. When it grew to two pages in March, the helpers stopped reading it, and we cut it back within a week. It now lives next to the welcome template in the community wiki, and both files get one review per quarter.

I'll write about the moderation queue in a future post. If you want to follow along, don't forget to subscribe.
