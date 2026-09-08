# The third cohort of my AI Engineering course wrapped: a practical guide

This article explains the workflow described in the source. The goal is to make the sequence understandable: start with the problem, choose a small implementation, check what it does, and keep the limitations visible.

The third cohort of my AI Engineering course wrapped this summer, and in this post I want to share what we built.

The projects are real-life and include an exam questions generator, a chess coach, a RAG pipeline, job tools, and research assistants.

This is not the first post about the projects that AI Buildcamp graduates built.

I wrote about the previous two cohorts earlier:

* First cohort: 
* Second cohort: 

In this post I want to describe some of these projects.

As a result,me of the course participants presented their projects live on , so we’ll start with them.

## 1) Exam Questions Generator by Salma Bouzid


Quizgen generates exam questions from the lecture slides

Salma is a data analyst who took the course to get better at building an AI app.

She’s leaving her job to work as a founder.

Her project helps university professors generate exams from their own slide decks.

You upload a course PDF and pick how many questions you want.

You also choose a mix of case studies, theory, and applied-concept questions.

A professor can approve, edit, or reject each question, then export the exam.

In the live demo she asked the model to tailor an HR-management exam to a business student in Berlin.

* The frontend is Next.js
* Supabase stores user actions plus API cost, PDF size, and regeneration prompts
* She started with Claude and later moved to OpenAI
* An LLM judge checks that a question is grounded in the course and not answerable without it



## 2) ATS Gap Analyser by Amar Agrawal


ATS Gap Analyser’s example result with a 75/100 match, missing keywords, and improvement suggestions

Amar’s  is for people who apply to jobs and never find out what went wrong.

You paste a job URL and your CV.

The app returns a match score out of 100, missing keywords, improvement suggestions, and a three-paragraph cover letter.

It doesn’t store the CV or the job description, not even in the logs.

* Extract job requirements
* Score the CV
* Suggest improvements
* Generate the cover letter

Suggestions retrieve from 50 ATS best-practice documents with minsearch.

* Eval used 50 manually written cases.

* Version 1 had 60% recall and 30% accuracy, and version 6 reached 88% recall.

* Amar kept accuracy lower on purpose: he would rather flag a missing skill than miss it.

## 3) Chess Coach Agent by Leo Cabibihan


Chess Coach practice screen with a Stockfish-backed move recommendation and a scheduled retry

Leo’s first project was a chess-coach chat, but it wasn’t useful.

You import Lichess, Chess.com, or a PGN file.

The app finds weak moments, explains them, and drills those positions.

Leo imported about 2,700 of his own Lichess games for the demo.

The stack includes FastAPI, React, Postgres with pgvector, and PydanticAI.

It also uses Stockfish, BM25 lessons, Logfire, and it’s .

Practice uses spaced repetition at 1, 3, and 7 days, doubling up to 30.

If there’s no API key, deterministic templates still run.

CThe practical choice iss a TestModel so tests stay offline.

## 4) Document Preparation Agent by Paulien Out and Alena Fojtik


ArXiv papers, manuals, and EU documents are parsed by LLM so they can be used in a RAG pipeline

Paulien and Alena build on-premise AI systems.

A useful way to apply this is to keep each decision next to the constraint that caused it. Begin with the smallest working version, verify the important path, and only then add the next piece. When a tool produces something that looks complete, inspect the underlying behavior as well. The source is careful about this distinction, and it is the part worth carrying into another project.
