# Six Projects That Taught Me What to Keep

I have 195 repositories on my personal GitHub account, plus projects in the DataTalks.Club and AI Shipping Labs organizations. Coding agents made it easier to try ideas, so I also created more projects that never became part of my regular work. Some worked but were no longer useful. Others became too complex or never worked the way I wanted.

I usually start with a problem that's still vague. I try one solution, build part of it, and then learn that the approach doesn't fit. Sometimes I change the idea or remove features. Sometimes I stop. Even when the repository doesn't survive, the problem becomes clearer.

Code Explainer was a small Streamlit app I built in October 2025 to understand other people's repositories. I pasted in a GitHub URL, and it downloaded the main branch. An agent could list directories, read files, and search the codebase. The interface showed the files it had examined. I could also ask follow-up questions in the same context and see the cost of a request.

After I started using Claude Code, I stopped needing a separate interface for this. Several coding agents could clone a repository and answer questions after reading its files. Maintaining Code Explainer added work without giving me enough in return.

The fitness tracker was more personal. I had tried several workout applications, but none matched the way I trained. My first Claude Code version had few constraints and let the agent choose the frontend and backend. It didn't work, and I didn't understand why. I then asked for a Django backend and a different frontend.

I wanted workout presets and warm-up support because the tracker also needed bodyweight exercises, drop sets, weights, and repetitions. I also wanted it to remember previous weights and save unfinished sessions on the server. That would let me refresh the page or switch devices.

Then I added meals and reusable meal templates. I added bodyweight, sleep, and a metabolism view as well. The custom logic kept growing, and none of it worked properly. I gave up on the application, but it taught me how much guidance a real project needed.

The metabolism simulator was partly an application and partly an experiment with the Ralph Wiggum continuation loop. I wanted to see what Claude Code would do if it worked on one project for many hours. The simulator covered my routines. It was meant to model food and exercise as well as glucose, hormones, energy, and recovery. I asked Claude to use a client-server architecture with unit, integration, and Playwright tests.

After three hours the interface existed, but its buttons did nothing. After 20 hours, food and exercise logging still failed. Instead of fixing the API, Claude displayed demo data. That made the application look functional while the backend was broken.

After several days there was a polished dashboard and many features, but it still wasn't reliable. I wouldn't let a loop like this run on a real project without clear requirements, tests, review, and somebody responsible for accepting the work.

CodeHive came from that problem. I wanted a tool that enforced a project-manager, software-engineer, QA, and acceptance pipeline. It also needed several agent providers, subagent status, GitHub issue intake, and access from different devices. It became too ambitious, so I stopped needing its web interface after Termius gave me a simpler way to work from my phone.

Litehive extracted the enforced pipeline and provider switching into a local command-line tool. It used SQLite state, worktrees, and task recovery. Logs and several agent engines completed the setup. I spent more than a month on it and rewrote it several times, but it never became stable.

Its state machine was deterministic, but the whole tool was too rigid for how I worked.

Two smaller tools survived, and Heru moved provider-specific command handling out of Litehive. That included output, session, and resume support. Quse normalized quota checks across Codex, Claude Code, Copilot, and Z.ai. It became the project I use most from this group. Merm is a pure Python Mermaid renderer that works, although I usually render diagrams in a browser with mermaid.js.

I don't consider these projects a waste. One replaced a tool I no longer needed, and another showed how quickly custom requirements can overwhelm a personal application. The larger experiments helped me simplify my agent workflow. Sometimes that produced a smaller tool. Sometimes it produced a clearer decision about what not to build next.
