# Moving the DataTalks FAQ into a Workflow

Since 2021, DataTalks.Club has launched new cohorts for free courses such as ML Zoomcamp, Data Engineering Zoomcamp, MLOps Zoomcamp and LLM Zoomcamp. Each cohort brings thousands of students into Slack. The same practical questions return about joining a course, setting up Windows, submitting homework or recovering from a broken step.

We started with a shared Google Docs FAQ for each course. Students could check whether a question had already been answered and add a new entry themselves. We even added one leaderboard point for a useful FAQ contribution. That incentive wasn't necessary for everyone, but it helped keep the document active.

The simple approach eventually stopped fitting. Open Google Docs had no real moderation, and vandalism happened more than once. Across the Zoomcamps, the FAQ grew to about 1,300 entries, with roughly 500 in the Data Engineering Zoomcamp FAQ. Questions covered the course, individual modules and particular homework assignments. Asking students to read the entire document before posting in Slack was no longer realistic.

## Alex Litvinov's retrieval bot

Community member Alex Litvinov built a RAG-powered Slack bot so students could ask questions where they were already working. The bot ingests more than the FAQ. It also uses past Slack discussions, GitHub course repositories and YouTube subtitles.

The ingestion pipeline runs daily with Prefect inside Docker. LlamaIndex handles chunking and embeddings, BAAI/bge-base-en-v1.5 provides the embeddings, and processed documents are stored in Zilliz Cloud. Cohere Rerank reranks results, while GPT-4o-mini generates answers. The stack also includes Slack Bolt, Upstash Redis, LangSmith and Fly.io.

The bot keeps a separate query engine for each course and uses the Slack channel ID to route questions. It retrieves 20 candidate documents and applies time weighting so newer Slack answers can take priority. It reranks the results to four before sending context to the model. That matters when answers depend on deadlines, cohort logistics or temporary instructions.

## My migration to Git

The bot made the FAQ easier to use, but Google Docs still caused maintenance problems. After the FAQ was vandalized again and Alex's bot encountered parsing issues, I moved the content into a Git repository and a dedicated static website.

I already had a notebook for parsing Google Docs. The pipeline downloads a document as DOCX, uses Python's `docx` module to extract content and detects question boundaries from document headings. It writes JSON records with fields such as text, section and question. The extracted content still needed cleanup. A script sent entries to GPT-4o to fix grammar, standardize formatting and turn code screenshots into actual code blocks.

I reorganized the cleaned content into course, module and question directories. Each FAQ entry became its own Markdown file with frontmatter containing its ID, question and sort order. This made questions easier to review, update and reorder under version control.

Jekyll was the obvious GitHub Pages choice, but it conflicted with dbt examples that use Jinja's double-curly-brace syntax. Jekyll's Liquid engine tried to interpret those expressions. I wrote a custom Python generator with help from GitHub Copilot. It reads Markdown, parses YAML frontmatter, renders Jinja2 templates and produces static HTML. The same generator exports JSON indexes that other tools can load into minsearch.

## Restore easy contributions

The Git repository improved moderation and reading, but it made contributions harder for students. Fred Pearce built the GitHub Actions orchestration around the FAQ Automation Bot. Students now submit a GitHub issue with a course, question and answer. The workflow retrieves similar FAQ entries, sends the proposal and section metadata to a model, and receives a structured decision.

The decision can be `NEW`, `UPDATE` or `DUPLICATE`. The workflow can prepare a pull request for a new or changed entry, while a duplicate can be closed with feedback. I still review the pull requests with Claude Code because the bot can select the wrong section or match a proposal to the wrong FAQ. The migration kept the source under version control while leaving a human in the loop for mistakes.
