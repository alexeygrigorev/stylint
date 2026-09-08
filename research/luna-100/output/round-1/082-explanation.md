# Keep the Data Better Than the Model

The source is deliberately drawn from community questions rather than an artificial benchmark. That matters because the assistant is meant to help people in the courses, and their corrections reveal where both retrieval and the underlying records need work.

It also keeps the evaluation connected to actual use.

An FAQ assistant can look like a search and generation problem, but the quality of the answers depends first on the data. The DataTalks.Club system turns GitHub issues, useful Slack discussions, and YouTube transcripts into reviewed FAQ records, then uses those records to answer questions in Slack.

The curation path starts with a contribution. Someone submits a GitHub issue containing a question, course, and answer. A workflow indexes the existing records with minsearch, searches both the question and the combined question-answer text, and merges the rankings. OpenAI then classifies the issue as NEW, UPDATE, DUPLICATE, or WRONG_COURSE. New and updated records become pull requests; duplicates and wrong-course items are closed.

Evaluation is necessary because a classification mistake can have different costs. A wrong NEW decision is easy to repair after a pull request appears. A wrong DUPLICATE or WRONG_COURSE decision closes the issue before anyone reviews it. The evaluation set therefore gives those cases more weight. Historical records also require leave-one-out testing: remove the record being tested, otherwise a former NEW example will now be found in the dataset as a duplicate.

The assistant does not need every retrieval component. The original bot used embeddings, Milvus, reranking, and several services. For AWS Lambda, a lighter design was more useful. Scientific Python dependencies were too large for the direct upload limit, so zerosearch replaced minsearch. Pydantic and requests were removed, and standard-library HTTP calls reduced packaging concerns. The index is rebuilt with the FAQ repository and is about 8 MB.

Search quality can be measured with real questions. A Slack dump produced 9,900 threads, filtered to 130 questions from three courses. Each question received correct documents, and retrieval was measured with hit rate and MRR at several values of k. Query rewriting works best when it turns ordinary text into keywords but keeps exact error messages, commands, tool names, and filenames.

Generation needs its own evaluation. Corrections and additions in Slack are evidence that an answer was incomplete or wrong. Instead of only changing a prompt, inspect why the record was not retrieved or why the FAQ entry lacked the answer. Update the record, rerun the evaluation, and deploy the new index.

This feedback loop makes a simpler architecture reasonable. A mention or `:faq:` reaction goes through Au-Tomator to the Lambda, which rewrites, searches, and generates. Bad answers become data improvements, so curation remains part of operating the assistant.
