# An Evaluation Ladder for AI Agents

Evaluation works best as a gradual process. Start close to the examples, keep human judgment in the first dataset, and automate only after the rules describe the behavior you want to measure.

Begin with manual review by asking the agent questions, looking at the results, and logging each interaction. Ten or fifteen records are enough for a first dataset. Label every result yourself as good or bad. This initial gold standard, sometimes called ground truth, shows the agent's concrete problems before an assistant turns them into generic rules.

To automate that judgment, create a judge that can reproduce your decisions. Ask an assistant to classify the same records, compare its decisions with yours, and explain disagreements. Then ask it to write `judge.md` with reusable rules rather than references to the exact examples.

Start a fresh session with a subagent that reads only the judge file and classifies the records. Compare its output with yours using agree and disagree labels. Keep refining the rules until the judge is aligned enough to measure the system.

The first logs rarely cover the whole input space. Equivalence partitioning divides inputs into categories whose members should behave similarly.

A documentation assistant might receive several kinds of questions:

- questions covered by the docs
- related questions outside the docs
- irrelevant questions
- ambiguous wording
- questions in other languages

Add a few examples for every category.

Boundary testing checks the edges of those categories.

Include these cases:

- an exact match to a document
- a semantic paraphrase using different words
- a question that matches several documents
- an off-topic request

These cases expose retrieval and routing problems that ordinary examples can miss. Add the new cases to the gold standard and run them through the judge.

Once the pipeline runs the agent, runs the judge, and calculates the fraction of good results, use that metric during development. One process can implement a change while another runs the complete evaluation. Re-run the full set after every change so a local improvement doesn't hide a regression elsewhere.

Synthetic questions can increase coverage, but real logs still supply important cases. Online evaluation continues the process after launch. Collect user feedback and score production traffic with a separate judge, then look at low-scoring conversations and add representative failures to the gold standard.

Start with one dimension and add completion or correctness first. Groundedness, completeness, instruction following, and trajectory quality can come later as the application needs them. The exact metrics depend on the problem, but every change should have evidence behind it.
