# Projects from the third AI Engineering cohort

The third cohort of my AI Engineering course finished during the summer. The projects covered a wide range of real problems. Participants built tools for studying and teaching alongside research assistants. Other projects help with job applications or software development. Some participants presented on Demo Day, and I describe the others as well.

Salma Bouzid built Quizgen for university professors. A professor uploads lecture slides and chooses the question types. The professor then approves or edits the generated exam. Next.js provides the frontend, Supabase stores actions and costs, and an LLM judge checks whether questions are grounded in the course.

Amar Agrawal's ATS Gap Analyser takes a job URL and CV, and returns a match score with missing keywords. It also suggests improvements and writes a cover letter. It doesn't store the documents. Amar evaluated it with 50 manually written cases, and the sixth version reached 88% recall. He preferred flagging a possible missing skill to overlooking one.

Leo Cabibihan's Chess Coach Agent starts with real Lichess, Chess.com, or PGN games. It finds weak positions, explains them, and schedules practice with spaced repetition. Leo imported about 2,700 of his Lichess games for the demo. Deterministic templates let the application run without an API key.

Paulien Out and Alena Fojtik built a document-preparation CLI that adds metadata to PDFs for filtering in private RAG systems.

Hana Ben Ali's Research Radar ranks the 100–300 papers that appear daily on arXiv, sends the top five by email, and learns from her ratings. Its NDCG@5 improved from 0.871 to 0.923.

Thet Su Win's AI Diet Coach plans Southeast Asian meals from 256 recipes and improved judge accuracy from 46.6% to 73.9%.

Wesley Tan's AI Learning OS separates saved content from learned knowledge and checks that an empty knowledge base doesn't produce invented answers.

Marco Teran's Teaching Copilot answers from course material and calibrated its judge to 1.0 on 33 cases.

Lars van Asseldonk built a natural-language-to-SQL assistant over Dutch Railways safety incidents.

Miki Foster's WorkerChronicle retrieves work examples for applications and interviews. It shows where evidence is missing before preparing an editable cover-letter outline.

Nitesh Mishra's platform starts with a requirement and asks a PM agent to prepare user stories. After human approval, agents design the architecture and generate backend code. Other agents write tests and review the code before the system packages the artifacts.

Dianne Bronola's LearnMate builds concept maps from videos and quizzes the learner. Katja Weber's GapFinder grades answers and identifies transcript sections the learner should revisit.

My next cohort priority is helping more participants finish ambitious projects. I'm researching what keeps learners on track and will apply it to the cohort beginning September 21.
