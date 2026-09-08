# Evaluating the cohort projects

Participants in my third AI Engineering cohort built applications for different users. Looking at the projects gives us several ways to check whether a generated answer helps with the task. The exam generator helps professors review questions. The ATS tool helps applicants understand a job match. The chess coach works from games a player actually played, so its practice can address mistakes from those games.

Several projects use human review as part of the product. Quizgen lets a professor approve, edit, or reject questions. The ATS analyser prefers high recall because flagging a possible missing skill is better for its purpose than silently missing one. WorkerChronicle shows evidence gaps before producing a cover-letter outline. Human judgment remains visible instead of being hidden behind a single generated answer.

Retrieval systems also need a useful source and a clear output. Research Radar ranks papers against a learned interest profile and sends five recommendations. Its ratings become both knowledge base and evaluation data.

AI Learning OS separates queued material from the knowledge a learner has actually studied, then cites that knowledge in chat. A document-preparation pipeline adds metadata and numbered chunks. Later queries can filter the private material.

Research Radar tracks NDCG@5, which improved from 0.871 to 0.923 after tuning its ranking blend. The diet coach compares judge performance across versions using 88 labeled answers. Accuracy rose from 46.6% to 73.9%.

The Teaching Copilot calibrates a judge on 33 cases. Its first judge scored 0.727 accuracy, and the calibrated version reached 1.0 on that set. The learning system tests an empty knowledge base to ensure the assistant doesn't invent content. These checks are small enough to run repeatedly and tied to a failure the author cares about.

Other participants built applications where the intermediate output can be inspected. A natural-language SQL assistant returns both an answer and the read-only query. A multi-agent platform moves a requirement through PM and human approval. Agents then design the architecture and develop the backend code. Other agents write tests and review the implementation before it gets packaged.

LearnMate turns a video into a concept map and asks questions about each concept. It provides hints or coding exercises when needed. GapFinder grades diagnostic answers against the transcript and identifies sections the student should rewatch.

Several participants also limited the first version to something they could build and test. The document-preparation team focused on PDFs and provided a command-line interface without a UI. Leo's chess coach uses deterministic templates when there's no API key, and CI uses a TestModel to keep tests offline.
