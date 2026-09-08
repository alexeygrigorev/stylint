# How the autoresearch loop works

Autoresearch is easier to understand as a controlled experiment loop than as a mysterious autonomous researcher. The project, created by Andrej Karpathy, automates the repeated work of changing code, running a model, reading a result, and deciding whether to keep the change. The important part is that the experiment has a fixed environment and a clear test for improvement.

Start with three files. Put the parts that define the experiment in `prepare.py`: data preparation, dataset downloads, and evaluation. Keep this file fixed so the agent cannot make the task easier by changing the test. Put the model implementation and training loop in `train.py`. This is the artifact the agent is allowed to modify. Finally, put the researcher’s instructions in `program.md`. This is where the human describes how the agent should search and behave.

Before searching, establish a baseline. The system creates a new branch, runs the original training script, and records its metric. Without this step, a later number has no useful reference. The baseline also makes the first accepted change part of a visible history rather than an unexplained final state.

Each experiment then follows the same sequence:

1. The agent proposes a change to `train.py`.
2. It commits the change so the experiment has a recoverable identity.
3. It runs training under the fixed time budget.
4. It reads the metric from the logs.
5. It keeps the commit when the metric improves and resets the repository otherwise.

The fixed budget matters. If one experiment could run longer than another, an apparent improvement might only reflect more computation. The single metric matters for the same reason: the system needs an explicit comparison. In Karpathy’s example, validation bits per byte is used, and a lower value is better. The loop can continue because every proposal has the same basic decision: did the measured result improve?

This creates three layers. Traditional code defines the rules. Python code represents the model being changed. Natural language describes the researcher’s behavior. An LLM translates that last layer into code edits, but it does not decide what counts as success. That definition remains in the fixed evaluation setup.

The pattern resembles AutoML, but the search space is different. AutoML often chooses values from predefined hyperparameters or architectures. Here the language model edits the training script itself and can suggest changes to the architecture or procedure. The flexibility is useful, but it makes the fixed environment and rollback rule more important.

The same shape could apply outside model training. A writing experiment might modify a style guide, generate samples, compare them with reference texts, and retain a change only when a similarity score improves. Possible signals include embeddings, a classifier, or an LLM judge. That would still require a dataset, a metric, and limits. Without those, repeated generation is only activity, not a controlled search.
