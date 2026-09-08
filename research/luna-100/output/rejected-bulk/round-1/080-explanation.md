# Forward-deployed engineering became a growing part of the AI: a practical guide

This article explains the workflow described in the source. The goal is to make the sequence understandable: start with the problem, choose a small implementation, check what it does, and keep the limitations visible.

Forward-deployed engineering became a growing part of the AI engineering market in 2026.

As a result, far we have 4,894 descriptions, and among them, the number of FDE-related postings increased from 28 in January to 108 in July.

According to this dataset, the AI Engineering job market doubled in these 6 months.

However, the number of FDE listings grew 4 times!

That is, it’s growing at twice the overall AI Engineering market rate.

Live FDE job postings nearly quadrupled between January and June 2026

In this article, I analyze 113 FDE postings to understand what this work involves.

Since our dataset focuses on AI Engineering roles, it’s limited to FDEs working in AI.

We discuss

* how companies define the role
* which skills they expect
* how FDE differs from applied AI engineering, solutions engineering, and consulting

At the end of the article, we also include a quick self-assessment checklist to help you determine whether the FDE role is for you.

## Forward-Deployed Engineer

Palantir created the forward-deployed engineering model in 2006.

They had a general platform, but making it useful required adapting it to each customer’s data, workflows, and infrastructure.

To solve it, they placed their engineers in their customer’s teams.

FDEs identified their problem, configured Palantir’s platforms, built integrations and custom components.

They also supported product development: when the same problem appeared across deployments, Palantir would integrate this as a feature to the main platform.

Palantir’s FDE model applies directly to AI in enterprises today.

General-purpose models must be adapted to each customer’s data, systems, and workflows before they can deliver value in production.

There’s a “deployment gap” - the gap between a prototype and a working customer system.

It exists because many enterprises don’t have the engineering capacity or product knowledge to close it themselves.

A forward-deployed engineer is a customer-facing software engineer who turns an ambiguous business problem into a working production system.

They work alongside the customer to define the problem, design the solution, adapt and integrate the company’s product, build any missing software, deploy and debug the system, and feed recurring customer needs back into the core product.

## FDE’s responsibilities: our analysis

We collected a dataset of 113 FDE jobs descriptions from January to July, and .

They include:

* Direct client engagement (90% of postings)
* Building and deploying production system (87% of postings)
* System, API, and data integration (62% of postings)
* Project scoping, discovery, and requirements gathering (51% of postings)
* System testing, evaluation, and monitoring (41% of postings)
* Channeling customer feedback back into the core product roadmap (39% of postings)
* Developing prototypes, demos, and proofs of concept (25% of postings)
* Travel or client on-site presence (10% of postings)


If we compare it with the rest of the dataset, only 21% of the other AI roles are expected to interact with the clients.

Here’s how it is possible to describe the FDE’s main responsibilities


### 1) Understand the customer’s problem

FDEs usually begin with a desired business outcome.

They work with users, domain experts, and engineering teams to understand the existing workflow, examine the available data, and identify technical constraints.

A useful way to apply this is to keep each decision next to the constraint that caused it. Begin with the smallest working version, verify the important path, and only then add the next piece. When a tool produces something that looks complete, inspect the underlying behavior as well. The source is careful about this distinction, and it is the part worth carrying into another project.
