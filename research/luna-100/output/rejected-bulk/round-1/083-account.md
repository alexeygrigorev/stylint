# This is the second article in a series based

I’m documenting one concrete piece of work here. The original material describes what was tried, what changed, and which parts remained useful. The important details are the decisions and the reasons behind them.

This is the second article in a series based on , the free course we run at DataTalks.Club.

In the , I wrote about turning an idea into a specification.

In this article, we will create an end-to-end application from scratch.

We will cover both frontend and backend, and add a database.

All articles in the series:

* Part 1: 
* Part 2:  (this article)
* Part 3: 
* Part 4: 
* Part 5: TBA

We will create an application for system-design interviews.

As an interviewer, you create a session and share the link with the interviewee.

They can create diagrams in the app, and you see the changes in real time.

Both frontends connect to the same room through WebAs a result,ckets, so the changes appear in both sessions simultaneously.

The FastAPI backend handles those events and saves them to SQLite.

Two browser sessions collaborate through one WebAs a result,cket-backed interview room

You can find the code in the  repository.

AI System Design Canvas: the application we will develop.

It’s based on my full-day workshop I did for AI Shipping Labs: .

## Overview

Like in the , we start with an idea.

As this is only an idea, we turn it into a specification using ChatGPT.

Generate a frontend that uses mocked backend calls.

Establish backend-frontend contract by creating OpenAPI specifications from the frontend service layer.

Implement the FastAPI backend, connect it to the frontend, and test the application.

At each stage we get something concrete that it is possible to test:

* First we define the specification and make sure it reflects what we want to build.

* After that, we use the specs to create a frontend prototype that it is possible to interact with.

We mock backend calls so it is possible to test the idea.

* Then we connect the frontend to the backend.

We start with an in-memory store to make sure the frontend-backend connection works.

* Finally, we add a database so the application keeps its state after a restart.

At the end, we have a working local application that is ready for deployment.

The interfaces stay stable while temporary components are replaced one at a time

## Start with a specification

Before building the frontend, the application needs to describe the application precisely.

If we don’t do it, we will get something that works but we don’t need.

For our application, the application needs to specify:

* who creates an interview session
* how a candidate joins it
* which components they can place on the canvas
* how both people see changes in real time

This is called “Specification-Driven Development”.

We don’t spend many time here because it was the focus of the previous article .

For creating the specification, I always use ChatGPT in dictation mode.

Give the assistant as much information as possible at this stage.

Dictating the initial application idea to ChatGPT

You can see the result .

## Frontend First

Now we have the specification, but it’s only text.

There are multiple options of what you can do next:

* Focus on the database layer, define the entities, and work all the way up through backend to frontend
* Alternatively, you can start with specifying OpenAPI and define how backend and frontend interact and build both independently from there
* Or you can focus on the frontend first and then build the rest

All these approaches make sense and have their pros and cons.

The result is specific to this project. Some parts worked, some became too complicated, and some ideas survived in a smaller form. That is enough to make the experiment useful without turning it into a universal recommendation.
