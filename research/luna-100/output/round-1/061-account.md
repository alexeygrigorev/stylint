# Why I built minsearch

Two years ago, while preparing the first LLM Zoomcamp, I needed to teach retrieval in notebooks. The examples used a few thousand documents, often in Google Colab with an open-source model on a GPU. Elasticsearch would have worked in production, but it needed a server, Docker, configuration, and operational explanations that were unrelated to the lesson. I wanted everything to run in one Python process.

I built minsearch as the smallest library that fit that situation. The first version was one Python file with an `Index` class and a bag-of-words TF-IDF implementation. It vectorized each text field, transformed the query, calculated scores, added field scores, and sorted the documents.

Course FAQs made the requirements concrete. A document had a question, answer, section, course, and metadata. A match in the question should count more than a match in the answer, and sometimes the search needed to be limited to one course. Field boosting and keyword filters made the tiny implementation useful without hiding the retrieval logic from learners.

At first, people downloaded the file. That became inconvenient whenever I fixed a bug or added a feature. Participants had to use `wget` again. I packaged minsearch and published it on PyPI, so it could be installed with `uv` or `pip`. It started at version 0.0.1 and reached 0.1.0 at the time of the article.

I use it in LLM Zoomcamp, AI Hero, and AI Engineering Buildcamp, as well as personal and DataTalks.Club projects. The FAQ automation loads its entries, indexes them, and checks whether a proposed question already exists before creating a new one.

When the second Zoomcamp added agents, I needed an index that could be changed during a conversation. `AppendableIndex` kept the same fit and search interface but allowed documents to be added one at a time. I later added `VectorSearch` for cosine similarity over precomputed embeddings. The library now has those three index types, common keyword, numeric, and date filters, and highlighting that shows matching snippets before an agent opens a full document.

The appendable index eventually became slow. A benchmark showed it was 14 times slower to index and 27 times slower to search than the simple implementation. Claude helped identify repeated token and score computation. I gave it a loop: save a baseline on Simple Wikipedia, change code, check that results still matched, and compare speed. After several rounds, the optimized appendable search was 20 to 76 times faster than the scikit-learn index on the benchmark.

Minsearch is for small or medium collections, notebooks, prototypes, and a few thousand documents. Its sweet spot is up to about 10,000. Larger local datasets may fit SQLiteSearch, while bigger systems need a real search engine or vector database.
