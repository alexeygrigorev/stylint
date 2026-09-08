# Rebuilding the DataTalks.Club FAQ Assistant

The DataTalks.Club FAQ assistant helps students find answers in course material. I wanted to run it in the same AWS infrastructure as Au-Tomator, our Slack management bot, instead of maintaining a separate deployment. The existing `ZoomcampQABot` was developed by Alex Litvinov and worked well enough.

It used Fly.io and Milvus on Zilliz Cloud. It also used Cohere reranking, HuggingFace embeddings, Redis caching, and several ingestion jobs. Moving that setup into a lean serverless environment would be difficult.

The old bot also depended on Alex's OpenAI account. When it ran out of money, the bot stopped and I had to ask him to fix it. I felt bad that he was paying for the project, so I offered to take it over and run it in DataTalks.Club infrastructure. He agreed this time.

I started with the FAQ dataset. It used to live in Google Docs, which was convenient but frequently vandalized. I had to roll the documents back manually, and using AI to curate Google Docs was awkward.

I moved the records into Markdown files in the `DataTalksClub/faq` repository. Questions now come from GitHub contributions, useful Slack discussions, and transcripts from live YouTube sessions.

The curation workflow starts with a GitHub issue containing a question, course, and answer. GitHub Actions indexes the dataset with minsearch. It searches once using the question and once using the question plus answer, then combines the results with reciprocal rank fusion.

OpenAI returns one of four decisions: `NEW`, `UPDATE`, `DUPLICATE`, or `WRONG_COURSE`. A new or updated record becomes a pull request, while a duplicate or wrong-course issue is closed.

I needed an evaluation set because incorrect decisions increased as more people used the automation, so I collected cases where I had corrected the result. `DUPLICATE` and `WRONG_COURSE` errors matter more because the issue closes without creating a pull request. No later review follows.

Historical `NEW` cases require leave-one-out evaluation, so the record must be removed before testing. Otherwise the system sees it in the dataset and calls it a duplicate. The current set has 61 cases across the four decisions.

For the serverless assistant, I removed direct indexing of Slack and YouTube because that information already enters the curated FAQ. I also removed the vector database. It could improve retrieval, but I wanted a lean setup. An occasional wrong answer could be corrected in Slack by me or another community member.

The deployment constraint led me from minsearch to zerosearch, a pure-Python search library without the scientific dependencies that exceed Lambda's 50 MB direct-upload limit. I removed Pydantic and requests. OpenAI calls use the standard library.

The index is rebuilt whenever the FAQ repository changes and deployed with the Lambda. It's about 8 MB.

I evaluated retrieval using 9,900 Slack threads and selected 130 questions from three courses. For each question, I marked the correct documents. Then I measured hit rate and MRR at k=1, 3, and 5. Query rewriting worked best when it turned a Slack message into keywords while preserving exact error messages, tool names, commands, and filenames.

Au-Tomator now routes mentions and the `:faq:` reaction to a third Lambda. The FAQ assistant rewrites the question, searches the combined index, and generates the answer. The index includes the FAQ, DataTalks.Club documentation, and course-repository Markdown. Wrong or incomplete answers become evaluation cases and often lead to a better FAQ record. The next index then contains the correction.
