When I was preparing the first run of LLM Zoomcamp, I needed to teach retrieval in notebooks. I was also running workshops about the same topics. Usually the examples contained a few thousand documents, sometimes fewer.

I knew Elasticsearch well, and for a normal production system I would probably use it. But for a workshop notebook, it meant asking participants to set up Docker, a server and configuration that weren't part of the lesson.

I wanted search to run in the same Python process as the notebook. I didn't find a small library that fit, so I built minsearch. I had worked with text processing and search before, and a chat assistant could turn my description into code and help with fixes.

The first implementation was one Python file with one `Index` class and bag-of-words TF-IDF search. In the course, I used FAQ documents with a question and answer, along with a section, course name and metadata.

I wanted matches in the question to count more than matches in the answer. Sometimes I also wanted to search within one course. So the first version already had field boosting and keyword filtering.

At first, participants downloaded the file with `wget` and had to download it again whenever I changed it. As I kept changing the library, this became inconvenient. So I packaged minsearch and published it on PyPI, and participants could install it with `uv` or `pip`.

During the second LLM Zoomcamp run, I wanted to show agents adding or modifying indexed data. The original index didn't support that well, so I implemented `AppendableIndex`. It kept `fit` and `search`, and I could append documents one at a time.
