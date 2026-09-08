## One Idea I Want to Share This Week

The second cohort of my [AI Bootcamp](https://maven.com/alexey-grigorev/from-rag-to-agents) starts soon, and I recently opened a scholarship program for motivated students who do not have the budget for a paid program.


This time, I received 2,500+ applications, far more than the number of available spots. The application form is now closed, and I have already contacted the selected full-scholarship participants. If you did not hear from me, you were not chosen for this round.

For those applying for partial scholarships, I am still reviewing applications and will reach out to selected candidates by next Monday.

### Thank You for Your Strong Submissions

Thank you to everyone who applied. I genuinely appreciated the time and thought many of you put into your submissions. There were many strong applications, but due to the volume, it was not possible to respond to everyone individually. If you invested effort in your application but were not selected, please do not take this as a negative signal.

If you were not selected, I still strongly encourage you to keep learning and building. There is a large amount of free material available:

* **[AI Agents Email Crash-Course (Cohort Edition)](https://alexeygrigorev.com/aihero/):** I’m running a free cohort-based version of the AI Agents Email Crash-Course this January. To complete the cohort, you’ll finish the project and review three other submissions; in return, you’ll receive a certificate of completion signed by me.
* **[LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp):** a free online course about real-life applications of LLMs. In 10 weeks, you will learn how to build an AI system that answers questions about your knowledge base.
* **Free tutorials:** recordings on [DataTalksClub](https://www.youtube.com/@DataTalksClub) and my personal [YouTube channel](https://www.youtube.com/@stolzenable).

> As a reminder, you can also unlock a curated list of workshops by inviting three friends.
>
> [My newsletter now has a referral program. Invite your friends and get exclusive rewards!](https://alexeyondata.substack.com/p/my-newsletter-now-has-a-referral)

On this Substack, I regularly share high-quality resources, tools, and learning opportunities, many of which are free.

[Alexey On DataI write about data from a practical angle: tools I'm experimenting with, systems and projects I'm building, and patterns that work in real setups.By Alexey Grigorev](https://alexeyondata.substack.com?utm_source=substack&utm_campaign=publication_embed&utm_medium=web)

If you are not subscribed yet, consider subscribing to stay up to date with new resources and future programs.

To make the scholarship selection process more transparent, I want to share some context on how I approach it. This should also help if you plan to apply in the future.

### Selection Process

The scholarship is designed for people who are already doing meaningful work and want to use this training to scale existing impact. It is not intended for beginners or general career exploration. No prior AI experience is required, but there must be a clear connection between what you are currently building and why this bootcamp is relevant at this stage.


Core requirements for candidate selection for the AI Bootcamp scholarship

The first and most important signal is motivation. Applications with empty, one-line, or generic responses are filtered out early, as are submissions focused purely on job-seeking, learning tools in isolation, or short-term income goals.


Strong applications clearly describe a specific problem, explain who benefits from solving it, and show why this training matters now.


Beyond motivation, I look for depth and alignment. This includes whether the applicant understands what the bootcamp actually teaches, how it connects to their current work, and why production-focused training is needed. Clear plans to scale an existing project, reach a community, or multiply impact stand out far more than abstract learning goals.


Because the program is demanding, the likelihood of completion is also critical. I pay close attention to signals that suggest an applicant can realistically commit the time and follow through, such as prior long-term projects, concrete plans, or existing accountability structures.

Not being selected does not mean an application was weak. In many cases, it reflects a mismatch between the scholarship’s intent and the applicant’s current situation, or simply the fact that competition exceeded the available spots.

#### Automation with Claude Code

With 2,500+ applications, reviewing every submission manually was not feasible. My evaluation process combined AI-assisted filtering with personal review at the final stage.

First, all applications underwent an AI-assisted preliminary review using Claude Code. I defined the evaluation logic in detail using custom slash commands and then validated the outputs myself. This step was used to rank applications and filter out those that clearly did not match the scholarship’s intent.


A key advantage of Claude Code here was the ability to run multiple commands in parallel via sub-agents, which made it possible to process large batches efficiently while keeping the logic consistent.


Claude’s ability to run multiple commands in parallel using sub-agents

Instead of building a custom agent in code, I relied on clear instructions, a strong model, and reusable command-based workflows defined in Markdown. This significantly reduced overhead without sacrificing control.

From this first pass, I selected the top 50 applications for manual review. These were reviewed personally, with applications shuffled to reduce bias. I read each submission in full, checked linked profiles or projects where provided, and verified that the AI-generated scores actually matched the substance of the application. At this stage, qualitative factors such as authenticity, clarity of intent, and likelihood of follow-through mattered more than any numeric score.


This approach allowed me to handle the scale of applications while still giving serious candidates proper attention.

If you plan to apply again, start building something concrete and meaningful now. Even if you aren’t selected for this cohort, keep building and learning with the resources available. Proactivity and having a clear goal will help you find a way to achieve it, given your current circumstances. It will also help you stand out.

Experience with real projects, persistence, and learning in public matter much more than any single opportunity.

## My Experiment: Turning Videos Into Articles With AI

This week, I also worked on the new documentation website for DataTalksClub’s free courses.

With every new cohort launch, I end up repeating the same organizational details during the live stream over and over again. This time is better spent on meaningful discussions and answering participant questions. That’s why I wanted to centralize all important information in one place and share a single link with everyone.

I started with Data Engineering Zoomcamp, since the new cohort has just launched on Monday. The content covered during the launch stream is largely the same every year, and I already had recordings from previous launches. So, instead of rewriting everything manually, I used the latest stream as input to automatically generate [structured, illustrated documentation](https://datatalks.club/docs/courses/data-engineering-zoomcamp/).

For this, I used Claude Code again. After some experiments, I ended up implementing two custom commands:

* [/article](https://github.com/DataTalksClub/docs/blob/main/.claude/commands/article.md) converts the transcript into a structured article and suggests where illustrations are needed
* [/extract-illustrations](https://github.com/DataTalksClub/docs/blob/main/.claude/skills/extract-illustrations/SKILL.md) extracts candidate screenshots directly from the video


This worked quite well for creating the article, but not great for illustrations. Even though only 50% of suggested images were good, it saved a lot of time.

But it also changes the way I can now approach automating my tasks. Previously, I’d have to create an agent from scratch: create a Python script, think of tools for this agent, and make calls to OpenAI. Now I describe what I want to do to Claude, iterate on the output until I like it. When it’s done, I ask it to summarize all the actions into a command or skill and correct it. That’s it. Now it’s reusable.

### Better Screenshots with Playwright

I still needed illustrations that I couldn’t extract automatically from the video. To get them, I used [Playwright](https://github.com/microsoft/playwright) - a browser automation tool. I mean, Claude used. I asked it to go to the relevant pages and take screenshots directly from the site.


It opened the website, took screenshots, saved the files in the right location, and included the images in the docs. At the end I only needed to crop these images.

### Exploring GitHub Repos with gh CLI

I also needed to [describe the course repository](https://datatalks.club/docs/courses/data-engineering-zoomcamp/resources/github/). So I told Claude to use the GitHub CLI to look at it, and after a few iterations, it found relevant sections and produced a structured documentation page.


This approach worked well for turning existing repositories into readable reference documentation with minimal manual effort.

Overall, using Claude Code significantly simplified the documentation process. I still spent around 4-5 hours reviewing, editing, and polishing the output, so it is not fully automated. However, without AI assistance, this work would typically take close to two full days. In practice, this reduced the time required by roughly a factor of four.

### Voice dictation

One more thing that helped a lot in this workflow is voice dictation. I often review drafts visually and give feedback to Claude via voice input. On Windows, I use the built-in speech recognition (Win + H), dictate edits, let Claude apply them, then iterate again. This makes editing and refinement much faster, especially for longer texts.


This setup is still evolving, but even in its current form, it has already changed how I approach documentation and content reuse for course launches.
