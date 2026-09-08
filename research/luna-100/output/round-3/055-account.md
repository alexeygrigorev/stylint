# Building Books for Narrow Questions

My child asks for books about narrow subjects, such as metals or warning sirens. Most of the time, those books don't exist, or they're not written for children. That led me to build a system for generating books at home.

The first request was a book about metals. He wanted to know what metals do and how people use them. His list included palladium, tin, magnesium, titanium and beryllium. It also included lithium and tungsten.

He also specified which properties to describe. ChatGPT suggested adding a few metals to complete the picture, and we planned one chapter per metal around history, extraction and uses.

We wanted to listen at bedtime, so I first asked ChatGPT to generate the book directly. We iterated on a table of contents and I asked for the first chapter, but the result was poor. ChatGPT alone wasn't enough for this kind of long narrative.

## Learning from the first books

I then used a coding agent. I gave it the finalized plan, created GitHub issues and reviewed the result before creating the next issue. The first version wrote bullet points instead of normal narrative text, probably because coding agents are tuned more toward documentation. I tightened the prompt and repeatedly asked for narrative writing.

Context limits created another problem. If I asked the agent to rewrite the entire book, it would rewrite the first five chapters and stop. I had to push it to finish the complete text. In parallel, I asked it to automate a website first, then added EPUB output because I wanted to try it. The metals book needed substantial manual guidance, but my child liked the final result.

Halfway through that project, my child became interested only in gallium, potassium and their unusual alloy. We made a second book about that subject. By then, I put the requirements directly in the first prompt, and the result came out well on the first attempt.

The project took two GitHub issues: one covered writing the book, and the other added EPUB and MOBI publishing.

A third book followed when he wanted to learn about conifers after studying them at school. The workflow was now familiar. We discussed the topic with ChatGPT, made a plan and created a GitHub issue. Copilot then worked on it.

## Building a specialized agent

After three books, I decided a general coding agent wasn't the best tool for narrative writing. I also needed a concrete example for my course participants, so I built a specialized book generator. I compared GPT, Claude and a newly released Gemini model informally by reading the books with my child. Gemini produced the best result in that comparison.

The generator uses a plan-then-execute workflow. We refine a table of contents in chat, convert it into a structured YAML plan and loop over the chapters. Each chapter receives a compressed summary of earlier chapters rather than the entire book. The system later handled books about warning sirens, fireworks and cable-driven mechanisms such as funiculars.

## Packaging and publishing

The generator produces audio, EPUB and Amazon KDP artifacts. A fireworks example created 21 chapters in about 45 minutes and cost roughly $4 using Gemini 3 Pro. That's an example run, not a fixed price. Model, book length, context, retries and optional steps all change the cost.

I also tested whether a generated book could be sold. The tested Amazon book had sold zero copies over about five months. Generating EPUB and print files proved that the pipeline could produce publishing artifacts, but it didn't prove demand. Market research, positioning, metadata, reviews and promotion are separate work.
