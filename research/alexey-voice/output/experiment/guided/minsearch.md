While preparing the first LLM Zoomcamp run, I needed to teach retrieval in notebooks. I was also running workshops about the same topics, so I wanted the examples to stay easy to set up. They usually contained a few thousand documents, sometimes fewer.

I knew Elasticsearch well, and for a normal production system I would probably use it. But Docker, a server and configuration added setup that was irrelevant to this lesson. I wanted search to run in the same Python process as the notebook. I did not find a small library that fit those needs, so I built minsearch.

I had prior experience with text processing and search. A chat assistant could provide code from my description and make fixes, which made it practical to start small. The first implementation was one Python file with one Index class and bag-of-words TF-IDF search.

The course FAQ documents had a question, answer, section, course name and metadata. Matches in questions needed more weight than matches in answers. Sometimes a search also needed to be limited to one course. Those requirements explain the two additions that followed: field boosting and keyword filtering.

Initially, participants downloaded the file again whenever I changed it, using wget in LLM Zoomcamp. As the library changed, repeated downloads became inconvenient. So I packaged minsearch and published it on PyPI, which let participants install it with uv or pip.

Later, during the second LLM Zoomcamp run, agent examples needed to add or modify indexed data. That motivated AppendableIndex. It retained fit and search, while allowing documents to be appended individually.
