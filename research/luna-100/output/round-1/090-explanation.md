# A Practical Evaluation Ladder for AI Agents

That shared understanding makes a metric useful in a team.

The people responsible for the product should be able to understand the examples and the decisions. Otherwise the metric may be precise without measuring the behavior anyone actually wants.

Evaluation is how you learn whether an agent works and whether a change made it better. Start small, keep human judgment close to the first examples, and gradually automate the checks without losing contact with real user failures.

First, run the agent manually and log every interaction. Ten or fifteen records are enough for a beginning dataset. Label each output yourself as good or bad. This is the first gold standard, sometimes called ground truth. Manual review is valuable because it exposes the agent’s actual failure modes before you write generic rules.

Next, create a judge that can reproduce your decisions. Ask an assistant to classify the records, discuss disagreements, and draft judge.md. The document should describe reusable rules rather than mention the exact examples. Start a new session with a subagent that reads only the judge file, then compare its output with yours. Use agree and disagree labels until the judge is aligned enough to measure the system.

To find cases beyond the initial logs, borrow two QA techniques. Equivalence partitioning divides the input space into categories with similar expected behavior. A documentation assistant might receive in-scope questions, related but unsupported questions, irrelevant questions, ambiguous questions, and queries in other languages. Add several examples for each category.

Boundary testing probes the edges of those categories. Include an exact document match, a semantic paraphrase, a question that matches several documents, and an off-topic request. These cases often expose retrieval and routing errors that ordinary examples miss. The new records become part of the gold standard and are checked by the judge.

Once the pipeline runs the agent, runs the judge, and calculates the good fraction, use it during development. An implementer can change the system and a tester can run the complete evaluation. Re-run the full set after every change so a local improvement does not hide a regression elsewhere. Synthetic questions can add coverage, but real logs remain important.

Online evaluation extends the dataset after launch. Collect user feedback and score production traffic with a separate judge. Inspect low-scoring conversations, understand the failure, and add a representative case to the gold standard. This makes the evaluation reflect how people actually use the system.

Start with one dimension and add others as the application matures: completion, correctness, groundedness, completeness, instruction following, and trajectory quality. The exact metrics depend on the problem. What matters is having a repeatable way to see what the agent does and evidence for every change.
