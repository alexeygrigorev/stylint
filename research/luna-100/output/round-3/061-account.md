# Growing minsearch from a notebook example

I built minsearch while preparing the first LLM Zoomcamp two years ago. I needed participants to index a small collection and retrieve documents inside a notebook. Some examples ran in Google Colab with an open-source model on a GPU.

For a normal production system, I'd probably use Elasticsearch. I knew it well, but a server and Docker setup would get in the way of the workshop. I wanted retrieval in the same Python process as the notebook and couldn't find a small library that fit.

The first implementation was one Python file with an `Index` class. It used TF-IDF, fitting a vectorizer for each text field and transforming the query with the same vectorizers. It calculated document scores, combined the field scores, and sorted the results.

My examples used course FAQs, where a question and its answer need different weights. I wanted a match in the question to count more. Sometimes I also needed to restrict results to one course, so field boosting and keyword filtering were part of the first version.

Participants initially downloaded the Python file with `wget`. Every fix or new feature meant downloading it again, which became inconvenient as I kept changing the library. I published it on PyPI so people could install it with `uv` or `pip`.

When I added agents to the second course run, I wanted them to put new information into the index. The original implementation was suited to building an index once and discarding it when the notebook ended.

I added `AppendableIndex`, an inverted index with the same `fit` and `search` methods that also accepts documents one at a time. Later, I added `VectorSearch` to rank precomputed embeddings using cosine similarity.

The index types share filters for keywords and numeric or date ranges. Highlighting also lets an agent see matching snippets before deciding whether to open a full document, similar to how people scan search results.

I eventually noticed that the appendable index was slow. At first I ignored it because it did more work and the datasets were small. When it became too slow even for my examples, I benchmarked it.

It was about 14 times slower to index and 27 times slower to search than the simple implementation. Claude found that it recomputed tokens and scores during searches, while the original index used optimized scikit-learn operations.

I asked Claude to save a Simple Wikipedia baseline, make changes, verify matching results, and compare speed. I checked in roughly once an hour while working on course material. After several rounds, appendable search was 20 to 76 times faster than the scikit-learn index in those benchmarks.

I use minsearch for notebooks and small automations, including checking for similar questions in the DataTalks.Club FAQ. Its sweet spot is up to 10,000 documents. For larger local collections, I built SQLiteSearch, while bigger systems need a search engine or vector database.
