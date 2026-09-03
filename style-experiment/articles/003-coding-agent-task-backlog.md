# Turning a Vague App Idea into a Task Backlog

I wrote this synthetic style exercise as a how-to guide. The project, dates and measurements are fictional. Last month I wanted a small expense tracker, and my first prompt to a coding agent was two sentences long. It produced a Flask app with a database, two pages and an import form.

The app looked plausible and failed my review. It allowed one currency, stored amounts as floating-point numbers and gave every user access to every expense. The agent had made reasonable guesses from bad instructions.

That failure changed my process. I now spend 20 to 30 minutes turning an idea into a reviewable backlog before the agent writes application code. The extra time replaced a three-hour cleanup session.

In this post, I'll share:

- why I stop after the idea statement
- how I write goals and constraints
- how I define interfaces first
- how I convert interfaces into tasks
- how I review the backlog with the agent

## Vague Prompts And Missing Criteria

A vague prompt gives the coding agent too much freedom. "Build an expense tracker" leaves the model to choose the database, authentication model, currency rules and deployment target. Each choice looks harmless until two of them conflict.

My first attempt used this prompt:

```text
Build a small expense tracker with Flask. Users should log in and add expenses.
```

The result had 14 files, 612 lines of Python and one migration. It also had no definition of a user, no currency field and no way to edit an expense. The acceptance test in my head didn't reach the agent.

The useful question changed from "can the model build this?" to "can I review what it plans to build?". A backlog makes that review possible.

## Write The Goal First

I start with one paragraph and no implementation words. It states who uses the app, what they do and what success looks like. For the expense tracker, I wrote that a household of two people records shared expenses in euros and reviews monthly totals.

Then I add explicit constraints. My first list had these five entries:

- store amounts as integer cents
- support only euros in the first version
- use Flask and SQLite
- allow only two predefined users
- keep every read endpoint behind login

Each constraint names a decision the agent shouldn't make. The two-user rule was important because it removed the need for registration, password reset and role management in version one.

## Define Interfaces Before Features

Next I write each API endpoint as four lines: method, path, input and response. I use plain text at this stage, even when the final app will use HTML forms. The exercise forces me to decide what data changes and who may change it.

For the first version, I wrote endpoints for adding, listing and sharing expenses. The project notes specified one endpoint:

```text
POST /expenses
input: date, description, amount_cents, payer_id, shared
success: 201 and the stored expense
failure: 400 with field errors
auth: one of the two configured users
```

This block exposed a missing decision about the "shared" field. It could mean split equally or split by percentage. I chose equal splitting for version one and put percentage splitting in a later milestone.

## Turn Interfaces Into Tasks

After the interface notes exist, I ask the coding agent to propose a backlog. The prompt includes the goal, constraints and endpoints. I also give it a definition of done: every task must be small enough for one focused review.

The first proposal contained 18 tasks, and I rejected five and rewrote four. The final backlog grouped 13 tasks into three milestones:

- a login route and SQLite schema
- create, list and update expense endpoints
- a monthly summary and basic tests

Each task names its files, expected behavior and verification. For example, one task says that `POST /expenses` rejects a negative amount with HTTP 400 and leaves the database unchanged. That sentence can be tested.

## Review The Backlog With The Agent

Reviewing the backlog is a separate session from writing code. I paste the backlog into a fresh agent session and ask for objections, missing dependencies and test cases. I don't ask it to implement anything yet.

The agent found a time-zone issue in my second pass, so I chose Berlin and stored the choice in configuration. It also noted that updates should restrict which fields can change. I added both topics to the review agenda.

I made these backlog changes after that review:

- add a time zone to the summary interface
- split amount validation into its own task
- require one test per failure response

Then I ask the agent to number the tasks in build order, and I still review its proposal. Database tasks precede endpoints, and tests travel with the endpoint task rather than waiting for a final cleanup.

## Results From Review

The second expense tracker attempt used the full backlog. The coding agent produced the first milestone in 18 minutes. I reviewed the schema and login route, requested one change to session handling and accepted the milestone after tests passed.

Across 13 tasks, four rejections referenced a specific backlog criterion. The discussion stayed about behavior, and the total work took four hours.

The limitation is planning fatigue. A tiny internal tool can drown in ceremony, so I now use this process for anything with authentication, persistence or more than two endpoints. A one-page script still gets a direct prompt.

I plan to write next about the review checklist I use for each generated task. If you want to follow along, don't forget to subscribe.
