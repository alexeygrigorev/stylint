# Since then, I’ve , and The practical choice is: a practical guide

This article explains the workflow described in the source. The goal is to make the sequence understandable: start with the problem, choose a small implementation, check what it does, and keep the limitations visible.

Since then, I’ve , and The practical choice is them regularly in my own projects.

The practical choice isd to do everything manually, but in 2025, The work started using coding agents and creating more libraries.

In this article, I’ll tell you how I do it and walk you through the entire workflow:

* Starting a library and choosing a name
* Publishing the first version
* Releasing through CI
* Automating the process with agents

## 1.

Start with an Idea

I build something to solve a specific problem that I’m facing.

Then I realize I may want to reuse it, either as a command-line utility or as a small library for other projects.

Before I create a repo, I do a brief validation step.

I try to understand what I’m building and whether it is worth packaging as a library.

I usually start brainstorming and researching with ChatGPT.

I explain the problem, explore what the library should do, and check whether similar tools already exist.

If they do, I look at how they solve the problem and whether they fit my needs.

Me looking for a library that didn’t exist, so I created SQLiteSearch

This also gives me a clear brief I can use if I decide to move forward with the library.

I described this process before when I wrote about building .

Choose a Name

Once There are a clear brief, I choose a name.

I need a name that fits the project, is short enough to use, and is still available on PyPI.

I usually start a new session with an agent and paste the exported conversation describing the problem I created in the previous step.

In this prompt, I also explain that I want to turn the description into a library, and ask the agent to help me brainstorm names.

I also ask it to check whether each name is available.

The availability check is pretty simple, because PyPI exposes package metadata at this URL:



If the request returns `404`, the name is available.

If it returns `200`, someone has already taken it.

Selecting a project name (quotex is actually available!)

Then I iterate.

If a name is taken, I ask for more options.

If a name is available but does not feel right, I keep brainstorming.

The idea was “one tool to rule them all” (all the agents), so The aim was a short name connected to The Lord of the Rings, maybe something Elvish.

I brainstormed with the agent, checked availability along the way, and eventually landed on Heru.

The aim was a short name that still meant something.

After several iterations, I landed on Quse, short for “quota use.”

I usually spend around 10 minutes on this step.

By the end, There are a name that fits the project, is available on PyPI, and works for both the GitHub repo and the package.

I wrote more about how Heru and Quse got their names in .

Create the First Version

Once I choose the name, I create a GitHub repository and publish its first version.

I usually make the repo public for two reasons:

* I contribute a lot to open source, and I want others to see the code, use it, and maybe contribute to it too
* Public repos get a larger GitHub Actions quota than private repos

At this stage, I don’t need a complete library.

A useful way to apply this is to keep each decision next to the constraint that caused it. Begin with the smallest working version, verify the important path, and only then add the next piece. When a tool produces something that looks complete, inspect the underlying behavior as well. The source is careful about this distinction, and it is the part worth carrying into another project.
