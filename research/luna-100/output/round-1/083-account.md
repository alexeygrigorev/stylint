# Building the Interview Canvas in Small Steps

The project was based on a full-day AI Shipping Labs workshop. I wanted each stage to leave something I could open and test, rather than wait until the end to discover that the concept or the connection between the two screens was wrong.

That constraint shaped the order of implementation.

It kept the work concrete.

For the second AI Dev Tools Zoomcamp workshop, I built an application for system-design interviews. An interviewer creates a session and shares a link. The interviewee joins, both people draw diagrams, and changes appear in real time. Two browser sessions use the same room through WebSockets, while FastAPI handles events and SQLite stores the state.

I did not start with the database. First I turned the idea into a specification with ChatGPT in dictation mode. The specification had to explain who creates a session, how a candidate joins, what can be placed on the canvas, and how both participants see changes. Without those decisions, an agent could build an application that worked but solved a different problem.

The first implementation was a frontend prototype. I used Lovable because I am not a frontend engineer and prefer its design choices to a random stack selection. The important instruction was to centralize every backend call in a service layer and provide a mock implementation. That made the interface interactive before a real backend existed and gave me one integration point to replace later.

After moving the exported React project into a repository, I created backend, frontend, and docs folders and added AGENTS.md with commands and working rules. Then I asked an agent to read the frontend service layer and write openapi.yaml. This document described endpoints, paths, request and response bodies, and authentication. The backend could now target an explicit contract instead of guessing from screens.

I implemented the backend with FastAPI and an in-memory store. I asked for routers, models, store, authentication with hashed passwords and bearer tokens, and tests. At that stage the point was to make the frontend-backend connection work. Persistence could wait. A Makefile hid the command I always forget and made `make run` start the server.

Once the real client connected, I tested two browser windows. One created a session and produced a join link; the other joined and changed the canvas. CORS problems and smaller failures appeared, which is exactly why this stage exists before adding more infrastructure.

Finally I replaced the in-memory store with SQLite and SQLAlchemy, configured through an environment variable. SQLAlchemy kept the application open to another database later. After a restart, the sessions and diagrams remained. Each stage left a concrete result: a specification, a frontend, a connected backend, and persistent state.
