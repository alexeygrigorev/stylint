# Moving an FAQ out of Google Docs

DataTalks.Club has run free courses since 2021, and each cohort brings the same practical questions into Slack. Students ask how to join, configure Windows, submit homework, or recover from an error. We started with a shared Google Docs FAQ because it was easy for anyone to read and add an answer.

The document worked for a while. We even gave a small leaderboard incentive for useful FAQ contributions. But an open document was difficult to moderate, and vandalism happened more than once. The collection also grew to around 1,300 entries across the Zoomcamps. The Data Engineering FAQ alone reached roughly 500 entries, covering course-wide questions, modules, and individual homework.

Alex Litvinov built a Slack bot to make retrieval easier. It could answer in the channel instead of asking students to search a large document. The bot combines FAQ entries with Slack history, GitHub repositories, and YouTube subtitles. Its ingestion runs daily with Prefect in Docker. LlamaIndex handles chunking and embeddings, Zilliz Cloud stores the processed data, Cohere reranks results, and GPT-4o-mini writes the answer. It retrieves 20 candidates, accounts for the age of Slack answers, and passes the best four to the model.

The bot improved access, but Google Docs remained the source of truth. After another vandalism incident and parsing problems, I decided to move the FAQ into Git. I already had a notebook that downloaded a document as DOCX, used Python’s `docx` module, and identified questions and answers from headings. GPT-4o then cleaned grammar, formatting, and code screenshots.

The new repository stores one Markdown file per question. Frontmatter contains the ID, question, and sort order, while folders separate courses and modules. Jekyll did not work because it tried to interpret dbt’s Jinja expressions as Liquid templates. I wrote a Python generator instead. It reads the files, renders them with Jinja2, copies assets, and creates static HTML for GitHub Pages. It also exports JSON indexes, which makes the FAQ available to minsearch and other consumers.

The Git repository made reading and moderation better, but contributions became more difficult. Students now needed to fork, edit Markdown, and open a pull request. The FAQ Automation Bot gives them a simpler issue form with course, question, and answer fields. It retrieves similar entries, asks a lightweight model to decide whether the proposal is new, an update, or a duplicate, and opens a pull request when needed.

The bot is not trusted to merge by itself. I batch its pull requests and use Claude Code to move entries to the right section, merge duplicates, or correct the selected target. Fred Pearce added the GitHub Actions workflow, issue template, helpers, CLI, tests, and documentation that made the original notebook usable for the community. The FAQ became a website, a dataset, and a controlled contribution workflow, one constraint at a time.
