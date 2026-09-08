# is the free course we run at DataTalks.Club

I’m documenting one concrete piece of work here. The original material describes what was tried, what changed, and which parts remained useful. The important details are the decisions and the reasons behind them.

is the free course we run at DataTalks.Club.

I showed how to do it in 3 stages:

*  - coming up with an idea, creating frontend and backend, and running it locally
*  - making the application testable and deployable, and setting up CI/CD
*  - adding dev/prod environments, collecting metrics, logs, and traces, and having AI agents react to incidents


In this article I’ll put everything together, so you can use it as a reference for developing your projects.

It doesn’t quite matter which assistant you use.

I show a sequence of steps you can follow, one after another, to take your product from a vague idea to production.

In most cases, it helps to start a new session for each step: this way, only the important things are in your agent’s context so it can finish the work faster and better.

In the build stage, we:

* Turn the raw idea into a concrete specification
* Create frontend and backend, and connect them

### 1.

It’s better to be very clear about what you want and capture this in a document called “specification”.

You can start your discussion with your AI assistant using this prompt:



At the end, ask the assistant to summarize the discussion into a markdown document.

Use this document to build the frontend.

It’s the least expensive way: you create a clickable interface and you test it with some mock data.

Put this into your coding assistant (or tools like Lovable, v0 or Bolt.new):



Save the frontend code in the `frontend/` directory.

Manual test

Come up with a test you can use to validate that your application works.

For an app that helps you find study partners, it could be something like:

1.

Sign up to the event from another browser session
6.

AGENTS.md

AGENTS.md is loaded into the agent’s context every time you start a new session.

For now let’s add one line there:



Later you can add more things here.

OpenAPI schema

We previously asked the assistant to centralize all backend calls in one place.

We will use this specification to define frontend-backend interaction:



Now we have the specification for our backend so it is possible to build it.

Ask the coding assistant to help:



You can challenge your AI assistant and ask it some questions, or just accept the option it suggests.

Backend

We have selected the technology, so let’s use it to build the backend.

First, focus on making sure the frontend-backend integration works, and then connect a proper database.

For that, I usually use Makefiles, so I can just type:



And the backend runs.

Let’s connect them:



Use the test scenario from before to make sure it works.

Test the application and ask the agent to fix the problems you discover until it works correctly.

I usually use SQLite for local development, so I’ll use it here too.

After it’s done, use the test scenario again and iterate until it fully works.

Let’s deploy it and make it available for others to use:

* Containerize it
* Deploy it to the cloud
* Automate the deployment with CI/CD

### 11.

The result is specific to this project. Some parts worked, some became too complicated, and some ideas survived in a smaller form. That is enough to make the experiment useful without turning it into a universal recommendation.
