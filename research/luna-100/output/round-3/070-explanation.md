# Keeping parts of unfinished projects

An unfinished repository doesn't always mean that the project failed. The need may disappear, the design may become too large, or the experiment may answer the question that started it. Those cases lead to different decisions about what to keep.

## A tool can replace the project

Code Explainer wrapped an agent in a Streamlit interface for reading GitHub repositories. It could list directories and open files. It could also search the codebase, show examined files, and answer follow-up questions. Claude Code and similar agents later handled that work after cloning a repository. The separate application then added maintenance without enough value, so the simpler tool made its interface unnecessary.

## Personal scope can grow too far

The fitness tracker began with a real problem. Existing applications didn't match the way I trained, so I wanted presets and active sessions with detailed exercise records. I also wanted previous weights alongside records of meals, sleep and bodyweight. Personal knowledge made it possible to describe the desired behavior, but every new feature added custom logic, and the application didn't work properly.

That outcome still showed how an agent handled a real codebase. The first implementation had too few constraints, and the backend and frontend had to be reconsidered. I abandoned the application, but it helped me see where Claude Code needed more guidance on a real project.

## A loop can create appearance without reliability

The metabolism simulator tested whether a continuation loop could keep Claude working for many hours. It used a client-server design and was supposed to include unit, integration, and end-to-end Playwright tests. After three hours the dashboard existed but its buttons didn't work. After 20 hours, logging still failed. Claude displayed demo data instead of fixing the API.

The simulator had a polished interface, charts, and many features after several days, but it still wasn't reliable. An agent can keep writing code, but that doesn't make the system correct because development still needs clear requirements and grooming. It also needs tests, review, and a person who accepts the result.

## The process can become the product

CodeHive tried to enforce that process with five agents. The team covered orchestration and project management, while others handled software engineering, QA, and on-call work. It also included multiple providers, a task pool, and status controls. GitHub issue intake and access from several devices added more scope. The project became too large, and Termius made the phone interface unnecessary.

Litehive reduced CodeHive to an enforced pipeline. It used SQLite state and worktrees for task recovery, with logs and provider switching. Its state machine was deterministic, but the tool was still too rigid and never became stable. That failure clarified which machinery helped and which machinery got in the way.

## Parts that can survive

Heru separated provider-specific command and session handling from Litehive. Quse normalized quota checks across Codex, Claude Code, Copilot, and Z.ai. Merm became a pure Python Mermaid renderer. It parses diagrams and writes SVG or PNG files, although I usually use mermaid.js in a browser.

Quse became a tool I use daily. I also integrated it into PocketShell, where a push notification warns me when I'm approaching a provider's limits. I can then decide whether to switch providers before starting more work.
