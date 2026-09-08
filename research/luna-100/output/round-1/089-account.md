# How I Started Evaluating Agents

The dataset is not a certificate that an agent is correct. It is a record of cases I understand well enough to compare after a change, and it should grow whenever the system meets a new failure.

Across 4,894 AI engineering job descriptions collected for the AI Engineering Field Guide, evaluation appeared as the number one skill. That matches my experience. Building an agent is easy enough: provide an API key, instructions, and tools. Making sure it behaves reliably is the hard part.

An agent can answer incorrectly, hallucinate confidently, stop without answering, repeat a tool call, exhaust its context, or send invalid arguments. Without evaluations I cannot tell whether a change improved the system or quietly broke an unrelated case. I therefore treat evaluation as a progression rather than a single prompt to an assistant.

I begin with a manual vibe check, but I log the interactions immediately. After ten or fifteen examples I build a small labelling tool and classify each result as good or bad myself. This first gold-standard dataset is small, but manually reviewing it teaches me what the agent actually does. I do not delegate that judgment to a coding assistant.

Then I align a judge. I ask an assistant to classify the same records, compare its decisions with mine, discuss disagreements, and create a generic judge.md. I read the rules to make sure they describe the behavior I care about rather than memorizing examples. A fresh subagent reads only judge.md and classifies the dataset. I keep refining until the judge usually agrees with me. The fraction of good results becomes a metric.

The initial examples are not enough, so I use QA ideas to create failures. Equivalence partitions divide inputs into groups, such as documented questions, relevant questions outside the documentation, irrelevant questions, ambiguous wording, and other languages. Boundary tests include exact matches, paraphrases, queries matching several documents, and completely off-topic requests. I add cases from each group and check the judge again.

Once the evaluation is automated, the agent can help improve the agent. One process implements a change, another runs the judge, and a third checks the result. Every change runs against the full dataset so regressions remain visible. I also generate synthetic questions, but I treat them as additional coverage rather than a replacement for real cases.

Eventually real users provide the most useful data. Logs, corrections, thumbs up and down, and conversations where someone adds missing information reveal failures I did not imagine. Online evaluation can score that traffic with a stand-alone judge and show results on a dashboard. I periodically inspect bad examples and add them to the gold set.

One judge is enough to begin. Later I can measure task completion, correctness, groundedness, completeness, instruction following, and tool trajectory separately. The dataset is never finished; it grows when the system meets a new failure.
