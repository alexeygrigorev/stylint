# This is the third article in a series for: a practical guide

This article explains the workflow described in the source. The goal is to make the sequence understandable: start with the problem, choose a small implementation, check what it does, and keep the limitations visible.

This is the third article in a series for , the free course we run at DataTalks.Club.

All articles in the series:

* Part 1: 
* Part 2: 
* Part 3:  (this article)
* Part 4: 
* Part 5: TBA

In this article, I want to take a web application and make it accessible for everyone on the internet.

We will:

* Take the application that’s already working locally
* Containerize the application
* Switch from SQLite to Postgres
* Add integration tests
* Deploy to AWS
* Set up CI/CD via GitHub Actions

It’s based on the second half of the full-day workshop I did for AI Shipping Labs: .

## Recap

In the , we started building an application for system-design interviews.

An interviewer creates a session and shares a link with a candidate.

When the candidate updates something on the canvas, the interviewer sees the updates in real time.

* First, we created the frontend only with React
* Then we created an OpenAPI specification for defining the frontend-backend API
* Next, we created the backend from this specification
* We added database support with SQLite and SQLAlchemy

You can find the code in the  repository.

## Containerization

When we run the application locally, the application needs to execute two commands: one for the frontend and one for the backend.

Let’s run them in two separate terminals:



As a result,, we have two services, and the application needs to deploy them to production.

We may think that the application needs two containers: one for the frontend and one for the backend.

During development, we run the frontend as a separate service because we use Vite.

Vite watches the frontend code and refreshes the page when we make changes.

It’s very convenient because it is possible to see our changes immediately.

In production, the frontend code doesn’t change while the application is running.

We build it once and get a set of static HTML, CSS, and JavaScript files.

That means we don’t need a separate container for the frontend: the backend can serve these files.

In development (1), the frontend and backend run separately.

In production (2, 3), FastAPI serves the built frontend from one container

Ask the coding assistant to create it:



We get a two-stage Docker build:

* First, we use a Node.js image to compile the frontend
* Then we build the backend and copy only the frontend files without the Node.js dependencies

You can see the .

Build and run the image from the repository root:



Here we specify a named Docker volume `sdip-data` that will keep the SQLite database between container runs.

Open the application at  and test it:

* Create an interview session
* Open the join link in a different browser window
* Move an element in the candidate window
* Check that the interviewer sees the change

We’ll repeat this test again.

I’ll refer to it as the two-session test.

## Switch from SQLite to Postgres

SQLite is very convenient for local development.

It keeps the data in a single file and doesn’t need a separate database server.

However, for production, we typically use Postgres or a similar database.

A useful way to apply this is to keep each decision next to the constraint that caused it. Begin with the smallest working version, verify the important path, and only then add the next piece. When a tool produces something that looks complete, inspect the underlying behavior as well. The source is careful about this distinction, and it is the part worth carrying into another project.
