# This is the first article in a series based

I’m documenting one concrete piece of work here. The original material describes what was tried, what changed, and which parts remained useful. The important details are the decisions and the reasons behind them.

This is the first article in a series based on , the free course we run at DataTalks.Club.

* Part 1:  (this article)
* Part 2: 
* Part 3: 
* Part 4: 
* Part 5: TBA

Subscribe to receive the next article in the series.

When we give an agent a task, it can quickly implement it.

A weak agent that misunderstands us writes fifty lines of broken code.

The code works, but it isn’t what the application needsed.

We spend it saying precisely what we want and checking what came back.

Then we decompose the request into tasks and assign them to a product manager, a software engineer, and a QA engineer.

We cover topics like:

* Spec-driven development
* Context engineering
* Loop engineering
* Graph engineering

We’ll use a deliberately vague project idea: a tool for weekly feedback for projects.

You can see the final result in the .

We have to think it through in detail and give explicit instructions.

We start with the specification, make sure it aligns with our vision, and only then write the code from it.

* Who are the users for this tool?

If we don’t specify these things and give the idea directly to a coding agent, it’ll fill the gaps.

It came up with `weekly-feedback`, a command-line tool for tracking weekly project status.

It also created documentation and covered the app with 62 tests, all of which passed.

I needed a web tool for a team retrospective that captures feedback from teams in the form of “Start/Stop/Continue”.

## Start in a chat assistant

Instead of giving a prompt directly to the coding assistant, I start in a chat application and talk the idea through.

I begin with the same vague idea:



This way, it is possible to use AI as our brainstorming partner and find out precisely what we want:

* Who contributes feedback?

* What can people see before the reveal?

All cards appear at the same time.

Decisions and action items from the discussion.

They can upload audio, video, or a transcript after the meeting, but built-in recording isn’t part of the first version.

## Bootstrapping a project

Create a project from this specification:



Copy the `plan.md` file:



You can find the  from this project in the Retroloop repository.

With those commits, it is possible to review what the agent changed.

## Choose the stack and architecture

During the brainstorming session, we didn’t choose the tech stack.

I choose Django because I know it well enough to review.

It’s also okay not to have a preference and to let the agent select what it thinks will work best.

Review the tasks and ask the agent to merge tasks that are too small or split tasks that don’t fit into one session.

If something is out of scope for your vision of the MVP, remove it.

Ask the agent to do it:



For that to work, the application needs the `gh` CLI tool authenticated and the repo connected to the GitHub remote.

## Context engineering

The repository has a backlog now.

It must figure that out every time.

The result is specific to this project. Some parts worked, some became too complicated, and some ideas survived in a smaller form. That is enough to make the experiment useful without turning it into a universal recommendation.
