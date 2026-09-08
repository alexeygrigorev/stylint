# Building books for very specific questions

My child asks for books about narrow topics. He wanted to understand metals and then asked about signal sirens, but books for children on those subjects were hard to find. I started with an experiment in ChatGPT and eventually built an automated pipeline that plans, writes, formats, and packages books.

The first request was a metals book covering palladium, tin, magnesium, titanium, beryllium, lithium, and tungsten. We planned one chapter per metal, including history, extraction, and uses. ChatGPT helped make the table of contents, but its first chapter was poor. I then gave the outline to a coding agent. Its first version produced bullet points, so I changed the prompt to request ordinary prose and worked through the book with GitHub issues and reviews.

Context limits caused another problem. A request to rewrite the complete book stopped after a few chapters. I had to ask the agent repeatedly to continue. I also asked it to automate a website and later EPUB output. The text needed a lot of manual guidance, but my child liked the final book.

The next book was about a gallium and potassium alloy. By then the workflow was clearer, so the project took only two issues: one for writing and one for EPUB and MOBI. A third book covered conifers after my child studied them at school. We discussed the topic with ChatGPT, made a plan, opened an issue, and let Copilot generate the book.

After that I built a specialized book generator. I wanted a better fit for narrative writing and a project to show course participants. I compared GPT, Claude, and Gemini informally by reading the results with my child. Gemini produced the best text in those experiments. The system now separates planning from execution. A chat produces an outline, the outline becomes typed YAML, and a loop generates chapters from each specification while using a compressed progress summary.

The generator has a Streamlit planning interface and command-line alternatives. A `BookPlan` model defines chapters, sections, and bullet points. `plan.yaml` becomes the contract for writing, audio, cover text, EPUB, and KDP files. Chapter files are skipped when they already exist, and a ready marker prevents changes to completed books.

The pipeline also produces audio, EPUB, interior PDFs, and cover PDFs. A fireworks example produced 21 chapters in about 45 minutes and cost roughly $4 with Gemini 3 Pro. Those figures depend on book size, retries, context, and optional steps. The publishing experiment made the limitation clear: a technical pipeline can generate a book package, but it cannot create demand. One generated book had been on Amazon for about five months and had sold zero copies.

The project remains useful for its original purpose. It makes it possible to answer a narrow question with a book a child can read or listen to, and it also gives me a concrete way to study planning, generation, formatting, and publishing as one workflow.
