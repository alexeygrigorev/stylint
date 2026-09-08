When I was preparing the first run of LLM Zoomcamp, I needed to teach retrieval in notebooks. I was also running workshops about the same topics, so I wanted the examples to stay focused on retrieval rather than on setting up infrastructure. Usually the examples contained only a few thousand documents, and sometimes fewer.

I knew Elasticsearch well, and for a normal production system I would probably use it. But Docker, a server, and configuration would add setup that was irrelevant to this lesson. I wanted search to run in the same Python process as the notebook. I did not find a small library that fit those needs, so I built minsearch.

The first implementation was deliberately small: one Python file with one `Index` class and bag-of-words TF-IDF search. I already had experience with text processing and search, and a chat assistant could provide code from my description and make fixes. That was enough to get the basic version working.

The course FAQ made the next requirements clear. Each document had a question, answer, section, course name, and metadata. A match in the question needed more weight than a match in the answer, and some searches needed to be limited to one course. Those needs explain the field boosting and keyword filtering in minsearch.

At first, participants downloaded the file again whenever I changed it, using `wget` in LLM Zoomcamp. As the library changed, repeated downloads became inconvenient. I packaged minsearch and published it on PyPI so participants could install it with `uv` or `pip`.

Later, during the second LLM Zoomcamp run, the agent examples needed to add or modify indexed data. That motivated `AppendableIndex`: it retained `fit` and `search` while allowing documents to be appended individually.
