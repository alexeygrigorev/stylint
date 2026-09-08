# The 2026 cohort of starts today (August 31): a practical guide

This article explains the workflow described in the source. The goal is to make the sequence understandable: start with the problem, choose a small implementation, check what it does, and keep the limitations visible.

The 2026 cohort of  starts today (August 31).

The course is free, and registration is open for the next few weeks.

In this course, we use AI coding tools across the full software-development lifecycle.

* Part 1: 
* Part 2: 
* Part 3: 
* Part 4: 
* Part 5: 

In this course we give you a tool-agnostic way to work with any coding agent and increate your productivity as a developer.

Watch the launch stream:

## Start Here

Use these links to join the course and find the materials:

* .

*  to see deadlines, submit homework and projects.

It contains the module materials, recordings, homework, and final-project requirements.

*  for prerequisites, setup, logistics, and detailed guidance.

*  for talking to your peer course participants and join the `#course-ai-dev-tools-zoomcamp` channel.

The repository is the source for module materials, homework, recordings, and project requirements

## Course Curriculum

In this course, we use AI coding tools across the full software-development lifecycle.

* Part 1: 
* Part 2: 
* Part 3: 
* Part 4: 
* Part 5: 


The five modules take one application from specification through deployment, operations, and agent extensions

## Module 1: AI-Native Developer Workflow

Giving a coding agent a vague request often produces a plausible application that doesn’t solve the problem you had in mind.

We begin by improving the instructions and context we give it.

You turn a product idea into a specification and a backlog of small tasks.

You create durable project context, then separate product management, implementation, and QA into focused sessions.

You also learn how agent loops and multi-agent workflows can help with larger backlogs without removing your responsibility for review.

By the end of the module, you have a repeatable way to direct an agent and verify its work independently.

* 
* 
* 
* Homework:  ·  — due 2026-09-07

## Module 2: Build and Ship an AI-Assisted Full-Stack App

Next, you use that way of working to create a complete application.

You write a product specification and build a frontend.

Then you describe the API with OpenAPI, implement the backend, add SQLite persistence, and test the main behavior.

We use AI tools to produce the first version of each part, but we don’t accept generated code because it looks reasonable.

We look at the code, run it, compare it with the specification, and write tests for the behavior we expect.

You finish with a tested full-stack application that runs locally and follows a documented OpenAPI specification.

* 
* 
* 
* Homework:  ·  — due 2026-09-14

## Module 3: Test, Containerize, and Deploy

A working local application is only the beginning.

In this module, you test the seams between the frontend, backend, and database.

You add integration tests, move from SQLite to Postgres, package the application with Docker, and run the checks automatically in CI.

Then you deploy the application to a public URL and connect deployment to the CI pipeline.

When you merge a change that passes the required checks, the pipeline ships it.

You finish with a containerized application that other people can use and a documented way to test, deploy, and roll it back.

A useful way to apply this is to keep each decision next to the constraint that caused it. Begin with the smallest working version, verify the important path, and only then add the next piece. When a tool produces something that looks complete, inspect the underlying behavior as well. The source is careful about this distinction, and it is the part worth carrying into another project.
