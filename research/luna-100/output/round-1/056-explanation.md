# A plan-first pipeline for generating books

Book generation works better when the structure is decided before prose is produced. The pipeline I built separates an interactive planning stage from chapter execution and publishing. That separation came after direct ChatGPT generation and general coding agents produced weak or incomplete narrative text.

Start in the Streamlit interface with a topic and a size such as Small, Medium, or Large. Gemini 3 Pro Preview proposes an outline. You can refine it in the chat, and each refinement updates the current plan instead of starting over. When the outline is ready, the interface converts it into a structured plan. A command-line path can build the plan from an input file.

The structured plan is generated as JSON using a Pydantic `BookPlan` schema and saved as `plan.yaml`. It contains the book name, slug, language, parts, chapters, introductions, and bullet points. This file is the contract for the rest of the system. Writing scripts use it for chapter order, publishing scripts use it for metadata, and the cover process uses it for back-cover text. The planning interface can change as long as it still produces the same structure.

Execution works chapter by chapter. The chapter-based implementation flattens the plan and gives the model the current chapter specification plus a progress view. Completed chapters are marked, the current chapter is highlighted, and future chapters remain pending. The model does not receive all previous prose. Cohesion comes from the upfront plan and compressed progress information, which keeps context smaller.

The repository has both section-based and chapter-based generators. The section path makes more model calls and provides finer control for longer books. The chapter path typically produces 3,000 to 5,000 words per chapter in one call. Outputs are saved under predictable paths such as `books/<slug>/part_01/01_chapter.md`.

The pipeline is resumable. It checks whether each chapter or artifact already exists before regenerating it. A `_ready` file marks a completed book. The same folder stores the plan, chapters, cover, audio, EPUB, and KDP PDFs, so an interrupted run can continue with missing pieces rather than starting again. The Makefile connects planning, generation, text-to-speech, ebook creation, and print files.

Cost is visible during the process. A tracker reports incremental usage in the interface and terminal, and a fireworks example took about 45 minutes and cost roughly $4 with Gemini 3 Pro. That is an example, not a fixed price. Quality, book length, context, retries, and optional assets change the result.

Publishing requires another boundary. EPUB, interior, and cover files solve formatting, but they do not solve audience demand. A book can be generated and uploaded to Amazon without selling. Market research, positioning, metadata, reviews, and promotion remain separate work from the generation pipeline.
