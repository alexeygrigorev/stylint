# Across all 4,894 AI engineering job descriptions that I

I’m documenting one concrete piece of work here. The original material describes what was tried, what changed, and which parts remained useful. The important details are the decisions and the reasons behind them.

Across all 4,894 AI engineering job descriptions that I collected for the , evaluation consistently comes as the number one skill that AI Engineers must have.

In interviews, you’ll definitely hear something like “how do you evaluate a RAG pipeline?” or “how do you measure agent performance?”.

If you don’t include evals in your home assignment, it’s a red flag.

Why is it such an important skill?

It’s easy to build an agent these days.

I show how to do it in my .

You need to get an OpenAI key, take any agentic framework, define the instructions and the tools, and that’s it.

However, this agent will break in so many ways.

It will:

* Give a wrong answer
* Confidently hallucinate a plausible answer
* Finish without giving any answer
* Get into a loop and call the same tool over and over again
* Exhaust the context
* Call a tool with invalid arguments

That’s just the tip of the iceberg.

To make sure this agent works reliably, you need to test and evaluate it.

You don’t know how the agent is performing.

You also can’t quite change anything: every change you introduce may break the system in many ways, including the areas where you least expect it.

It takes many time to understand the problem, get input from real users, and gather the right data.

It’s not something you can just delegate to Claude and forget about it.

That’s what makes evals such an important part of AI Engineering.

In this article, I will tell you about my approach to evaluations:

* Start manually by “vibe-checking” the system, but also collect logs as early as possible
* Create a tool for labelling the logs and put together a gold standard dataset
* Create a judge that’s aligned with our judgement
* Break the agent like a QA engineer
* Get more data by generating it synthetically
* Start collecting data from real users
* Monitor your system with online evaluation
* Always refine your gold standard dataset


The stages, in the order I go through them.

Each stage adds new cases to the gold standard dataset.

## Collecting the Gold Standard Dataset

You have an agent.

There’s nothing wrong with “vibe-checking” it: you poke it, ask questions you want it to answer, and look at the results.

If they aren’t good, you figure out how to fix it.

However, already at this step you can be a bit more organized and start logging what the agent is doing.

When you ask a question and see the answer, make sure they are saved somewhere.

You do a few vibe-checking sessions, and you already have 10-15 logged records.

Now you can systematically look at these logs and classify each record into

* “good”: the answer is what you expect
* “bad”: the answer is not what you wanted to see

To help me do it, I usually vibe-code a small labelling tool.

The labelling tool for the “version 0” of the gold standard dataset

This gives you a “version 0” of the gold standard dataset - the dataset you will use for evaluating your system (sometimes it’s also called the “ground truth” dataset).

The result is specific to this project. Some parts worked, some became too complicated, and some ideas survived in a smaller form. That is enough to make the experiment useful without turning it into a universal recommendation.
