# A Simple Way to Explore ChatGPT Data



The useful part of this example is the workflow. I will walk through the problem, the decisions, and the limits so the idea stays connected to what actually happened. 

I often use ChatGPT for brainstorming. When I have an idea, I brain-dump it in dictation mode, and

ChatGPT helps me organize my thoughts and formulate the right questions. Sometimes I switch to research

mode to explore existing solutions or what has already been implemented for my idea. A while back, when

the first cohort of my AI Engineering Buildcamp course on Maven launched in September 2025, I was

considering my next project to be a course continuation. I discussed it with ChatGPT, created a solid

outline, but then got busy with Buildcamp and couldn’t develop it further. Later, I wanted to find that

conversation. I tried using the ChatGPT search, but it couldn’t locate it. I manually scrolled through

the chat history and searched for keywords, reviewing many messages. I thought it was from December, but

I wasn’t sure. The search proved ineffective. Eventually, I decided the idea was lost and that I would

need to start over. While the thoughts themselves weren’t entirely gone, the structure I’d built seemed

to be lost. Some time later, I noticed that ChatGPT has a data export feature. I downloaded it, but my

Windows laptop couldn’t open the file properly. Claude Code managed to extract the most important

content, but I didn’t want to sift through a 155 MB JSON file to find the necessary conversation.

https://github.com/alexeygrigorev/chatgpt-data-viewer/ and built it overnight with Claude Code. In this

post, I’ll walk you through how I did it and how you can use ChatGPT Data Viewer too. ChatGPT Data

Export As I mentioned in the intro, I started by exporting data from my ChatGPT account. Here’s how I

did it: The data controls settings in ChatGPT with the export data option A few minutes later, I

received a notification that my export was ready. OpenAI email notification when the data export is

ready for download The download was 775 MB! Yes, I talk to ChatGPT a lot. The exported download file -

775 MB of conversations It turned out that the ZIP file from ChatGPT was incomplete. Windows couldn’t

open it. I tried downloading it twice with the same result. Windows cannot open the folder; the ZIP from

ChatGPT was invalid But Claude Code could still extract the most important content. ~155 MB160 MB, and

other files 160 MB that visualizes the conversations, showing example threads like a discussion of

flat-earth beliefs: Example conversation from chat.html Implementation I had a large conversations.json

file that contained the main conversation data, and I wanted to visualize it. My initial idea was to

create a contribution graph similar to GitHub’s, allowing me to click on any day to see the relevant

information. I discussed this concept with Claude, and here’s the mockup of the UI design that we came

up with: UI design mockup with contribution heatmap and conversation list Clause also suggested that we

need to specify the API response format. Here’s what it came up with: API endpoint designs for

statistics, contribution data, and conversation lists I then described how the application should look

to Claude Code. We planned both the backend and frontend for visualization: Architecture: FastAPI

backend with Vite



That is the part I would keep from this example: connect each tool to the problem that made it necessary, and keep the limitation next to the claim. The details matter because they explain what can be reused and what was specific to this project.
