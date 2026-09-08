# Building a Viewer for My ChatGPT History

I often use ChatGPT in dictation mode as a brainstorming partner. When an idea appears, I brain-dump it and use the conversation to organize my thoughts and formulate questions. In September 2025, when the first cohort of my AI Engineering Buildcamp launched, I considered making the next project a continuation of the course. I created a solid outline with ChatGPT, then became busy and left it there.

Later I wanted to recover that conversation, but ChatGPT search couldn't find it. I scrolled through the history manually and tried keywords across many messages, but I wasn't sure which month to search. The approach was ineffective, and I eventually assumed the idea was lost and that I would need to start over.

## Recovering the export

Some time later, I remembered that ChatGPT offered a data export. I downloaded it, but the 775 MB download didn't open correctly on my Windows laptop. The ZIP archive was incomplete. Downloading it twice produced the same result.

Claude Code could extract important content, but the main `conversations.json` file was about 155 MB. Searching that manually wasn't a practical way to find one conversation.

That failure suggested a small tool. I built ChatGPT Data Viewer overnight with Claude Code so I could visualize and search the history locally. My initial interface idea was a GitHub-like contribution graph. Clicking a day would show that date's conversations. I discussed the design with Claude and planned API responses for statistics, contribution data and conversation lists.

## Letting Claude implement the plan

After the UI mockup and API plan were ready, I described the backend and frontend to Claude Code. The planned backend used FastAPI, while the frontend used vanilla JavaScript bundled with Vite. I didn't use tests or Test-Driven Development.

My workflow was to obtain the export and ask Claude to examine data in the corrupted ZIP. We reviewed the data together. I asked about its contents and API models, then let Claude manage the implementation. I didn't examine the code myself.

The first working version stabilized in one or two iterations. The total effort took about two to three hours. That included requesting and downloading the export, extracting the corrupted archive, building the implementation, and refining its design and structure.

The final architecture stayed compact, with FastAPI handling the Python backend in one `main.py` file. The frontend used vanilla JavaScript bundled by Vite, with `main.js` importing the stylesheet and `app.js`. minsearch powered search.

FastAPI also served the built `frontend/dist/` directory, so one server handled the API and interface without a separate frontend server or reverse proxy.

## Results from the index

Once the archive was indexed, it contained 2,808 conversations and 45,247 messages spanning 2022-12-21 to 2026-02-06. The most-used models were gpt-4o and gpt-5. I also found my earliest saved conversation, from 2022-12-21, about MLOps workshop proposals and converting ML pipelines with DVC.

The lost Buildcamp conversation appeared immediately in the first search results. The initial indexing took some time, so I asked Claude to add caching for faster later runs. The viewer also lets me select a date and see that day's conversation titles and message counts. This is easier than navigating the normal web history.
