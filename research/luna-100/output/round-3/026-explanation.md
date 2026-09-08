# Turning a ChatGPT Export into a Searchable Archive

A local viewer becomes useful when the application's own search can't recover something important. I built ChatGPT Data Viewer after ChatGPT search failed to find an earlier conversation about a possible AI Engineering Buildcamp continuation. Manual scrolling and keyword searches across many messages were ineffective, so I needed a way to work with the exported data directly.

## Start with the awkward input

The export wasn't a neat small dataset. The download was 775 MB, and the ZIP archive was incomplete. Windows couldn't open it, even after I downloaded it twice. Claude Code still extracted important content. The archive included `conversations.json`, about 155 MB, and `chat.html`, about 160 MB.

A file that large is difficult to search by hand. The viewer therefore needed two related capabilities: a way to see activity over time and a way to search the actual conversation content. The first interface idea was a contribution graph similar to GitHub's. Selecting a date would show the conversations from that day.

## Plan the interface and API

I discussed the visual idea with Claude and used its mockup to refine the interface. We also planned the response formats for statistics, contribution data and conversation lists. Those endpoints gave the date-based view a clear API schema before implementation started.

The planned architecture used FastAPI for the backend and a vanilla JavaScript frontend bundled with Vite. I then asked Claude Code to build the application from that description. I didn't use tests or Test-Driven Development, and I didn't examine the code myself. The workflow was closer to guided construction. I supplied the data and requirements, asked questions about the API and models, and Claude managed the implementation.

The first stable version appeared after one or two iterations. The total effort was about two to three hours. That included requesting and downloading the export, handling the corrupted archive, building the initial version, and refining the design and structure.

## Keep the deployment small

The backend used FastAPI in a single `main.py` file. The frontend was vanilla JavaScript bundled by Vite, with `main.js` importing the stylesheet and `app.js`. minsearch powered the search functionality. FastAPI also served the built `frontend/dist/` directory, so one server handled the API and user interface.

This arrangement avoided a separate frontend server, reverse proxy or additional deployment setup. It kept the viewer compact enough to run locally while still providing a visual archive and search interface. The source describes it as a self-contained application with minimal configuration, rather than as a replacement for a larger data platform.

## Use the indexed archive

The archive contained 2,808 conversations and 45,247 messages spanning 2022-12-21 to 2026-02-06. The first search found the missing course conversation immediately. Initial indexing took some time, so I asked Claude to add caching for faster subsequent runs.

The date view also helps with browsing. Selecting a day shows the conversation titles and message counts, which is easier than relying on the normal ChatGPT web history. The important design choice was to make the export searchable locally, even though the input began as a large and partially corrupted download.
