# What I Changed When 2026 03 16 Karpathys Autoresearch Went Viral Became Too Much

I started working on 2026 03 16 karpathys autoresearch went viral because there was a concrete problem in front of me. The first version was useful enough to try, but it also showed where the workflow was becoming uncomfortable. This is what I changed, and what I learned from the result.

I did not begin with a large architecture. I followed the friction in the existing process. When one step became expensive, confusing, or repetitive, I looked for a smaller change that would remove that particular problem.

At one point, Over the last few days, [Andrej Karpathy]’s [autoresearch project] has been widely shared and discussed. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. Many people on X (Twitter) are exploring the idea and trying to apply the same pattern to their own projects. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. I looked through the repository and decided to write a short note explaining what the project actually does and why it is attracting so much interest. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. Core Idea At a high level, autoresearch automates something that normally takes a large amount of human time: running experiments and iterating on models. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. In a typical workflow, a researcher modifies the training code or parameters, runs an experiment, evaluates the result, logs the metrics, and then repeats the process. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. Autoresearch delegates this entire loop to an agent. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. You start the system, let it run for hours, and it performs many small experiments on its own, gradually improving the model. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. Conceptually, this resembles AutoML, where algorithms search through hyperparameters and architectures. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. The difference is that autoresearch uses an LLM to perform the search directly in code. I kept this part visible because it explains the decision rather than only describing the final shape.

The next detail mattered as well. Instead of selecting parameters from predefined spaces, the model edits the training script itself and proposes new ideas for the architecture or training procedure. I kept this part visible because it explains the decision rather than only describing the final shape.

This sequence also explains what the approach does not promise. A working example can be appropriate for its context without becoming a universal recipe. The constraints, inputs, and evaluation method still matter, so I would keep them next to any claim about the result.

I prefer this kind of workflow because it leaves a trace of the reasoning. Someone reading it can see what was fixed, what remained manual, and which parts can be changed independently. That is more useful than a polished description that hides the tradeoffs.

There is no need to add a dramatic conclusion here. The useful result is concrete: the source describes a particular problem, a set of decisions, and an outcome with limits. Those details are enough to reproduce the idea or decide that a different approach fits better.
