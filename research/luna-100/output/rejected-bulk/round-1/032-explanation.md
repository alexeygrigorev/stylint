# CRISP-DM as a Guide for AI Systems



The useful part of this example is the workflow. I will walk through the problem, the decisions, and the limits so the idea stays connected to what actually happened. 

If you come from machine learning or data science backgrounds, there’s a high chance you already know

CRISP-DM, a framework developed in the 1990s for structuring data projects and later actively adopted by

the DS and ML community. At first glance, AI engineering can look like a completely different

discipline. Today’s teams work with LLM APIs, retrieval pipelines, agents, prompts, evaluation tooling,

and production observability. The stack has changed significantly. But if you step back from the tools,

the underlying development process is less new than it seems. Many of the stages of the work still map

reasonably well to the CRISP-DM lifecycle. In this post, we use CRISP-DM as a reference point to look at

AI engineering work phase by phase. We show where the structure still holds and how it can help when

planning or analyzing modern AI systems. The Six CRISP-DM Phases, in AI Terms CRISP-DM breaks projects

into six phases: Business Understanding Data Understanding Data Preparation Modeling Evaluation

Deployment Example To illustrate how CRISP-DM can be applied to AI engineering, let’s take an example of

an online classifieds platform where users can sell their items. To create a new listing, they fill out

the form with the item’s title, description, category, and price. Instead of asking a user to fill in

every field manually, we may want to create an AI feature that automatically suggests fields based on a

user-uploaded photo. With that example in mind, we can walk through the CRISP-DM phases. 1. Business

Understanding The first phase focuses on defining the problem and the criteria for success. In the

classifieds example, the problem may be that creating a listing takes too long, causing users to drop

off. The result can lead to measurable objectives such as reducing listing creation time from 5 minutes

to 1 minute and lowering the abandonment rate from 15% to 5%. At this stage, the AI engineer often helps

determine whether an AI system is appropriate or whether a simpler solution could address the problem.

2. Data Understanding Once the objective is defined, the next step is to examine the data that could

support the solution. For the classifieds feature, the team would analyze the image data that users

upload when creating listings. Questions at this stage might include: How are images stored and

accessed? What formats and resolutions are common? How often do listings include images? Are images

frequently blurry, rotated, or incomplete? The team may also explore related data such as existing

listing titles, descriptions, and categories. These fields can provide additional context that helps the

AI system generate structured outputs. 3. Data Preparation After understanding the available inputs, the

team prepares them for use by the system. For the classifieds feature, this might involve: Validating

uploaded image formats Normalizing image size or orientation Preparing category metadata Defining the

structured output format for generated attributes In other AI systems, preparation may involve tasks

like document chunking, embedding generation, or building retrieval indices for RAG pipelines. 4.

Modeling The modeling phase focuses on designing and testing the system that will produce the desired

output. In traditional machine learning projects, this stage usually involves training and



That is the part I would keep from this example: connect each tool to the problem that made it necessary, and keep the limitation next to the claim. The details matter because they explain what can be reused and what was specific to this project.
