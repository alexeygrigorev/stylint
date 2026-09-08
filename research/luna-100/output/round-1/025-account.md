# I Built a Searchable Viewer for My ChatGPT History

I often use ChatGPT to brainstorm. I dictate a rough idea, ask questions, and sometimes switch to research mode to look for existing solutions. When the first AI Engineering Buildcamp cohort launched in September 2025, I discussed a possible continuation course with ChatGPT and created a solid outline. Then I became busy with the Buildcamp and stopped working on it.

Later, I wanted to find that conversation. ChatGPT search could not locate it, and I manually scrolled through history and tried keywords. I thought the discussion was from December, but I was not sure. The search did not help, and I eventually assumed the idea was lost. The thoughts were still somewhere in my head, but the structure I had built seemed gone.

Then I noticed ChatGPT offered a data export. I downloaded it, but the ZIP file was incomplete and Windows could not open it. Claude Code could extract important content, but I did not want to search a 155 MB JSON file by hand. That became the idea for ChatGPT Data Viewer, a tool for visualizing and searching the conversation archive. I built the first version overnight with Claude Code.

The export download was 775 MB. It contained `conversations.json`, a `chat.html` file, and other data. I wanted a contribution graph like GitHub’s, where selecting a day would show the conversations from that date. Claude helped design the UI mockup and API response format. We planned a FastAPI backend with a Vite and vanilla JavaScript frontend, then Claude Code implemented the application.

I did not use tests or Test-Driven Development for this project. The workflow was to obtain the export, ask Claude to inspect the corrupted ZIP, review the data together, ask questions about its contents, and discuss the API and models. I did not examine the code myself; Claude handled the implementation.

The first working version stabilized after one or two iterations. The whole process took about two to three hours, including downloading the export, extracting the damaged archive, implementing the viewer, and refining its design. FastAPI served the backend and the built frontend from one application. The backend logic lived in `main.py`; the frontend used vanilla JavaScript bundled with Vite, and minsearch powered search. There was no separate frontend server or reverse proxy.

The archive revealed how much history I had accumulated: 2,808 conversations and 45,247 messages from December 21, 2022 to February 6, 2026. My most-used models were gpt-4o and gpt-5. The earliest saved conversation concerned MLOps workshop proposals and converting ML pipelines with DVC.

The viewer found the lost course conversation immediately. Initial indexing took some time, so I asked Claude to add caching for later runs. I could select a date and see the conversations, titles, and message counts from that day. The tool was already usable, though I still had ideas for better damaged-ZIP handling, a simpler CLI, and clearer documentation. The main result was simple: a private archive that had felt inaccessible became a searchable record of projects, research, drafts, and experiments.
