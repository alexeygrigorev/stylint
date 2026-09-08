# Rebuilding the DataTalks.Club FAQ Assistant

A simpler search engine and a small packaged index are reasonable because the community can correct an occasional answer in Slack.

The DataTalks.Club FAQ assistant helps students find answers in course material. I wanted to run it in the same AWS infrastructure as Au-Tomator, our Slack management bot, rather than keep maintaining a separate deployment. The existing ZoomcampQABot worked, but it used Fly.io, Milvus on Zilliz Cloud, Cohere reranking, HuggingFace embeddings, Redis caching, and several ingestion jobs. It was difficult to move that setup into a lean serverless environment.

The first part of the system is the FAQ dataset. It began in Google Docs, which was convenient but could be vandalized and was awkward to curate with AI. I moved the records into Markdown in the DataTalksClub/faq repository. Questions come from GitHub contributions, useful Slack discussions, and transcripts from live YouTube sessions. GitHub Actions indexes the dataset and uses search plus OpenAI to classify contributions as NEW, UPDATE, DUPLICATE, or WRONG_COURSE.

I also needed a way to know whether the classifier was improving. The evaluation set came from cases where I had corrected the automation. WRONG_COURSE and DUPLICATE errors are especially important because those issues close without creating a pull request. Historical NEW examples require leave-one-out evaluation: remove the record from the dataset before testing it, otherwise the system will correctly see it as a duplicate. The current set contains 61 cases across the four decisions.

For the serverless assistant, I removed the vector database and the direct indexing of Slack and YouTube. That information already enters the curated FAQ. I replaced minsearch with zerosearch, a pure-Python search library without the scientific dependencies that exceed Lambda’s 50 MB direct-upload limit. I also removed Pydantic and requests so OpenAI calls use the standard library. The full index is about 8 MB.

The index is rebuilt whenever the FAQ repository changes. This is different from the daily cron approach used by the old bot, but it means data updates reach Lambda quickly. The assistant also searches DataTalks.Club documentation and course repository Markdown, combining all three sources into one packaged index.

I built retrieval evaluation from 9,900 Slack threads and selected 130 questions across three courses. For each question I marked the correct documents and measured hit rate and MRR at k=1, 3, and 5. Query rewriting works best when it keeps exact error messages, tool names, commands, and filenames while turning the rest into keywords.

Au-Tomator now routes mentions and the `:faq:` reaction to a third Lambda. The assistant rewrites the question, searches the index, and generates an answer, while Au-Tomator acknowledges Slack and posts the response. Incorrect or incomplete answers become evaluation cases and often lead to a better FAQ record. The data loop matters more than adding another component to the stack.
