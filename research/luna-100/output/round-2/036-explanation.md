# The autoresearch experiment loop

Autoresearch is a controlled experiment loop. It automates the repeated work of changing code, running a model, reading a result, and deciding whether to keep the change. The environment and comparison rule stay fixed while the agent explores the training code.

The project has three important files. Keep data preparation, dataset downloads, and evaluation in `prepare.py`, which the agent can't change. Put the model implementation and training loop in `train.py`, which is the file it may edit. Put the researcher's instructions in `program.md`, where the human describes how the agent should search and behave.

Before the first experiment, establish a baseline. The system creates a branch, runs the original training script, and records its metric. Without a baseline, a later number has no clear reference. The branch and commits also make the sequence of accepted changes recoverable.

Each experiment follows the same sequence:

1. The agent changes `train.py`.
2. It commits the proposal.
3. It runs training under the fixed time budget.
4. It reads the metric from the logs.
5. It keeps the commit if the metric improves and resets otherwise.

The fixed budget prevents extra computation from looking like a better model. The single metric gives the system an explicit comparison. In Karpathy's example, validation bits per byte is lower when the result is better. The loop continues by comparing each measured result with the previous one.

This creates three layers: traditional code defines the environment and evaluation, while Python code represents the model being changed.

Natural language describes the researcher's behavior. The LLM turns those instructions into edits, while the fixed evaluation setup defines success.

The approach resembles AutoML, but the search is less constrained. AutoML often selects values from predefined hyperparameters or architectures. Here the model edits the training script and can propose changes to the architecture or training procedure. That flexibility makes rollback and evaluation more important.

The same structure could apply to another experiment, such as testing writing prompts against a reference dataset and a judge. It would still need a fixed input, a metric, and a rule for keeping changes. Without those, repeated generation is activity rather than a controlled search.

The fixed files are what keep the experiment interpretable. If the agent could change the evaluator, an apparent improvement might only reflect a changed test.

This is why the baseline and rollback rule belong to the design.

The baseline and commits make it possible to look at how an accepted change affected later runs. If the metric moves in the wrong direction, the repository returns to the last accepted state.

The agent can then try a different change without bringing a failed experiment into the next comparison.
