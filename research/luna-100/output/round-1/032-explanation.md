# The Six CRISP-DM Phases in an AI Feature

CRISP-DM was created for data projects in the 1990s, but its structure still offers a useful way to discuss AI engineering. The tools may now include LLM APIs, retrieval, agents, prompts, evaluation systems, and observability. The lifecycle still asks the same broad questions: what problem are we solving, what data supports it, how do we build the system, how do we know it works, and how does it operate in production?

Consider an online classifieds site. A user creates a listing by entering a title, description, category, and price. The proposed AI feature uses a photo to suggest those fields.

Business Understanding defines the problem and success criteria. If listing creation takes too long, the team might target a reduction from five minutes to one minute and a drop in abandonment from 15 percent to 5 percent. This phase also asks whether AI is necessary. A simpler product change may solve the same problem without adding a model.

Data Understanding examines the inputs before the system is designed. The team studies how images are stored and accessed, which formats and resolutions are common, how often listings contain photos, and whether images are blurry, rotated, or incomplete. Existing listing titles, descriptions, and categories can provide context for the attributes the system should generate.

Data Preparation makes those inputs usable. Images may need format validation, resizing, and orientation normalization. Category metadata can be prepared, and the output structure for generated attributes can be defined. Other AI systems may prepare documents by chunking and embedding them, then building a retrieval index for a RAG pipeline.

Modeling focuses on the system that produces the result. With a foundation model, this often means designing a prompt instead of training a model from scratch. The team defines a structured schema, such as a Pydantic model, validates generated attributes, and tests extraction quality on representative images. Experiments lead to changes in the prompt or configuration.

Evaluation checks the result against the original product goals. An A/B test could compare the current listing flow with the AI-assisted version. The team measures listing creation time and abandonment rather than relying on a convincing demo. If the metrics improve, deployment is justified. If they do not, the team returns to data preparation or modeling and changes the system.

Deployment integrates the AI service with backend systems. The production version needs error handling, support for unexpected inputs, and monitoring of system performance. Product metrics continue after release so the team can check whether the feature delivers value.

CRISP-DM describes deployment last, but the process is iterative. New production inputs can expose a data problem, an evaluation gap, or a weak prompt. Those findings send the team back to earlier phases. The value of the framework is this connection between business goals and technical work, even when the model and surrounding tools have changed.
