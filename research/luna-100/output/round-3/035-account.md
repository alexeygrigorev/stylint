# Reading Karpathy’s autoresearch repository

Over the last few days, Andrej Karpathy's autoresearch project was widely shared. I read through the repository because I wanted to understand what it actually did. What interested me was the small loop connecting natural-language instructions, code changes, experiments, and a metric.

Normally, a researcher changes a training script or parameter, runs the model, and checks the result. They record the metric and decide what to try next. Autoresearch delegates that repetition to an agent. The researcher defines the environment and rules, so the agent can run for hours and explore many small changes.

The repository is small enough to understand quickly. `prepare.py` contains data preparation, dataset downloads, and evaluation, and the agent can't modify it. `train.py` contains the model and training loop, so this is the file the agent edits.

`program.md` contains the research instructions in natural language. Karpathy describes that file as "research org code written in English".

At startup, the system creates a branch, runs the unmodified training script, and records a baseline. The experiment loop then edits `train.py`, commits the change, runs the experiment, and reads the metric from the logs. If the metric improves, the commit stays. If the result is worse or unchanged, the repository returns to the previous state.

Every experiment has the same time budget. Comparisons remain meaningful even when the model or training procedure changes.

There are three layers of programming. `prepare.py` defines the rules of the environment, `train.py` is the model code being explored, and `program.md` describes how the language model should behave as a researcher.

The human writes instructions in English, and the model translates them into Python changes. That Python trains a neural network. The human is programming the experimental process rather than editing every model change directly.

The constraints matter because the example uses one evaluation metric, validation bits per byte, where lower is better, and a fixed budget for each run. Karpathy reported 110 successful changes in about twelve hours, moving the metric from 0.862415 to 0.858039. He also said much of his recent effort went into improving the experimental setup.

Other people are applying the approach elsewhere. Autosearcher runs experiments in parallel and shares discoveries, while AutoVoiceEvals applies an iterative loop to prompt optimization with adversarial evaluation. The common idea isn't that an agent can research without supervision. It's that a person can define boundaries within which the agent can explore.

The repository made that boundary visible to me. The agent can change the training code, but the person still chooses the data, metric, and time budget. The fixed evaluator is what lets me understand the reported improvement as an experiment rather than simply a large amount of generated code.
