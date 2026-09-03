# Building a Lightweight Intake Queue for Community Questions

On 14 March 2026, my community support queue had 43 unanswered threads. The oldest had waited 31 hours, and two volunteers had answered the same pricing question within ten minutes. I built a small intake process so the next week would be less chaotic.

I generated the workspace, messages, measurements, and helpers as a synthetic style exercise. The engineering moves still follow a practitioner build log.

In this post, I'll share:

- the rules I wrote before automating anything
- how the intake queue is organized
- why I kept routing manual for the first week
- how tags and escalation categories work
- what changed after 214 questions

## One Channel, Forty-Three Threads

The community had one channel for every request. A bug report could sit next to a homework question, a partnership offer, and a person asking for a job referral. Volunteers scanned the channel between other work, so items arrived faster than decisions.

My first instinct was to build a classifier. It would read each message, predict the topic, and assign a helper. I stopped after writing the prompt. The main failure was already visible in the old channel: some messages were missing the information needed for any route.

So the first version moved work instead of understanding it. It made one place to decide what happened next.

## Define the Minimum Record

Every request needed a stable record, so I chose Slack's workflow builder because volunteers already knew it.

That tool produced a message in `#intake` with five fields:

- request type
- short title
- original thread link
- request date
- current owner

I tested the form with three realistic messages. A link, a date, and a short title let another volunteer understand most cases without scrolling back. Free-text description stayed optional because people paste logs inconsistently.

The workflow posts this compact record:

```text
Type: course access
Title: Cannot open week 3 notebook
Thread: 2026/03/14 C0382
Owner: unassigned
Opened: 2026-03-14 09:12 CET
```

That format made the channel scannable and exposed records with a missing owner.

## Route by Defaults

I created three routes before any automation:

- general course questions go to two volunteer moderators
- bugs and access failures go to the operations rota
- partnership and paid-work requests go to me

The routes took 25 minutes to write and prevented most ownership fights. They also gave each owner a visible default. A volunteer could move an item when the category was wrong, and the mover left a one-line reason.

We used this manual routing for seven days. Of 86 questions, 68 stayed in their original route, twelve changed once, and six needed more information before they could move anywhere.

That result convinced me the routing labels were good enough. It also showed that reminders were more urgent than classification.

## Use Tags for Work, Not Identity

My first tag list had 14 topic labels, but it looked more organized than it worked. Helpers asked whether "model", "deployment", and "inference" formed mutually exclusive groups.

I reduced the tags to seven and wrote examples next to each:

- missing information
- course material
- environment or installation
- evaluation
- community event
- paid engagement
- safety or harassment

The important change was purpose, because tags answer two operational questions:

- what blocks progress
- who should look next

For example, "I can't install package X in Colab" is an environment item even if the package relates to evaluation. When a later question involved both topics, the helper opened a course-material thread and left the intake item tagged as an environment blocker.

## Clean Up Stale Threads

Intake queues fail quietly when old items stay visible, so every Monday I checked the queue for three conditions:

- items older than five days need an owner action
- items missing details need one request and a 48-hour timer
- resolved items are archived with a one-sentence outcome

The routine started on 23 March and took 18 minutes the first time. I found nine stale records. Five had been resolved in the original Slack threads but were still open in intake. Two volunteers had replied without updating the form.

I made resolution a form action instead of a social convention, and the responder selected one of three options:

- answered
- closed without response
- moved to a bug tracker

Then the workflow changed the owner to `done` and added the date.

In the following two weeks, the median age of unresolved questions fell from 26 hours to 11 hours. That improvement came from visible ownership more than from faster replies.

## Escalate Only Three Cases

Escalation needs boundaries because otherwise every hard message feels urgent.

Our fictional community therefore used exactly three categories:

- normal checks can't restore account access
- a report involves harassment or personal data
- a paid engagement could conflict with course policy

Each category had one named backup owner and a target response time. Access issues aimed for four working hours. Safety reports aimed for one hour during waking hours and eight hours overnight. Partner requests had no public target, but I checked the queue every morning.

When an item met a condition, the owner added `escalate` and tagged me. The message included the record link and one sentence describing the risk. I replied with a decision in the same thread, so the next incident had an example to copy.

One request for a free consultation looked like a partnership offer. It didn't meet any condition, so it stayed in the normal queue and received a public price link.

## Results After 214 Questions

After five weeks, the queue had 214 records. Of those, 171 were answered and 26 were closed without response. Another 17 stayed open, while nine records moved to GitHub and five became documentation updates.

The Slack workflow still does no automatic classification, and that limitation surprised one volunteer. It kept the system explainable because a person could correct a wrong route in seconds and leave the reason.

The biggest remaining gap is recurring questions. We answer them individually even when 12 people ask the same thing in a month. My next experiment will group closed items weekly and propose candidates for a FAQ.

## Lessons From Five Weeks

Start with a shared queue and clear ownership. Those two pieces give you measurements and a place to try better routing later.

The rule I took from this project is to avoid automating a decision until people can make it consistently from the visible record. I plan to write about the FAQ grouping experiment soon. Subscribe for updates.
