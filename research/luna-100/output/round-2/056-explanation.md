# A Plan-First Pipeline for Generated Books

A book generator is easier to control when planning and execution are separate. I use an interactive Streamlit step to decide what the book should contain, then convert that discussion into a structured YAML plan. Writing, audio generation and publishing all consume the same plan instead of relying on one long conversation.

## Refine the outline first

Start the interface with `make ui`, then enter a topic and choose a size such as Small, Medium or Large. Gemini 3 Pro Preview streams a draft outline into the Streamlit chat. You can send feedback, and each refinement call receives the current plan together with the new request. Gemini updates the existing outline rather than starting from nothing.

When the outline is ready, click `Ready - Create Structured Plan`. A command-line alternative can build the plan from a text file with `uv run python -m chapter_based.plan -p books/mybook/input.txt`. The important boundary is that freeform discussion ends before chapter generation begins.

The next step sends the finalized outline to Gemini and requests JSON with an application/json response type and a schema generated from the Pydantic `BookPlan` model. The structured output is saved as `books/<slug>/plan.yaml`. It contains the book name and language, plus parts, chapters, introductions and bullet points.

`plan.yaml` connects planning with the later steps. Writing scripts use its chapter specifications, publishing scripts use its metadata and structure, and the cover pipeline uses its back-cover text. Because each step reads the same file, the planning interface can change without requiring a rewrite of the execution pipeline.

## Generate chapters from specifications

Once `plan.yaml` exists, the writing scripts no longer need the chat history. The chapter-based command is `uv run python -m chapter_based.execute mybook`, with `make generate-book` available through the Makefile. The repository also has a section-based implementation for longer books, but the chapter-based path makes the workflow easier to see.

The execution script flattens the parts into a list of chapter specifications. For each chapter, it builds a progress marker: completed chapters receive `[x]`, the current chapter receives an arrow and remaining chapters receive `[ ]`. Gemini receives that outline and the current chapter's bullet points. It doesn't receive the full text of earlier chapters. Cohesion comes from the plan rather than passing the entire book through every call.

That design makes the initial outline significant. It needs enough structure to keep chapters aligned, while the progress markers show the model where the current chapter sits in the whole book. Existing chapter files are skipped on reruns, so an interrupted generation can continue without regenerating completed work. A `_ready` sentinel marks a completed book.

## Produce the remaining artifacts

After Markdown chapters exist, the same folder can generate audio. `make tts BOOK=...` calls Gemini text-to-speech with `models/gemini-2.5-flash-preview-tts` and the default `Charon` voice. The script wraps PCM audio in WAV files and uploads them to S3. A separate ffmpeg script creates MP3 files.

Publishing scripts also read the Markdown and `plan.yaml`. `make ebook BOOK=...` creates an EPUB with Pandoc, while `make kdp-interior BOOK=...` renders a print PDF through XeLaTeX in Docker. `make kdp-cover BOOK=...` creates a wraparound cover with ReportLab. These files make a book package, but they don't guarantee sales.

The generator tracks cost while planning and writing. A fireworks example produced 21 chapters in about 45 minutes and cost roughly $4 using Gemini 3 Pro. The exact amount depends on model, context, retries and optional steps. The pipeline's predictable paths, existence checks and ready sentinel make generation resumable, while the publishing artifacts remain separate from the commercial result.
