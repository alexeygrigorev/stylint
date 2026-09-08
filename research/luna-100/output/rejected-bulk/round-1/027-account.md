# What a Thousand Job Ads Showed



I want to describe what happened, because the sequence of small decisions is more useful than a polished summary. 

The term “AI engineer” is still relatively new, and the best way to understand its definition today is

to examine market demand. To cut through the confusion, we analyzed 1,000+ “AI Engineer” job

descriptions from a large tech job site across Berlin, Amsterdam, London, Los Angeles, and New York, and

distilled them into a practical, market-driven definition of the role. To see how companies use the

title “AI Engineer” in practice, we asked our LLM to classify each of the 889 job descriptions into one

of three main categories: ≈70%: Work directly on LLM and GenAI systems: RAG, agents, evaluation, and

production deployment. These roles are closest to the “classic” image of an AI engineer building

AI-powered product features. ≈28.5%: Focus on infrastructure and platforms around AI rather than model

behavior itself: internal AI platforms, GPU and inference infrastructure, data pipelines, deployment and

monitoring tooling, and prompt or experimentation UIs. <2%scikit-learn, XGBoost, PyTorch, TensorFlow,

CV, recommendations but are labeled “AI Engineer.” Their day-to-day looks more like that of an ML

Engineer or Research Engineer than an LLM application builder. Looking at how the biggest category where

the majority of roles fall into, we can suggest this practical definition: An AI engineer is an engineer

who owns the design, evaluation, and production operation of systems built on foundation models.

95.6%nearly 50%20%. Overall, market signals point to AI engineers being primarily Python-based,

cloud-native application builders who integrate LLM systems into production environments. ML knowledge

is still valuable, but it serves as a supportive context rather than the core of the role. Here are the

most frequent skill mentions grouped into categories, listed from most to least prominent: most

distinctive cluster 35.9%: The strongest GenAI skill signal; more common than prompt engineering or

generic “LLM” mentions. 29.1%: Important but framed as part of system design and evaluation, not a

standalone job. 25.4%: Using hosted APIs with awareness of tokens, latency, cost, and reliability.

14.4%: Multi-step workflows, tool use, and orchestration frameworks. 8.5%: Present but clearly secondary

to integrating and operating models. especially RAG than about prompt engineering or pure model

training/fine-tuning. 2. Programming languages and app layer 82.5%: The backbone of AI engineering

roles. 23.4%14.8%10.7%: Indicate an expectation to build APIs and sometimes UIs around AI systems. Be

fluent in Python, comfortable with web APIs, and at least conversant with modern web/frontend tooling.

3. Cloud and infra The strongest signals come from operations at 17.4% and cloud at 13.4%, which

together form a large production-oriented cluster. Deployment, automation, and infrastructure knowledge

are core expectations for AI engineers. Deployment, automation, and infrastructure knowledge is one of

the core expectations for AI Engineer. 4. ML Foundations 6.4%4.5% are mentioned less frequently, and in

many cases, they are secondary to core application responsibilities. 5. Databases 6.2% of

mentions10.8%9.3%. AI frameworks tend to be interchangeable and ecosystem-driven, while DevOps and

infrastructure tools are standardized and production-critical. 40.1%31.0%29.3%29.1%. Azure appears in

23.9% of roles and GCP in 23.0%, reinforcing that multi-cloud familiarity is useful even when one

provider dominates in a given organization. Cloud and infrastructure tools form a standard baseline for

reproducible, scalable deployments. 18.8%8.0%5.8% No single library dominates; employers care more



That is the part I would keep from this example: connect each tool to the problem that made it necessary, and keep the limitation next to the claim. The details matter because they explain what can be reused and what was specific to this project.
