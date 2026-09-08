# Assignment

Write a 250–400 word newsletter excerpt in Alexey's first person, covering the origin and early evolution of minsearch. Use only the facts below. This is a reconstruction of an archived account, not a new event. Do not add a subscribe line or a general introduction to AI. Headings are optional. Output only the article excerpt.

# Fact ledger

- M1: While preparing the first LLM Zoomcamp run, Alexey needed to teach retrieval in notebooks. He was also running workshops about the same topics.
- M2: Examples usually contained a few thousand documents, sometimes fewer.
- M3: Alexey knew Elasticsearch well and would probably use it for a normal production system. Docker, a server and configuration added setup that was irrelevant to this lesson.
- M4: He wanted search to run in the same Python process as the notebook. He did not find a small library that fit his needs, so he built minsearch.
- M5: He had prior experience with text processing and search. A chat assistant could provide code from his description and make fixes.
- M6: The first implementation was one Python file with one Index class and bag-of-words TF-IDF search.
- M7: Course FAQ documents had a question, answer, section, course name and metadata. Matches in questions needed more weight than answers, and searches sometimes needed to be limited to one course. This explains field boosting and keyword filtering.
- M8: Initially participants downloaded the file again when Alexey changed it, using wget in LLM Zoomcamp.
- M9: Repeated downloads became inconvenient as the library changed. Alexey packaged minsearch and published it on PyPI so participants could install it with uv or pip.
- M10: Later, during the second LLM Zoomcamp run, agent examples needed to add or modify indexed data. This motivated AppendableIndex, which retained fit and search and allowed appending documents individually.

# Required content

Preserve M1, M3, M4, M6, M7, M8, M9 and M10, including uncertainty about production use and the reason for each change. Other facts are optional. Do not add benchmarks, costs, dates, adoption claims, classroom incidents or emotional reactions. The account should stop after the appendable index motivation.
