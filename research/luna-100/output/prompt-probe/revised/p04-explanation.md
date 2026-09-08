# A Plan-First Pipeline for AI-Generated Books

A book generator becomes easier to control when planning is separate from writing. The pipeline starts with an interactive outline in Streamlit. It converts that outline into a typed YAML plan and uses the same plan for chapters, audio and publishing. The later stages all read the same plan.

Start the planning interface with `make ui`. Enter a topic and select a size such as Small, Medium or Large. Gemini 3 Pro Preview streams a draft book plan into the chat. You can refine it through conversation because each request receives the current plan and your new feedback. When the outline is ready, click `Ready - Create Structured Plan`.

The system sends the finalized outline to Gemini again and requests JSON with a schema generated from the Pydantic `BookPlan` model. It saves the structured result as `books/<slug>/plan.yaml`. The file describes the book language and parts. It also contains chapters, introductions and bullet points. Writing scripts use the chapter specifications, while publishing and cover scripts use the metadata and structure.

Once the plan exists, chapter generation no longer needs the chat history. The command-line entry point is `uv run python -m chapter_based.execute mybook`, with `make generate-book` as a Makefile alternative. The repository includes section-based and chapter-based implementations. The chapter-based script flattens parts into chapter specifications and generates one chapter at a time.

For each chapter, the script builds progress markers. The script marks completed chapters with `[x]`, the current chapter with an arrow and future chapters with `[ ]`. Gemini receives the progress outline and the current chapter's bullet points, but not the full text of earlier chapters. Cohesion comes from the initial plan. Existing chapter files are skipped on reruns, and a `_ready` sentinel marks a completed book.

The same book folder can produce audio after the Markdown chapters exist. `make tts BOOK=...` uses Gemini text-to-speech with `models/gemini-2.5-flash-preview-tts` and the default `Charon` voice. The script wraps PCM output in WAV files, uploads them to S3 and can create MP3 derivatives with ffmpeg.

Publishing uses the Markdown and the same `plan.yaml`, and `make ebook BOOK=...` creates an EPUB with Pandoc. KDP commands create an interior PDF through XeLaTeX in Docker and a wraparound cover through ReportLab. The output gives you a package of files, but it doesn't show whether a book will sell.

The generator tracks cost during planning and writing, writes artifacts to predictable paths and skips files that already exist. A fireworks run produced 21 chapters in about 45 minutes and cost roughly $4 with Gemini 3 Pro. That's an example rather than a fixed estimate because context, retries, model choice and optional steps change the cost. The ready sentinel and existence checks let an interrupted run continue from missing artifacts.
