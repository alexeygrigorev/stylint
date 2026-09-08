# Why I Still Use CRISP-DM for AI Engineering

AI engineering can look new because the tools are new. Teams work with LLM APIs, retrieval pipelines, agents, prompts, evaluation systems, and production observability. But when I step away from the names of those tools, the development process still looks familiar. Many stages map naturally to CRISP-DM, the lifecycle created in the 1990s for data projects.

I use CRISP-DM as a reference point rather than claiming that AI engineering is identical to traditional machine learning. The six phases are Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, and Deployment. An online classifieds feature makes the relationship concrete. Imagine a listing form where a user enters a title, description, category, and price. An AI feature could suggest those fields from a photo.

Business Understanding comes first. The problem might be that creating a listing takes too long and users abandon it. The team could define goals such as reducing creation time from five minutes to one and lowering abandonment from 15 percent to 5 percent. At this point, the AI Engineer also helps decide whether AI is appropriate or whether a simpler change would solve the problem.

Data Understanding means examining the inputs and the context around them. For the classifieds feature, that means asking how uploaded images are stored, what formats and resolutions appear, how often listings contain images, and whether images are blurry, rotated, or incomplete. Existing titles, descriptions, and categories may provide additional context for structured outputs.

Data Preparation turns that understanding into usable inputs. Images may need format validation, size or orientation normalization, and metadata preparation. The team also needs to define what the generated attributes should look like. In a RAG system, preparation might instead include chunking documents, generating embeddings, and building a retrieval index.

Modeling is where the system around the foundation model is designed and tested. The work may include writing an extraction prompt, defining a schema such as a Pydantic model, validating generated attributes, and testing how consistently the system reads information from images. The team refines the prompt or configuration from the results. It is modeling in the CRISP-DM sense, even when no foundation model is trained.

Evaluation returns to the goals from the first phase. An A/B test could compare the existing listing process with the AI-assisted version. The team would check listing time and abandonment. If the metrics improve, the feature can move toward broader deployment. If they do not, the team returns to an earlier phase instead of treating deployment as inevitable.

Deployment connects the system to the listing workflow, handles errors and unexpected inputs, and monitors performance. It is not the end of the work. Production reveals edge cases and weaknesses in the evaluation criteria, sending the team back to data preparation, modeling, or evaluation. That iterative loop is the part of CRISP-DM that remains most useful to me: it keeps the product problem connected to every technical decision.
