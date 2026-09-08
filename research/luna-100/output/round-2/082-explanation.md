# A FAQ Assistant Begins with Curation

An FAQ assistant connects curation with retrieval. One part curates a dataset from student contributions, Slack discussions, and YouTube transcripts.

The other retrieves records from that dataset and answers questions in Slack. The quality of the second part depends heavily on the first.

DataTalks.Club accepts a GitHub issue with a question, course, and proposed answer. A GitHub Actions workflow indexes the existing records with minsearch. It searches the question alone. It then searches the combined question and answer, combining both rankings with reciprocal rank fusion.

OpenAI classifies the issue as `NEW`, `UPDATE`, `DUPLICATE`, or `WRONG_COURSE`. New and updated records become pull requests, while duplicates and wrong-course submissions are closed.

Those decisions have different costs when they're wrong. A mistaken `NEW` or `UPDATE` can still produce a pull request for review. A mistaken `DUPLICATE` or `WRONG_COURSE` closes the issue before anyone can examine it. I therefore gave the more expensive mistakes more weight in the evaluation set.

Historical evaluation needs another precaution. The dataset keeps changing, so a record that was once classified as `NEW` may already be present when I replay the case. The system would then find the record and call it a duplicate.

Leave-one-out evaluation removes the record being tested and runs the case against the remaining records. That preserves the situation in which the original decision was made.

The retrieval system also changed because of its deployment environment. The original bot used embeddings, Milvus, reranking, and several supporting services. I wanted a leaner AWS Lambda deployment, and minsearch brought scientific Python dependencies that were too large for Lambda's direct upload limit.

I replaced minsearch with zerosearch, a pure-Python search engine. I also removed Pydantic and requests, then used the standard library for HTTP calls. The rebuilt index is about 8 MB.

To measure retrieval, I started with a real Slack dump containing 9,900 threads. I filtered it to 130 questions from three courses.

The set had 60 questions from Data Engineering Zoomcamp, 40 from Stock Markets Analytics, and 30 from AI Dev Tools.

I marked the correct documents, then measured hit rate and MRR at several values of k. Query rewriting worked best when it produced keywords while keeping exact error messages, commands, tool names, and filenames.

Generation needs a separate evaluation. When someone corrects a bot answer or adds missing information in Slack, that interaction becomes evidence that the answer was incomplete or wrong. The first repair is often a FAQ record update rather than a prompt change.

I check whether retrieval missed a record or whether the record lacks the needed information. Then I rerun the evaluation and deploy the new index.

The assistant now combines the FAQ, documentation, and course repository Markdown in one zerosearch index. A mention or `:faq:` reaction travels through Au-Tomator to the Lambda, which rewrites the question, searches the index, and generates an answer.

Corrections from users feed back into curation. That keeps the data work visible instead of hiding it behind a more complicated retrieval stack.
