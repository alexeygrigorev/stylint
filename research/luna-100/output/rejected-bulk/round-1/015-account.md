# Building a Telegram Assistant



I want to describe what happened, because the sequence of small decisions is more useful than a polished summary. 

One Thing I Want to Share The result Week I work on many projects, and most of the work happens before

anything becomes public. The result includes early thinking, small experiments, and intermediate

workflows that usually disappear once a final result is ready. That means you can only see the final

results of my work: finished projects, talks, or materials. Everything that led to them remains

invisible. As I started this Substack, I realized I want to share my background work too since it’s an

important part of what I do. It helps you understand how I approach my projects and, hopefully, gives

you new ideas. https://github.com/alexeygrigorev/telegram-writing-assistant/tree/master

https://github.com/alexeygrigorev/telegram-writing-assistant/tree/master using Claude Code agents. It

can process my raw voice notes, files, and text messages into structured articles and store them in a

GitHub repository. I want to explain how I put together the system, how it works, and how you can adapt

the same approach for your own workflow. Origin Story https://alexeyondata.substack.com/. Initial

Telegram chat where I dumped my ideas But it had one limitation: manual processing. Over time, my

Telegram became overloaded with voice notes that quickly piled up into a long, unstructured list of raw

materials. Some pieces belonged to the same topic. Others were partial thoughts, corrections, or

follow-ups. We had a lot of pending voice messages, files, and screenshots to process before publishing

a new edition of the newsletter. At some point, it was hard to categorize them and required

back-and-forth switching between voice messages, links, and files. That created additional friction for

content creation. Turning this stream into something structured required rereading, sorting, and

stitching everything together by hand. The result was slow and mentally expensive. The result is how I

started thinking about how to handle an incoming stream of background work so it can be organized and

transformed into pieces I could share publicly. How I Implemented the Telegram Assistant I had an

initial vision for how the assistant should work and decided to iterate on it using ChatGPT. Repo

structure suggested by ChatGPT https://github.com/alexeygrigorev/telegram-writing-assistant/blob/master/S

UMMARY.md file, which became the system specification. It was initially in Russian, but I translated it

into English for you. I usually use ChatGPT to refine my vision before starting any new project. It

helps me to better understand what I want to build and how I want to do it. Workflow suggested by

ChatGPT I didn’t want to implement the system described in summary.md myself. Instead, I asked the

Claude Code agent to follow that description and build it. The result produced the first working

version. Claude created a Telegram bot that lives in my chat and connected it to a GitHub repository

that stores the specification and all subsequent updates from the chat. I then tested the system by

using it as intended: sending messages and recording improvement ideas as voice notes, without leaving

the same workflow I was trying to optimize. Claude processed those messages and updated the system. Here

is what the final version looks like. How the Final Version Works Telegram Assistant follows this

workflow: 1. Capturing Telegram Chat All interaction starts in a Telegram chat. I send text messages,

voice notes, images, or files to



That is the part I would keep from this example: connect each tool to the problem that made it necessary, and keep the limitation next to the claim. The details matter because they explain what can be reused and what was specific to this project.
