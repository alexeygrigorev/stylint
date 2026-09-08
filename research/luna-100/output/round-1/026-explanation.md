# How the ChatGPT Data Viewer Works

The ChatGPT Data Viewer started with a retrieval problem. A conversation containing a useful course outline could not be found through ChatGPT’s search, and manually scrolling through history was not practical. The resulting application turned an exported archive into a local interface for searching conversations by date and content.

The input is a ChatGPT data export. In this case, the download was 775 MB and the ZIP archive was incomplete, so Windows could not open it even after two downloads. Claude Code could still extract important files. The export included a `conversations.json` file of about 155 MB and a `chat.html` file of about 160 MB. The JSON held the main conversation data used for indexing.

The first interface idea was a contribution graph similar to GitHub’s. A day on the graph could be selected to show the conversations associated with it. Claude helped produce a UI mockup and suggest API response formats for statistics, contribution data, and conversation lists. The planned application used a FastAPI backend with a Vite-bundled vanilla JavaScript frontend.

The implementation stayed compact. FastAPI handled the backend and served the built frontend from the same application. Backend logic lived in `main.py`, while the frontend used two JavaScript files bundled by Vite. minsearch powered the search. Because one server handled both the API and the user interface, the application did not need a separate frontend server, reverse proxy, or extra deployment layer.

The development process had a clear limitation. There were no tests and no Test-Driven Development. The steps were to obtain the export, have Claude inspect the corrupted archive, review the data, ask questions about the contents, and discuss the API and models. Claude managed the implementation, and the author did not inspect the code directly. The first stable result arrived after one or two iterations and took roughly two to three hours in total.

The viewer also made the archive measurable. It contained 2,808 conversations and 45,247 messages from December 21, 2022 through February 6, 2026. The most-used models were gpt-4o and gpt-5. The earliest saved conversation concerned MLOps workshop proposals and converting ML pipelines with DVC.

The search solved the original problem. The course conversation appeared in the first search, although initial indexing took some time. Caching was added so later runs could start faster. The interface could filter by date and show conversation titles and message counts, making older material easier to browse than the web interface.

The application was already usable, but the source kept several possible improvements open: better corrupted-ZIP handling, a simpler CLI, and clearer documentation. The important design choice was to keep the result self-contained. A local export, one small server, and a search index were enough to turn a private archive into a navigable record.
