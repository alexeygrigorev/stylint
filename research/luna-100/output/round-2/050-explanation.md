# From a Google Doc to an FAQ Workflow

At DataTalks.Club, each new course cohort brings repeated questions into Slack. Students ask whether they can still join, how to set up Windows, where to submit homework and what to do when a step breaks. The first response was a shared Google Docs FAQ. It was easy to read and easy for students to edit, but the document grew beyond what a single file could support.

Across the Zoomcamps, the FAQ reached about 1,300 entries, including roughly 500 in the Data Engineering Zoomcamp FAQ. Students needed answers about an entire course, a module or a particular homework assignment. Asking them to read the whole document before posting in Slack was no longer realistic.

## Add retrieval to Slack

Community member Alex Litvinov built a RAG-powered Slack bot to bring the FAQ into the conversation. The bot doesn't use the FAQ alone. It ingests question-and-answer entries, past Slack discussions, GitHub course repositories and YouTube subtitles.

Each source is chunked according to its structure, so an FAQ entry stays a question-answer pair. A Slack thread stays together as the original question and discussion, while GitHub content is organized by file.

A daily Prefect pipeline runs in Docker, where LlamaIndex handles chunking and embeddings. BAAI/bge-base-en-v1.5 produces embeddings, and the processed documents go to Zilliz Cloud. The wider stack includes Cohere Rerank, GPT-4o-mini and Slack Bolt. It also uses Upstash Redis, LangSmith and Fly.io.

The bot keeps a separate query engine for each course and routes questions using the Slack channel ID. It retrieves 20 candidate documents, applies time weighting for newer Slack answers and reranks the result to four documents before sending context to the model. This matters when an answer depends on a deadline, cohort logistics or a temporary instruction.

## Move the canonical version

The Slack bot made the FAQ easier to use, but Google Docs still had moderation and maintenance problems. After another vandalism incident and parsing issues in Alex's bot, I moved the FAQ into a Git repository and a static website.

The migration downloaded each Google Doc as DOCX and used Python's `docx` module to extract headings and answers. It then wrote JSON records containing fields such as text, section and question. The extracted material still needed cleanup, so a script sent entries to GPT-4o to fix grammar, standardize formatting and turn code screenshots into code blocks.

I reorganized the result into course, module and question directories. Each entry became a Markdown file with frontmatter containing its ID, question and sort order, while the body held the answer. This structure made individual questions easier to review, update and reorder under version control.

## Generate HTML and JSON

Jekyll was the obvious GitHub Pages choice, but it conflicted with dbt examples that used Jinja's double-curly-brace syntax. Jekyll's Liquid engine tried to interpret the same expressions. Rather than keep escaping those examples, I built a custom Python generator with help from GitHub Copilot.

The generator reads Markdown, parses YAML frontmatter, converts the content to HTML and renders Jinja2 templates. It also exports `courses.json` and a JSON file per course, so other tools can load the FAQ into minsearch. That made the website a readable interface and a structured dataset.

## Reopen contributions with automation

Git made maintenance safer, but contributions became harder than editing a shared document. Fred Pearce built the GitHub Actions workflow around the FAQ Automation Bot. A student submits a course, question and answer through an issue. The workflow retrieves similar entries, sends the proposal and section metadata to a model, then returns a structured decision.

The decision can be `NEW`, `UPDATE` or `DUPLICATE`. It can also identify the section, order and proposed content. The workflow then opens a pull request or closes a duplicate issue.

I still review the pull requests with Claude Code. The bot can put a question in the wrong section or match it to the wrong FAQ. The workflow restores easy contribution while keeping human review in the loop.
