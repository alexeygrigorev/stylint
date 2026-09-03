# Running Batch Jobs with a Local Model Overnight

I wrote this synthetic style exercise as a build log. Project names, measurements and costs are fictional.

Last month I had 412 fictional support emails from a course platform called CourseDesk. I wanted drafts for a private knowledge base. Each draft needed a summary, three recurring questions, a suggested task and a confidence rating.

Sending all 412 messages to an API would have cost about $6 with a mid-size hosted model. I already had a used RTX 4090 in an Ubuntu server with Ollama installed. I chose to run the job overnight with Llama 3.1 8B Instruct.

In this post, I'll share:

- how I built the input queue
- why checkpointing became the main design choice
- how I validated the generated output
- what the run cost in time and electricity
- what still breaks when I reuse the workflow

## The Overnight Backlog

The emails arrived over 19 weeks. Some threads contained a single question, while others had eleven replies, forwarded stack traces and customer names in signatures. The average thread was 1,800 tokens after cleaning.

My first attempt processed all messages in one Python script. It read a JSON array, called Ollama in a loop and wrote one large JSONL file at the end. After 47 items, the SSH session disconnected. The model state disappeared, and the script had saved nothing.

That mistake was mine, and a nine-hour run needs restartable state. The rule I took from it was simple: a long job may lose its process, but it should never lose its completed work.

The next version had a simple architecture:

- `clean_emails.py` reads the export and writes one normalized JSON object per thread
- `batch_runner.py` reads a queue table, calls Ollama and updates each row
- `validate_drafts.py` rejects malformed output and returns it to the retry queue
- `report.py` counts successes, failures, tokens and wall-clock time

## Queue And Checkpoints

I used SQLite because the job had one writer and I wanted transactional state. The database contains 412 rows with fields for status, attempts, cleaned tokens, model output and validation errors. Each completed item commits immediately.

The runner takes a thread from the queue, formats it with a fixed prompt template and calls Ollama through its HTTP API. The prompt asks for JSON only. If the response fails to parse, the row gets a validation error and an attempt count.

I added two safety limits before starting the full run. A thread over 6,000 cleaned tokens goes to a separate review queue. A row with three failed attempts stops and waits for human attention. Neither limit fired during the overnight run, but the oversized-thread rule caught 14 cases in testing.

For resumption, the command is deliberately dull:

```bash
uv run python batch_runner.py --queue coursedesk.db --limit 50
```

If the process stops, running it again skips successful rows. That behavior turned a failed connection from a disaster into a non-event.

## Output Validation

The first test batch of 20 threads looked plausible. The second batch contained empty question arrays, invented policy names and one confidence value of 1.7. Plausibility was a poor acceptance test.

I therefore checked the structure before judging the content. The validator requires four fields, two to five questions, a nonempty task, a confidence value from 0 to 1 and no unresolved placeholders. It also rejects any response containing an email address, because I wanted the internal drafts to be safer for sharing.

Every generated draft also has a source list with message identifiers. If the model says the customer requested a refund, that claim must reference at least one message ID. A separate script checks those IDs against the original export.

After the run, I sampled 40 outputs. I marked 31 usable, 6 needing edits and 3 unusable. Most edits removed broad recommendations and replaced them with a concrete documentation task. The local model was good at finding repeated phrasing and weaker at deciding what the team should change.

## Costs And Runtime

The full job took 7 hours 51 minutes and processed 395 of 412 threads automatically. Eleven rows stopped after three attempts, and six remained in the oversized review queue.

The server drew about 390 watts while the GPU worked. Berlin household electricity at a fictional 0.34 EUR per kWh put the run at roughly 1.04 EUR. Startup, validation and sampling added another 50 minutes of my time.

The API comparison is more complicated than the electricity number. A hosted model produced better summaries on my 20-thread sample, especially for ambiguous threads. It also finished in 22 minutes and cost $0.31 with a smaller model. The local run won on privacy, reproducibility and the freedom to rerun 412 prompts without thinking about the bill.

I stored the model output, prompts, database and validation report in one dated directory. Rerunning version 3 of the prompt on the same cleaned input is straightforward.

## Remaining Failure Classes

Two failure classes remain in the workflow. In the first, threads that mix several unrelated problems produce generic tasks. The model summarizes each topic, but it won't choose the most urgent one. Second, the confidence score isn't calibrated. A 0.9 can mean an obvious password reset, while another 0.9 can describe a confusing billing thread.

I currently use routing rather than more prompting.

The routes are mechanical:

- obvious threads can publish after a human spot check
- mixed threads go to a triage queue
- anything below 0.55 gets a second pass with only the final three messages

The retry pass improved 9 of 17 ambiguous drafts in a small test. It also made two drafts more generic, so I don't plan to apply it automatically to every low score.

## Closing Notes

The valuable design was the queue, not the prompt. Checkpoints, validation errors and source links made the output reviewable. The model filled in repetitive structure, while the database and tests protected the process.

For hundreds of private documents, the local path is now my default first pass. For twenty documents that need publication, I would probably pay for the better hosted output.

I'll write more about the retry queue in another article. Subscribe to stay updated.
