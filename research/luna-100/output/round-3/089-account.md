# Building an Evaluation Habit for Agents

Across 4,894 AI engineering job descriptions collected for the AI Engineering Field Guide, evaluation appeared as the number one skill. Building an agent is easy enough. I provide an API key, instructions, and tools.

Making sure it behaves reliably is harder because an agent can fail in many unrelated ways.

It can give a wrong answer, hallucinate confidently, or stop without answering. It can also repeat a tool call, exhaust its context, or send invalid arguments. Without evaluations I can't tell whether a change improved the system or broke an unrelated case.

I treat evaluation as a progression rather than as one prompt sent to an assistant.

I begin with a manual vibe check and log the interactions immediately. After ten or fifteen examples, I build a small labelling tool and classify each result as good or bad myself.

This first gold-standard dataset is small, but reviewing it shows me what the agent actually does. I don't delegate that judgment to a coding assistant.

Then I align a judge. I ask an assistant to classify the same records, compare its decisions with mine, explain disagreements, and create a generic `judge.md`.

I read the rules to make sure they describe the behavior I care about rather than memorizing the examples. A fresh subagent reads only `judge.md` and classifies the dataset. I keep refining the rules until the judge usually agrees with me. The fraction of good results becomes a metric.

The first examples aren't enough, so I borrow test ideas from QA. Equivalence partitions divide the input space into groups that should behave similarly.

For a RAG agent, I use groups such as:

- documented questions
- relevant topics outside the documentation
- irrelevant questions
- ambiguous wording
- other languages

I write two or three questions for each group.

Boundary testing adds cases at the edges of those groups. I use exact matches to documents, semantically related questions with different words, questions that match several documents, and completely off-topic requests.

I run the enlarged dataset through the agent and judge, then compare the judge's decisions with mine. Full agreement isn't realistic, but the judge should be correct most of the time.

Once evaluation is automated, one process can implement a change while another runs the judge. Every change runs against the full dataset so regressions stay visible.

I also generate synthetic questions from documents in the knowledge base. They add coverage, but they don't replace cases that came from real use. When a synthetic case exposes a failure, I add it to the gold set.

Real users provide more cases. Logs, corrections, thumbs-up and thumbs-down feedback, and conversations where someone supplies missing information reveal failures I didn't imagine.

Online evaluation can score that traffic with a standalone judge and display results on a dashboard. I periodically look at bad examples and add them to the gold set.

One judge is enough to begin. Later I can measure task completion, correctness, and groundedness separately.

I can also measure completeness, instruction following, and tool trajectory. The dataset stays unfinished because every new failure gives me another case to evaluate.
