# The Checklist I Use to Run a Public Workshop

In April, I ran a 3-hour online workshop for 41 registered participants. I wrote
this synthetic style exercise with fictional attendee counts, tools, and
feedback numbers. The checklist helps me make every teaching and setup
prerequisite ready before people arrive.

My first public session taught me the answer by failing pleasantly. The main
example ran, but installation took 18 minutes for two participants, and I had
no short fallback prepared.

People were patient, but the ending felt rushed.

In this post, I'll share five parts of my workshop checklist:

- how I rehearse the learner's path,
- what I check in the shared environment,
- the fallbacks I prepare,
- the follow-up artifacts I publish,
- the 20-minute final pass.

## Rehearse the learner's path

I start by distinguishing the presenter path from the learner path. On my
laptop, dependencies are installed, credentials work, and the dataset is
cached. That path hides the exact problems learners meet.

Three days before the session, I create a fresh virtual machine (a clean
computer image running on my workstation). I follow only the public setup
instructions. I use a stopwatch and write down every command that waits longer
than 30 seconds.

The March rehearsal found three problems:

- a package name in the README differed from the install command,
- the sample dataset was 340 MB instead of the promised 80 MB,
- one Python version check failed on Python 3.13.

I fixed all three and repeated the clean setup, and the second pass took 9
minutes, down from 24. That's still long enough to damage a 3-hour schedule, so I added
a pre-install session 24 hours earlier.

During the main rehearsal, I speak the instructions out loud and time each
section. A section can introduce an idea, run code, and explain the result. If
it needs more than 25 minutes, I cut an example or move it to an optional
appendix. My target leaves 20 minutes unused.

## Check the environment and the room

Two days before the workshop, I run an environment test script.

The script checks these dependencies and resources:

- Python,
- Node,
- Docker (a tool for running isolated applications),
- Git,
- network access,
- disk space

It prints a version and a pass or fail result for each item.

The command looks like this:

```bash
./scripts/check-workshop-env.sh --profile public
```

The script writes `env-report.txt`, including the operating system, CPU
architecture, and available memory. Participants can paste the last 10 lines
into the chat. That gives me enough information to classify most setup issues
without a screen share.

Then I check the meeting setup with this list:

- one computer for presenting and one for chat,
- a network cable connection,
- a backup microphone,
- camera framing at eye level,
- recording settings and local storage,
- a co-host who can admit people and watch chat.

The co-host role is essential. In April, 6 people arrived without the required
API key. The co-host sent the replacement instructions while I continued the
demonstration. The delay stayed under 4 minutes.

I also post the schedule and a one-page setup guide one day ahead.

In the guide, I list install commands, the workshop repository name, and the
exact first command. In it, I also give the start time in UTC. It promises no
result the learner can't verify.

## Build fallbacks for the likely failures

For every live demonstration, I prepare two fallbacks. I record a run of the
same commands, and I save a precomputed output file plus a short explanation.
If the live path fails, I can show the evidence and continue.

My demo directory has a stable structure:

```text
workshop/
  README.md
  scripts/
  examples/
  outputs/
  recordings/
```

Before the session, I run every example, copy its expected output into
`outputs/`, and record a screen capture with no narration. The capture is
usually 2 to 6 minutes. It's deliberately boring and easy to follow.

The fallback decision is mechanical:

```text
failure under 2 minutes -> debug live
failure from 2 to 5 minutes -> switch to recording
failure after 5 minutes -> use saved output and move on
```

This removes the negotiation I used to have with myself. In the April run, a
model download stalled at 71%, so I switched to the recording after 2 minutes.
One participant later finished the download and confirmed the same result.

I prepare one more fallback for my own setup. A second laptop holds the
repository, slides, and recordings, and it's signed in as a muted co-host. I
don't treat it as a full development machine, because it only needs to finish
the session.

## Prepare follow-up artifacts

Follow-up starts before the workshop. I create a private feedback form with
five questions and a public repository. The repository has top-level folders
for setup, exercises, and solutions. In the README, I state what each folder
contains.

During the session, the co-host records timestamps for questions we postpone.

A simple note is enough:

```text
00:41 - Docker permissions on Linux
01:22 - Choosing a model size
02:14 - Testing retrieval quality
```

Afterwards, I turn those notes into issues in the workshop repository. Each
issue names the question, the time, and the answer or the plan to answer it.
This keeps good questions from disappearing into chat history.

Within 24 hours, I publish:

- the recording and chapter markers,
- slides as PDF,
- the exact repository revision,
- solutions for all core exercises,
- two optional exercises,
- a feedback form.

I fix the repository revision because the code may change later. The revision
identifier makes the recording reproducible even if the main branch moves on.

## The final 20 minutes

Twenty minutes before start, I stop editing material. Editing after that point
has caused more risk than value. Instead, I run a fixed pass.

The final checklist has 12 items:

- close every unrelated application,
- set the presenter computer to do-not-disturb,
- test microphone and camera,
- confirm recording works,
- open the repository at the fixed revision,
- open the terminal in the workshop directory,
- run the environment check,
- open slides at section one,
- open the fallback recording,
- verify the saved output files,
- give the co-host the schedule,
- put water within reach.

I also write the opening promise, the first demonstration, and the final
exercise on a paper card. If my nerves produce a blank moment, the card returns
me to the path.

In April, the final pass caught a stale Python virtual environment and a
recording folder with only 14 GB free. Both fixes took 5 minutes. Neither would
have been fun to discover live.

## Lessons From the Checklist

A workshop checklist promises attention. The material can be excellent, but if
setup consumes the first half hour, learners spend their energy recovering
confidence.

Three practices now matter most:

- rehearse from a clean machine,
- prepare a recording and an output for every live path,
- publish the exact revision afterwards.

The checklist doesn't remove judgment. I still decide when to slow down, when
to drop an exercise, and when to answer one person's question because it
represents several more. It just keeps the mechanical work from competing with
that judgment.

For the next cohort, I want to test a 30-minute optional setup call and compare
the number of first-hour problems. I'll write about that experiment in a future
article. If you want to follow along, don't forget to subscribe.
