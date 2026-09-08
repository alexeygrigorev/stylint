# Working Through the AI Engineering Buildcamp

The AI Engineering Buildcamp is structured around building one project while learning the parts of AI engineering that make it useful in practice. The course lasts nine weeks, with a running example called the Documentation Agent.

That example gives the lessons continuity, but it isn't the only project. The optional work shows how the ideas change with different data and products.

The RAG projects include an FAQ Assistant and a YouTube Transcript Summarizer. A PDF Book Processor handles documents with mathematical formulas and complicated layouts.

For agents, there's a Web Search Agent and a YouTube Researcher. The set also includes a Coding Agent that scaffolds Django applications, a Code Analysis Agent, and a Deep Research Agent. Each project practices a different combination of retrieval, tools, and structured output.

Homework provides another kind of practice because you build a system yourself. During weeks 1 and 2, you download books and extract PDF text. You then chunk the documents and build a full RAG pipeline.

Week 3 is a Wikipedia Agent. In week 4, you build a DuckDB SQL Agent for New York City taxi data. You also write pytest tests, add LLM judges, and track costs. Week 5 uses Logfire to instrument a Trivia Quizmaster Agent. Week 6 evaluates a Recipe Assistant with more than 20 scenarios and checks for hallucinations.

The capstone grows in stages. Weeks 1 and 2 define the use case and produce the first RAG version. Week 3 adds tools so the project can make decisions.

Week 4 adds testing, week 5 adds monitoring and logs, and week 6 evaluates interactions and generated scenarios. Weeks 7 and 8 are for polishing, extending, and deployment. In week 9, you present the result and receive peer feedback.

I encourage starting the capstone on the first day because participants in the first two cohorts sometimes spent too long deciding what to build. Some of them didn't finish the capstone as a result. For the third cohort, I added a design-thinking framework with prompts and templates. If you already have an idea, the framework helps structure and scope it. If you don't, it gives you a way to begin without waiting for the perfect project.

The target is to have a working capstone by the end of week 6. That leaves the final weeks for refinement, testing, and presentation. The course is mostly asynchronous, with lessons, exercises, and homework taking about 3–10 hours per week depending on your background and pace. There's also one live office-hours session each week, and I record it and share a written summary.

This format is useful when watching lessons isn't enough. You build small systems, test them, observe their behavior, and evaluate whether they work. By the end, the capstone has passed through RAG, agents, and testing. It then adds observability, evaluation, and deployment rather than remaining a collection of disconnected examples.
