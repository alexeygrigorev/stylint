# Thirteen Projects from an AI Engineering Cohort

I like looking at these projects together because they are not variations of one demo. Each participant began with a problem they could describe, then chose enough technology to make the first useful version visible.

The participants also made different tradeoffs about data, interfaces, and evaluation.

That variety is the useful part of the cohort.

The third cohort of my AI Engineering course finished during the summer, and the projects covered a wide range of real problems. They included exam generation, job applications, chess practice, research, learning, teaching, and multi-agent software development. Some participants presented on Demo Day, and I describe the others as well.

Salma Bouzid built Quizgen for university professors. A professor uploads lecture slides, chooses a mix of theory, case-study, and applied questions, then approves or edits the generated exam. Next.js provides the frontend, Supabase stores actions and costs, and an LLM judge checks whether questions are grounded in the course. Amar Agrawal’s ATS Gap Analyser takes a job URL and CV, returning a match score, missing keywords, suggestions, and a cover letter. It does not store the documents. Its sixth version reached 88% recall after 50 manually written evaluation cases.

Leo Cabibihan’s Chess Coach Agent starts with real Lichess, Chess.com, or PGN games. It finds weak positions, explains them, and schedules practice with spaced repetition. Paulien Out and Alena Fojtik built a document-preparation CLI that adds metadata to PDFs for filtering in private RAG systems. Hana Ben Ali’s Research Radar ranks the 100–300 papers that appear daily on arXiv, sends the top five by email, and learns from her ratings. Its NDCG@5 improved from 0.871 to 0.923.

The other projects solve similarly concrete problems. Thet Su Win’s AI Diet Coach plans Southeast Asian meals from 256 recipes and improved judge accuracy from 46.6% to 73.9%. Wesley Tan’s AI Learning OS separates saved content from learned knowledge and checks that an empty knowledge base does not produce invented answers. Marco Teran’s Teaching Copilot answers from course material and calibrated its judge to 1.0 on 33 cases.

Lars van Asseldonk built a natural-language-to-SQL assistant over Dutch Railways safety incidents. Miki Foster’s WorkerChronicle retrieves work examples for applications and interviews. Nitesh Mishra’s platform passes a requirement through PM, human confirmation, architecture, developer, QA, review, and artifact packaging. Dianne Bronola’s LearnMate builds concept maps from videos and quizzes the learner. Katja Weber’s GapFinder grades answers and points to transcript sections worth rewatching.

These projects are different, but they share evaluation, a defined user, and a workflow that produces a useful result. My next cohort priority is helping more participants finish ambitious projects. I am researching what keeps learners on track and will apply it to the cohort beginning September 21.
