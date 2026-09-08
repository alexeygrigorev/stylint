# When a small search library is enough

A workshop about retrieval should let participants see the complete path from documents to results. Elasticsearch is powerful, but requiring a server, Docker, and configuration can move attention away from the lesson. Minsearch is a small in-process Python library designed for notebooks, prototypes, and modest collections.

The basic `Index` uses TF-IDF. It fits a vectorizer for each text field, transforms a query with the same vectorizers, scores documents, combines field scores, and sorts the results. This is enough to teach lexical search while leaving the implementation visible.

Use text fields for content such as question and answer, and keyword fields for exact filters such as course. Field boosting lets a match in the question count more than a match in the answer. The first examples used course FAQs because they made both needs clear. A minimal setup can fit documents and search them in the same notebook process.

There are three main index types. `Index` provides the basic TF-IDF behavior. `AppendableIndex` is an inverted index that keeps the same fit and search concepts while allowing new documents to be added after initialization. It is useful when an agent needs to write information back into an index. `VectorSearch` ranks precomputed embeddings with cosine similarity. It is a teaching and local-example tool rather than a replacement for a vector database.

The filters are shared. You can filter by exact keywords, numeric ranges, and date ranges. Highlighting extracts snippets and marks matching terms. This supports a two-step agent workflow: first inspect a relevant snippet, then request the complete document if the snippet justifies it. That mirrors how a person scans search results before opening a page.

Packaging matters once the library changes. A single downloadable file works until every fix requires participants to fetch another copy. Publishing minsearch to PyPI allows installation with `uv` or `pip` and gives course notebooks a versioned dependency.

Performance also needs a boundary. The appendable index was initially much slower because it recomputed tokens and scores on every search. A benchmark measured 14 times slower indexing and 27 times slower search than the simple implementation. Claude optimized it through a repeatable loop: establish a Simple Wikipedia baseline, change code, verify matching results, and measure speed. The resulting appendable search was 20 to 76 times faster than the scikit-learn index in that benchmark.

Minsearch fits a few thousand documents and has a practical sweet spot around 10,000. It works when everything can live in one Python process and the goal is a notebook, course, prototype, or small automation. If the collection is larger but still local, SQLiteSearch is a better option. For production-scale data, use a search engine or vector database. The small library is useful because its scope stays visible.
