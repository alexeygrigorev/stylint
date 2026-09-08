# What I Changed When 2026 05 29 Minsearch The Small Search Library Became Too Much

I started working on 2026 05 29 minsearch the small search library because there was a concrete problem in front of me. The first version was useful enough to try, but it also showed where the workflow was becoming uncomfortable. This is what I changed, and what I learned from the result.

I did not begin with a large architecture. I followed the friction in the existing process. When one step became expensive, confusing, or repetitive, I looked for a smaller change that would remove that particular problem.

At one point, Two years ago, I was preparing the first run of [LLM Zoomcamp], my free course on building LLM applications. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. I was also running workshops on the same topics. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. Search, or retrieval, is one of the most important parts of RAG. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. I needed a way to teach it without asking participants to install Docker or Elasticsearch. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. So I built [minsearch]: a small in-process Python search library. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. It started as the smallest thing I needed to teach retrieval in a notebook, then grew as the course examples changed. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. In this post, I will share: Why was Elasticsearch too much for this setup How the first version worked How it became a PyPI package Why I added an appendable index and vector search How I used Claude to make it faster When minsearch is the right tool Why Elasticsearch Was Too Much In the first run of LLM Zoomcamp, I needed to show participants how to index a small dataset, submit a query, and retrieve relevant documents. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. Usually, it was a few thousand documents, sometimes fewer. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. Most of the examples were run in notebooks, sometimes on Google Colab, using open-source LLMs on a GPU. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. And working with notebooks was my main motivation for creating minsearch as a lightweight alternative to more complex search engines. I kept this part visible because it explains the decision rather than only describing the final shape.

This sequence also explains what the approach does not promise. A working example can be appropriate for its context without becoming a universal recipe. The constraints, inputs, and evaluation method still matter, so I would keep them next to any claim about the result.

I prefer this kind of workflow because it leaves a trace of the reasoning. Someone reading it can see what was fixed, what remained manual, and which parts can be changed independently. That is more useful than a polished description that hides the tradeoffs.

There is no need to add a dramatic conclusion here. The useful result is concrete: the source describes a particular problem, a set of decisions, and an outcome with limits. Those details are enough to reproduce the idea or decide that a different approach fits better.
