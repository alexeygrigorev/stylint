I often use ChatGPT for brainstorming. When I have an idea, I brain-dump it in dictation mode, and ChatGPT helps me organize my thoughts and formulate the right questions. Sometimes I switch to research mode to explore existing solutions or what has already been implemented for my idea.

A while back, when the first cohort of my AI Engineering Buildcamp course on Maven launched in September 2025, I was considering my next project to be a course continuation. I discussed it with ChatGPT, created a solid outline, but then got busy with Buildcamp and couldn’t develop it further.

Later, I wanted to find that conversation. I tried using the ChatGPT search, but it couldn’t locate it. I manually scrolled through the chat history and searched for keywords, reviewing many messages. I thought it was from December, but I wasn’t sure. The search proved ineffective.

Eventually, I decided the idea was lost and that I would need to start over. While the thoughts themselves weren’t entirely gone, the structure I’d built seemed to be lost. Some time later, I noticed that ChatGPT has a data export feature. I downloaded it, but my Windows laptop couldn’t open the file properly. Claude Code managed to extract the most important content, but I didn’t want to sift through a 155 MB JSON file to find the necessary conversation.

That’s how I came up with the idea for a tool to help me easily visualize and search ChatGPT’s conversation history. I called it the [ChatGPT Data Viewer](https://github.com/alexeygrigorev/chatgpt-data-viewer/) and built it overnight with Claude Code.

In this post, I’ll walk you through how I did it and how you can use ChatGPT Data Viewer too.

## ChatGPT Data Export

As I mentioned in the intro, I started by exporting data from my ChatGPT account.

Here’s how I did it:


The data controls settings in ChatGPT with the export data option

A few minutes later, I received a notification that my export was ready.


OpenAI email notification when the data export is ready for download

The download was 775 MB! Yes, I talk to ChatGPT a lot.


The exported download file - 775 MB of conversations

It turned out that the ZIP file from ChatGPT was incomplete. Windows couldn’t open it. I tried downloading it twice with the same result.


Windows cannot open the folder; the ZIP from ChatGPT was invalid

But Claude Code could still extract the most important content.


ChatGPT export contains conversations.json (~155 MB), chat.html (160 MB), and other files

There’s also chat.html data (160 MB) that visualizes the conversations, showing example threads like a discussion of flat-earth beliefs:


Example conversation from chat.html

## Implementation

I had a large conversations.json file that contained the main conversation data, and I wanted to visualize it. My initial idea was to create a contribution graph similar to GitHub’s, allowing me to click on any day to see the relevant information.

I discussed this concept with Claude, and here’s the mockup of the UI design that we came up with:


UI design mockup with contribution heatmap and conversation list

Clause also suggested that we need to specify the API response format. Here’s what it came up with:


API endpoint designs for statistics, contribution data, and conversation lists

I then described how the application should look to Claude Code. We planned both the backend and frontend for visualization:


Architecture: FastAPI backend with Vite + vanilla JS frontend

Once the plan was finalized, I asked Claude Code to create the appreciation based on it.

We did not conduct any tests or follow Test-Driven Development (TDD). The entire development workflow was as follows:

1. I obtained the data from the ChatGPT export.
2. I asked Claude to examine the data within a corrupted ZIP archive.
3. We reviewed the data together.
4. I asked Claude questions about the contents.
5. I inquired about what the API and models should look like.
6. I did not examine the code myself; Claude managed the implementation entirely.

## Final Result: A Ready-to-Use Library


The first version of the viewer is already working with the contribution graph

The first working version came together quickly. In 1-2 iterations, the core functionality was stable. The total time spent was approximately 2-3 hours, including:

* Requesting and downloading the data export
* Handling and extracting data from a corrupted ZIP archive
* Building the initial implementation
* Refining the design and structure

The final architecture was simple, but included all the necessary components to meet my requirements:

* The backend is built with FastAPI in Python. All backend logic lives in a single file, main.py, which keeps the application easy to inspect and modify.
* The frontend is written in vanilla JavaScript and bundled with Vite. It consists of two JavaScript files. The entry point is main.js, which imports only style.css and app.js and then calls init(). The actual application logic resides in [app.js](http://app.js).
* Search functionality is powered by minsearch.
* The backend also serves the frontend. FastAPI mounts the built frontend/dist/ directory at the root path using StaticFiles. This means a single FastAPI server handles both the API endpoints and the user interface. There is no need for a separate frontend server, reverse proxy, or additional deployment setup.

The result is a compact, self-contained application that can be run and deployed with minimal configuration.

## What I Learned about My ChatGPT History

After exporting my ChatGPT data, I analyzed the archive to understand how extensively I had been using it.

Here are the numbers:

* Total conversations: 2,808
* Total messages: 45,247
* Time span: 2022-12-21 to 2026-02-06
* Most used models: gpt-4o and gpt-5

The volume alone was surprising. Over multiple years, this effectively became a searchable record of projects, experiments, drafts, and research threads.


My ChatGPT usage statistics - over 2800 conversations across multiple years

## My First ChatGPT Conversation

Out of curiosity, I wanted to look at the earliest saved conversation, which was from 2022-12-21. It was about MLOps workshop proposals and converting ML pipelines using DVC.

It is interesting to see how the early usage focused on practical infrastructure topics. Over time, the conversations expanded into research, product design, architecture planning, and content strategy.


My first saved ChatGPT conversation: MLOps Workshop Proposal and DVC pipelines

## Finding the Lost Conversation

I quickly found the course conversation on my first search. The first two chats were exactly what I needed. The search process is instantaneous.

The only bottleneck I encountered was the initial indexing. When I first loaded it, building the index took some time. I asked Claude to implement caching so that subsequent runs could use the cached index and start much faster.


Search functionality: found the course research conversations immediately

The interface allows you to select a specific date and view all conversations from that day, including their titles and message counts. This made browsing older material much easier than relying on the web UI.


Conversation list for a selected date showing titles and message counts

## Future Plans

The tool is already usable. You can export your ChatGPT data, run the viewer, and search your entire history locally.

That said, there are a few improvements I may implement:

* Better handling of corrupted ZIP archives in ChatGPT exports
* A simplified CLI entry point such as uvx chatgpt-viewer path/to/archive.zip
* Clearer documentation for others who want to run it on their own data

The core functionality is stable. The next step is to polish usability and make it easier for others to adopt.
