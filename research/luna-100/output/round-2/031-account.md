# Using CRISP-DM to explain AI engineering projects

AI engineering involves tools that weren't part of traditional ML projects, including LLM APIs and agents. Teams also work on retrieval and prompts, along with evaluation and production observability. I wanted to look at the development process behind those tools using a familiar reference.

CRISP-DM was developed in the 1990s for data projects and later adopted by the data science and ML community. Its phases still map reasonably well to much of AI engineering work.

I use a hypothetical classifieds feature to explain that mapping. A seller normally enters a title and description, along with the category and price. We could use an uploaded photo to suggest those fields instead.

## Business Understanding

We first need to understand the problem. If creating a listing takes too long, users may abandon it. Example targets could be reducing creation time from five minutes to one and abandonment from 15% to 5%.

The AI engineer also helps decide whether AI is appropriate. A simpler solution might address the same problem without adding a model.

## Data Understanding

Next, we look at the images users upload. We need to understand how they're stored and accessed, including common formats and resolutions. We also look at how often listings have images and whether they're blurry, rotated, or incomplete.

Existing titles and descriptions may help provide context, as can the categories assigned to listings.

## Data Preparation

We can validate image formats and normalize their size or orientation. We also prepare category metadata and define the structure of the attributes the system should generate.

For a RAG system, preparation could instead involve splitting documents into chunks and creating embeddings, then building a retrieval index.

## Modeling

With a foundation model, much of this work involves designing the system around it. For the classifieds example, we write an extraction prompt and define an output schema, perhaps using Pydantic.

We add validation for the generated attributes and test how reliably the system extracts information from images. We use the results to revise the prompt or configuration.

## Evaluation

We then check the product goals we set at the start. An A/B test could compare the original listing workflow with the AI-assisted version, measuring creation time and abandonment.

If the metrics improve, we may proceed to broader deployment. If they don't, we return to earlier phases and revise the approach.

## Deployment

We connect the service to the listing workflow so it can suggest details when someone uploads a photo. We also need to handle errors and unexpected inputs, then monitor performance and product metrics over time.

Production can reveal inputs we hadn't considered or weaknesses in our evaluation. That can send us back to data preparation, modeling, or evaluation.
