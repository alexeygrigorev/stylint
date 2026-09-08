# There are many projects that The work started with: a practical guide

This article explains the workflow described in the source. The goal is to make the sequence understandable: start with the problem, choose a small implementation, check what it does, and keep the limitations visible.

There are many projects that The work started with some grand idea, spent time on, and then never quite did anything with.

I abandoned many of them at different stages.

With coding agents, I write a lot more code than ever before, because I can try ideas faster.

These projects may not reach their final form, and I may not use them afterward, but building them still teaches me something.

Often, I start with a problem that is not clear yet.

The project itself may not survive, but the problem becomes clearer.

In this post, I’ll share:

* A few projects The work started and later abandoned
* Why some of them were still useful
* Which ideas survived as smaller tools
* What I learned from having all this dead weight in my repositories

## Code Explainer

In October 2025, The project was built a small Streamlit app to help understand other people’s repositories.

The interface showed what it was looking at, which files it had analyzed, and how much the request cost.

I can just ask Claude Code, Codex, or another coding agent to explain any project.

Project:  - a Streamlit app that loads a GitHub repository and uses an AI agent with file-reading, search, and directory-listing tools to explain it.

It was my first project where The practical choice isd Claude Code more intentionally.

I had tried several apps and trackers, but none of them matched the way I train.

I told it to choose whatever stack it wanted.

The aim was to define workout presets for different days, start a workout from a preset, and log the details the way I actually train: warm-ups, bodyweight exercises, drop sets, weights, and reps.

By that point, the project had many custom logic, and none of it worked properly.

It did not become something The practical choice is every day, but it helped me understand how Claude Code behaves on a real project: where it helps, where it needs more guidance, and how quickly a personal tool can grow once I start adding every feature I want.

## The Metabolism Simulator

In January 2026, The work started  more seriously.

The first project I tested with this setup was a metabolism simulator.

Since I do sports, I’m genuinely interested in how metabolism works.

How should I eat after a workout?

It would show what happens when a person eats, trains, or sleeps: glucose, hormones, energy, and muscle recovery.

There was a computer game in the 90s called Komputerschik, or “the Computer Guy”.

The aim was to change inputs and see cause and effect.

After that, I turned on the loop and let it work.

After 20 hours, it had added many more features, but food and exercise logging still did not work.

I let Claude run for a few more days.

The loop can produce something that looks good, but it isn’t reliable.

You need clear requirements, grooming, tests, review, and somebody to accept the work.

It showed me what breaks when I let an agent run without enough structure, and it pushed me toward the process The practical choice is now.

A useful way to apply this is to keep each decision next to the constraint that caused it. Begin with the smallest working version, verify the important path, and only then add the next piece. When a tool produces something that looks complete, inspect the underlying behavior as well. The source is careful about this distinction, and it is the part worth carrying into another project.
