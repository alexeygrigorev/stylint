Two years ago, I was preparing the first run of [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp/tree/main), my free course on building LLM applications. That first run focused mostly on RAG. I was also running workshops on the same topics.

Search, or retrieval, is one of the most important parts of RAG. I needed a way to teach it without asking participants to install Docker or Elasticsearch.

So I built [minsearch](https://github.com/alexeygrigorev/minsearch): a small in-process Python search library. It started as the smallest thing I needed to teach retrieval in a notebook, then grew as the course examples changed.

In this post, I will share:

* Why was Elasticsearch too much for this setup
* How the first version worked
* How it became a PyPI package
* Why I added an appendable index and vector search
* How I used Claude to make it faster
* When minsearch is the right tool


## Why Elasticsearch Was Too Much

In the first run of LLM Zoomcamp, I needed to show participants how to index a small dataset, submit a query, and retrieve relevant documents. Usually, it was a few thousand documents, sometimes fewer. Most of the examples were run in notebooks, sometimes on Google Colab, using open-source LLMs on a GPU. And working with notebooks was my main motivation for creating minsearch as a lightweight alternative to more complex search engines.

For a normal production system, I would probably reach for [Elasticsearch](https://github.com/elastic/elasticsearch). It is powerful, and I knew it well. But for a workshop notebook, it was too much. It requires a server, Docker, configuration, and operational details that weren’t the point of the lesson.

In the course or workshop setup, everything should run within a single notebook. I looked for a small Python library that could do a good-enough lexical search within the same Python process as the notebook, but I didn’t find anything that fit.

At that time, I had been doing text processing and search for quite some time, so building a small in-process search library myself wasn’t hard. Even back then, when coding agents weren’t as good as they are now, I could describe what I wanted to a chat assistant, get code back, and ask for a few fixes.


The retrieval module from the first run of LLM Zoomcamp, built around minsearch.

## The First Version

The [first implementation](https://github.com/alexeygrigorev/minsearch/tree/62ddbe9bc4adbc38cfd14114a2128fdf3b8e0110) was a single Python file.


It had one class, `Index`, and the search was just a bag-of-words with TF-IDF.

It worked like this:

1. Fit a TF-IDF vectorizer for each text field
2. Transform the query with the same vectorizers
3. Multiply the matrices to get document scores
4. Add the scores from all text fields
5. Sort the documents by score

In my teaching, I used examples with FAQs from my free courses, the Zoomcamps. A typical document had a question, an answer, a section, a course name, and some metadata.

This already required a little more than a plain text search. Matches in the question field should count more than matches in the answer field. Sometimes I wanted results only from one course. So the first version also had field boosting and keyword filtering.

That made minsearch useful for teaching. The implementation was small enough that learners could understand it, yet it still included the pieces I needed for real-world course examples: text search, filters, and boosts.

The basic usage looked like this:

```
from minsearch import Index
index = Index(
    text_fields=[”question”, “answer”],
    keyword_fields=[”course”]
)
index.fit(docs)
results = index.search(”can I join the course?”)
```

I also shared how I built it in the workshop titled “[Build Your Own Search Engine](https://github.com/alexeygrigorev/build-your-own-search-engine).” The first version of that workshop came out around two years ago, originally as a DataTalks.Club talk. But I later updated it to include the newer library versions and published it as a [structured tutorial](https://aishippinglabs.com/workshops/2026-05-14-build-your-own-search-engine) in the [AI Shipping Labs workshop library](https://aishippinglabs.com/workshops/).

If you want to understand how minsearch works internally, that workshop is the best place to look.

## From a File to a Package

At first, people downloaded the single Python file, and that worked until I needed to ship changes.

Every time I fixed something or added a feature, course participants had to download the file again. In LLM Zoomcamp, we used to do that with `wget`. It was fine for one notebook, but not for a library I kept changing.

So I packaged it properly, [published it on PyPI](https://pypi.org/project/minsearch/), and now people can install it with `uv` or `pip`:

```
uv add minsearch
```

The first published version was [0.0.1](https://pypi.org/project/minsearch/0.0.1/). At the time of writing, the current version is `0.1.0`.



## Where I Use It

I now use minsearch across my courses and workshops:

* [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)
* [AI Hero](https://aishippinglabs.com/courses/aihero)
* [AI Engineering Buildcamp](https://maven.com/alexey-grigorev/from-rag-to-agents)

I also use it outside teaching, in personal and DataTalks.Club projects. One example is the [DataTalks.Club FAQ system](https://github.com/DataTalksClub/faq), where the automation reads GitHub issues and creates FAQ entries. Before adding a new question, it uses minsearch to check whether a similar question already exists.

I told you about it in [From Google Docs to an Automated FAQ System for DataTalks.Club Courses](https://alexeyondata.substack.com/p/from-google-docs-to-an-automated):

[From Google Docs to an Automated FAQ System for DataTalks.Club Courses](https://alexeyondata.substack.com/p/from-google-docs-to-an-automated)

The automation loads the FAQ, builds the index, searches it, and continues in one Python process.

That is still the main reason I use minsearch, but the library had to grow once the course examples changed.

## Implementing Inverted Index and Vector Search

The appendable index came later, when I started working on the second run of LLM Zoomcamp and added the module covering agents.

### Implementing Inverted Index

I wanted to show that agents can do more than search existing documents, like adding data back to the index and modifying it. The original index didn’t support that well. It was built for the simple case: create the index, search it, and throw it away when the notebook ends.

To allow the agent to modify the index, I implemented a new index type: `AppendableIndex`. It’s an inverted index that keeps the same `fit` and `search` methods, but it also lets you append documents one at a time.


### Adding Vector Search

Vector search came later for a similar reason. I had already taught it in Build Your Own Search Engine, but it wasn’t part of the library at first. Eventually, I added it too.


`VectorSearch` works on pre-computed embeddings and ranks results by cosine similarity. It isn’t trying to replace a full vector database. It is a simple tool for local examples, and my primary use case is to explain search concepts during my courses and workshops.

### Three Index Types and Highlighting

Today the library has three main index types:

* `Index`: The basic TF-IDF index using scikit-learn
* `AppendableIndex`: An inverted index implementation that lets you add documents later
* `VectorSearch`: Cosine similarity search over pre-computed vectors

The same filter model works across all three. You can filter by exact keyword matches, numeric ranges, and date ranges. Keyword fields are optional now, because not every search example needs filtering.

There is also highlighting now. It extracts snippets from search results and marks where the query terms matched. The motivation was that we started to have more and more agents, and I realized that for agents, it is better to mirror how humans see.

The way humans search is that we look at the snippet, for example, in a Google search, and based on what we see, we decide whether we want to check an article. For agents, I think it works better if they can first see highlighted snippets; then, based on those snippets, they can decide whether to check the entire page for details.

I don’t see minsearch as a big infrastructure project. It grew because the examples kept needing more practical features.

## Making minsearch Faster with Claude Code

I used the appendable index more and eventually noticed a problem: it was much slower than the simple index.

At first, I just ignored it. The appendable index was doing more work, and the datasets were small. But at some point, it became too slow even for my use, so I decided to benchmark it.

The first benchmark showed that the appendable index was about 14 times slower to index and 27 times slower to search.

I asked Claude to look at it, and it found out the reason for this inefficiency. The appendable index recomputed tokens and scores during every search, while the simple index relied on scikit-learn’s optimized batch operations.

This was one of the first times I used an AI assistant to benchmark and optimize something like this.

I gave Claude a clear loop:

1. Benchmark against Simple Wikipedia and save a baseline
2. Make changes to the code
3. Check that results still match the baseline
4. Compare the speed

Then I let it run and checked in about once an hour while I worked on course materials. After a few rounds, search in the optimized appendable index was 20 to 76 times faster than the scikit-learn-based index. The gap grew on larger datasets.

The full benchmark writeup is here: [benchmark/BENCHMARK\_WRITEUP.md](https://github.com/alexeygrigorev/minsearch/blob/main/benchmark/BENCHMARK_WRITEUP.md).

## When Minsearch Is the Right Tool

Minsearch is a good fit when:

* You have a small or medium dataset
* You need to search in a notebook, course, prototype, or small automation
* Everything can live in one Python process
* You are indexing up to a few thousand documents

The sweet spot is up to 10,000 documents. At that size, indexing is fast, search is convenient, and you get a useful retrieval layer without setting up extra infrastructure.

It works best when there is enough plain text to search over. That is the case for course FAQs, workshop datasets, documentation pages, and small internal collections.

Beyond that, minsearch is no longer the right tool.

If you have a larger local dataset but still want something lightweight, use [SQLiteSearch](https://github.com/alexeygrigorev/sqlitesearch) instead. I built it for exactly that case, and wrote about it in [How I Built SQLiteSearch](https://alexeyondata.substack.com/p/how-i-built-sqlitesearch-a-lightweight).

[How I Built SQLiteSearch: A Lightweight Python Library for Local Text and Vector Search](https://alexeyondata.substack.com/p/how-i-built-sqlitesearch-a-lightweight)

For bigger systems, use a real search engine or vector database.
