# Building Books About Metals, Sirens and Conifers

My child asks for books about narrow subjects, and many of the books he wants either do not exist or are not written for children. The first request was about metals. He wanted chapters on palladium, tin, magnesium, titanium, beryllium, lithium and tungsten, with particular properties, history, extraction and uses. ChatGPT helped us make a table of contents, but its first generated chapter was very poor. ChatGPT alone was not enough.

I then gave the outline to a coding agent. The first version produced bullet points instead of normal narrative text. I tightened the prompt and managed the work through GitHub issues, reviewing one result before creating the next issue. Context limits caused another problem: when I asked for a rewrite of the whole book, the agent handled the first five chapters and stopped. I had to keep pushing it to finish.

At the same time, I asked the agent to automate a website so we could read the book in a browser. I added EPUB output later because I wanted to try it. The metals book required a lot of manual guidance, but my child liked the final version.

Halfway through the metals project, his interest narrowed to gallium, potassium and their unusual alloy. We made a separate book. By then I understood the workflow well enough to put the requirements into the first prompt. The result came out well on the first attempt, and the project took two GitHub issues: one for writing and one for EPUB and MOBI publishing.

The third book was about conifers, after he studied them at school. We discussed the topic with ChatGPT, built a plan, opened a GitHub issue and let Copilot work on it. By then, the process was routine.

After those books, I decided a general coding agent was not the best tool for narrative writing. I also wanted a concrete example for course participants who were learning to build specialized agents. I built a program to compare GPT, Claude and a newly released Gemini model. The evaluation was informal: I read the books with my child and chose the best text. Gemini produced the best result in that comparison.

The specialized generator uses a plan-then-execute workflow. We refine the table of contents in chat, convert it into a structured YAML plan and generate chapters from that plan while passing a compressed summary of earlier chapters. The system later handled books about warning sirens, fireworks and cable-driven mechanisms such as funiculars.

The generator now packages audio, EPUB and Amazon KDP artifacts. A fireworks example produced 21 chapters in about 45 minutes and cost roughly $4 with Gemini 3 Pro. I also tested the commercial side. The Amazon book I published sold zero copies over about five months, so producing publishing files did not establish demand.
