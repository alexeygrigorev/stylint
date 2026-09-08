# What a build-by-building AI engineering course covers

A practical AI engineering course should make the system grow in stages. Start with retrieval, then add tools, tests, monitoring, and evaluation. That is the structure of the AI Engineering Buildcamp. The running example is a Documentation Agent built over Evidently documentation, and each week adds a capability that changes how the system is developed.

Week one covers language models, the OpenAI API, RAG, and search. Participants index the documentation and build a first application that answers questions. This gives them a usable system immediately. Week two provides catch-up material and additional RAG examples. Week three turns the application into an agent that can explore the documentation database.

Reliability comes next. In week four, the agent gets classical unit tests and LLM-based judges. Week five focuses on monitoring: participants inspect behavior in production and collect information for debugging. Week six introduces systematic evaluation with human-in-the-loop judgments, judges that imitate human evaluators, and synthetic data. The progression is deliberate because an agent that answers a demo question is only a starting point.

The course uses optional projects to show variations. An FAQ Assistant uses boosting and filtering. A YouTube Transcript Summarizer extracts summaries and chapters. A PDF Book Processor handles complex layouts. Other examples add web search, YouTube research, coding, code analysis, or a multi-stage deep research process. The point is to see how the same patterns change with a new data source or task.

Homework makes participants implement those ideas independently. Early assignments cover downloading books, extracting PDF text, chunking documents, and building a RAG pipeline. A Wikipedia Agent adds search and page-fetching tools. The DuckDB SQL Agent introduces tests, LLM judges, and cost tracking. A Trivia Quizmaster adds instrumentation. The Recipe Assistant Evaluation uses more than 20 scenarios to detect hallucinations.

The capstone follows the same sequence while staying tied to a participant’s chosen use case. First define the problem and create a RAG version. Then add tools so the application can make decisions, test it, monitor interactions, and evaluate the collected examples. The final weeks are for polish, extension, deployment, peer feedback, and presentation.

Choosing a project early matters. In earlier cohorts, some participants delayed that decision and did not complete the capstone. A design-thinking framework was added to guide the definition stage. It helps someone with an existing idea narrow the scope and gives someone without an idea prompts and templates to begin.

The program is about nine weeks, mostly asynchronous, with a typical workload of three to ten hours per week. Weekly office hours provide a place for technical questions and architecture feedback. The format is intended for people who want to build and debug. Watching the lessons is only one part of the work; the learning comes from carrying a system through the full sequence.
