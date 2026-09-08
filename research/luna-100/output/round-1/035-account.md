# Reading Karpathy’s autoresearch repository

Over the last few days, Andrej Karpathy’s autoresearch repository has been shared widely. I was curious about what was actually in it, so I read through the code and the surrounding explanation. I’m a reader of the project, not its creator. What interested me was the small loop connecting natural language instructions, code changes, experiments, and a metric.

Normally, a researcher changes a training script or a parameter, runs the model, checks the result, records the metric, and decides what to try next. The human repeats this process. Autoresearch delegates the repetition to an agent. The agent can run for hours, make many small proposals, and keep exploring while the researcher has defined the environment and the rules.

The repository is small enough that its structure explains the idea. `prepare.py` contains the fixed parts: preparing data, downloading the dataset, and evaluating a run. The agent cannot change this file. `train.py` contains the model and training loop, and this is the file the agent edits. `program.md` describes how the agent should behave in ordinary language. Karpathy calls this natural-language layer “research org code written in English.”

At startup, the system creates a branch, runs the unchanged training script, and records a baseline. Then the loop begins. The agent edits `train.py`, commits its change, runs the experiment, and extracts the metric from the logs. An improvement is kept. A result that is worse or unchanged causes the repository to return to the previous state. Every run has the same time budget, so comparisons remain meaningful even when the model or training procedure changes.

There are three kinds of programming here. `prepare.py` defines the rules of the environment. `train.py` is the code being explored. `program.md` tells the language model how to act as a researcher. The human writes instructions in English, the model turns them into Python changes, and that Python trains a neural network. The human is programming the experiment rather than editing every model change directly.

The constraints are what make the loop useful. There is one evaluation metric, a fixed budget, and an automatic decision about whether a commit survives. In the example, the metric is validation bits per byte, where lower is better. Karpathy reported 110 successful changes in roughly twelve hours, with the metric moving from 0.862415 to 0.858039. He also said much of the work went into improving the experimental setup.

People are already trying related ideas. Autosearcher runs agents in parallel and shares discoveries. AutoVoiceEvals applies the loop to prompt optimization with adversarial evaluation. I found the pattern interesting because the agent is allowed to explore, but only inside boundaries chosen by a person.
