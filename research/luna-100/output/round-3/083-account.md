# Building the Interview Canvas One Boundary at a Time

For the second AI Dev Tools Zoomcamp workshop, I built an application for system-design interviews. An interviewer creates a session and shares a link. A candidate joins, and both people draw on the same canvas while changes arrive through WebSockets. FastAPI handles the backend and SQLite stores the state.

I wanted every stage to leave something I could open and test. A full-day AI Shipping Labs workshop had shown me the danger of waiting until the end.

I might otherwise discover a wrong idea or a broken connection between screens too late.

I started by describing the application in detail with ChatGPT in dictation mode. The specification covered who creates a session, how a candidate joins, which canvas elements exist, and how both participants see updates.

The first implementation was a frontend prototype. I used Lovable because I'm not a frontend engineer and preferred its design choices to asking an assistant to choose a random stack.

I asked for every backend call to go through one service layer, with a mock implementation behind it. The interface could then be interactive before a server existed, and I had one place to replace when the real API was ready.

I moved the exported React project into a repository with separate backend, frontend, and docs folders. I added `AGENTS.md` with commands and working rules.

Then I asked an agent to read the frontend service layer and write `openapi.yaml`. The file described endpoints and paths. It also described request bodies, response bodies, and authentication. The backend had an explicit API to implement instead of having to infer behavior from the screens.

For the backend I chose FastAPI and an in-memory store. I asked for routers, models, authentication with hashed passwords and bearer tokens, and tests. Persistence could wait while I checked the connection between the real client and the server. A Makefile made the command easy to remember, so `make run` started the backend.

I opened two browser windows for the test. In one, I created a session and produced a join link. The other joined as the candidate and changed the canvas. The interviewer had to see that change. CORS problems and smaller failures appeared before they were mixed with database work, which made them easier to find.

After the connected path worked, I replaced the in-memory store with SQLite and SQLAlchemy. An environment variable provided the database URL, and SQLAlchemy left room for another database later.

After restarting the server, I confirmed that sessions and diagrams remained. The project finished the workshop with a specification, a frontend, a connected FastAPI backend, and persistent state. Deployment stayed for a later step.
