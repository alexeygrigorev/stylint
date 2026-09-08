# Planning an AI feature through CRISP-DM

If you know CRISP-DM from data science or machine learning, you can use it to think through an AI engineering project. It dates from the 1990s, but many stages still apply when you work with foundation models and retrieval instead of training a model yourself.

Consider a classifieds site where a seller fills in a title and description, then adds a category and price. We could build a feature that suggests those fields from an uploaded photo.

Business Understanding starts with the problem the feature should address. Perhaps creating a listing takes too long and users leave before finishing. We might aim to reduce the process from five minutes to one, with abandonment falling from 15% to 5%.

We should also consider whether a simpler change could solve that problem. Defining a measurable objective helps us decide whether an AI feature is appropriate.

In Data Understanding, we examine the inputs available to us. We look at how images are stored and accessed, including their formats and resolutions. We also check how often users provide photos and what quality problems appear.

We may find images that are blurry, rotated, or incomplete. Existing listing titles and descriptions, along with category data, can provide context for generating the fields.

Data Preparation then makes the inputs usable. We validate image formats and normalize size or orientation, prepare category metadata, and define the expected structure of the output.

In another project, the same phase could involve chunking documents for RAG. We might generate embeddings and build a retrieval index before working on the system that uses them.

During Modeling, we design and test the system around the foundation model. For this feature, that includes the extraction prompt and an output schema such as a Pydantic model. We validate the generated attributes and test how consistently the system reads information from images.

The experiments give us results to use when revising the prompt or configuration. We then move to Evaluation and compare the feature against our original product goals.

An A/B test could measure creation time and abandonment for the existing workflow and the AI-assisted version. If the results improve, we may move toward broader deployment. Otherwise, we return to earlier work and adjust the approach.

Deployment connects the AI service to the backend and listing process. We handle errors and unexpected inputs, while continuing to monitor performance and product metrics.

A deployed system can reveal cases our earlier tests missed. We may need to revisit data preparation or modeling, or change the evaluation criteria.
