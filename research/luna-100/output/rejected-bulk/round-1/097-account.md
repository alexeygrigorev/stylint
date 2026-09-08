# This is the fifth article in a series based

I’m documenting one concrete piece of work here. The original material describes what was tried, what changed, and which parts remained useful. The important details are the decisions and the reasons behind them.

This is the fifth article in a series based on , the free course we run at DataTalks.Club.

All articles in the series:

* Part 1: 
* Part 2: 
* Part 3: 
* Part 4: 
* Part 5:  (this article)

In this article, I want to cover the two most important aspects of working with coding assistants: skills and subagents.

* A skill describes how to perform a repeatable task.

* A subagent is an agent that runs in a separate context with clear task instructions.

In addition, I’ll cover my process for creating skills and show how to run multiple agents in parallel and turn your coding agent into a task orchestrator.

Getting these concepts is enough to work with coding agents productively, and you most likely won’t need anything else.

This article is loosely based on a live workshop I did for the course.

In the workshop, I had to improvise, so the content doesn’t directly map to this article.

However, it’s still going to be useful, so check it out.

## From Markdown Files to Skills and Subagents

In Part 1 of the course, , we touched on both skills and subagents, but I didn’t define them explicitly.

Specifically, we created a few documents:

* `_docs/process.md` and the other project documents contained reusable instructions (see )
* `_docs/team/pm.md`, `_docs/team/software-engineer.md`, and `_docs/team/qa-engineer.md` described specialized roles for subagents (see ).

The aim was to keep the discussion high-level and not focus on the mechanics of any specific implementation.

We didn’t explicitly define them because it is possible to tell a coding assistant:



It will read the document and follow the steps there.

Or you can also specify the role of the agent at the beginning of a session:



Even better, you can ask it to start a subagent with this role:



It will work.

The coding assistant can just go read the file and do the task.

However, if you define these things as skills and subagents explicitly, you’ll be more effective in using them.

In this article, I’ll show you how.

## Building Block 1: Skills

A skill is a structured set of instructions for a repeatable procedure.

If you need to follow a specific sequence of actions for completing a task, you can document the steps in a skill.

Then later you can ask the agent to use this skill to perform a task.

It will read the file and follow the steps from there.

### My Skills

The practical choice is skills a lot.

For example, one of my skills is for releasing a new version of a Python package.

I maintain many Python libraries that I need to regularly update and publish.

I describe how I do it in .

It’s a process with multiple steps:

* Run the tests
* Update the version in pyproject.toml
* Push the code to GitHub as a tag
* Verify that CI publishes the package

If I want to release a new version of , I don’t want to describe these steps each time I do it.

Instead, I document this in a  and just say:



The agent understands what I need, reads the skill, and follows the steps there.

The result is specific to this project. Some parts worked, some became too complicated, and some ideas survived in a smaller form. That is enough to make the experiment useful without turning it into a universal recommendation.
