# Choosing an index for a notebook search example

I use minsearch when a course example or small automation needs retrieval inside one Python process. It began with LLM Zoomcamp notebooks, where setting up Elasticsearch would have added server and Docker work unrelated to the lesson.

For a normal production system, I'd probably use Elasticsearch. For a few thousand documents in a notebook, I wanted a smaller implementation that participants could understand.

The basic `Index` uses TF-IDF over text fields. It fits one vectorizer per field and transforms a query using those same vectorizers. It calculates document scores and adds the scores across fields before sorting the results.

In a course FAQ, the question and answer don't need equal weight. Field boosting lets a question match contribute more to the score. Keyword fields let me filter for an exact value, such as a particular course.

I added `AppendableIndex` when the course began covering agents that could write information back into an index. It uses an inverted index with the same `fit` and `search` methods, while allowing documents to be appended individually.

For embeddings, `VectorSearch` ranks precomputed vectors by cosine similarity. I use it to explain vector search in local examples. It isn't intended to replace a full vector database.

The filters work across the index types. You can use exact keywords, numeric ranges, or date ranges, and keyword fields are optional when the example doesn't need them.

Highlighting extracts snippets and marks the query terms that matched. An agent can read those snippets before deciding whether to request the complete document. That's how I wanted the agent to approach search results, using a short preview before opening a page.

The appendable index needed optimization as I used it more. It initially took about 14 times as long to index and 27 times as long to search as the simple implementation. Claude found repeated token and score computation during searches.

I gave it a benchmark loop using Simple Wikipedia. It saved a baseline, changed the code, checked that results still matched, and measured speed. After several rounds, the optimized appendable search was 20 to 76 times faster than the scikit-learn-based index on those benchmarks.

The library is available on PyPI and can be installed with `uv` or `pip`. Before packaging, participants had to download a replacement Python file whenever I fixed something or added a feature.

Minsearch works for notebooks and prototypes, as well as small automations with enough plain text to search. I describe its sweet spot as up to 10,000 documents. For larger local datasets, I use SQLiteSearch. Bigger systems call for a search engine or vector database.
