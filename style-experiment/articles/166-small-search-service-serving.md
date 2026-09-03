# Serving a Small Search Index from a Tiny Server

This synthetic style exercise invents the service, incidents, and measurements. On March 3, 2026, I put a 148,000-document course index behind FastAPI. Until then, the index lived in a script I ran on my laptop. That was fine while the audience was me, but three workshop helpers needed the same search results.

In this post, I'll share:

- why I kept keyword search instead of adding a vector database
- how I made queries predictable for browser users
- what the health checks covered
- how I updated the index without stopping searches
- what changed after four weeks of use

## Why a Tiny Server

The index was only 212 MB in memory. A single virtual machine with 2 vCPU and 4 GB of RAM handled that comfortably. I had used the same class of server for three side projects, so its behavior was familiar.

The search logic used Python, DuckDB, and a small reranker. Moving it behind a service preserved the ranking I had already tested. A hosted search product might have solved operations, but I would have had to translate the ranking and pay for a second copy of the data.

I set a narrow target first: answer 95% of searches in under 120 milliseconds and serve up to 30 requests per second. That covered the workshop of 80 people and left room for normal sharing.

## Query Contracts

My first API accepted every parameter as an optional query string. The UI could send a page size of 500, a negative offset, or a topic filter shaped like `data+eng`. One test request returned 40 MB of JSON and locked the tab.

That failure taught me to publish a narrow query contract. The service now accepts these fields:

- `q`, with one to 120 characters
- `topic`, from a fixed list of 14 course areas
- `limit`, from 5 to 25 results
- `page`, starting at 1

Pydantic rejects anything outside those limits. Malformed input gets HTTP 421 with a field name and a human-readable reason. Valid search requests stay close to 2 KB.

I also fixed result behavior before users could discover every corner. Empty queries return the 25 most recently updated documents. A query with only punctuation returns the same default set and reports `applied_query: false`.

For the UI, I added three fields to each result: title, course section, and a 28-word excerpt. The excerpt uses fixed sentence boundaries rather than an arbitrary character cut. A helper corrected a title on day two, and the change took one line.

## Health Checks

The first deployment reported HTTP 200 while search was broken. The server was alive, but the DuckDB file had failed to open because of a permissions mistake. I had confused process health with feature health.

The live endpoint now performs a real query:

```text
GET /health/live
GET /health/ready
```

The first route reports that the process accepts requests. The second runs a two-word search, checks for at least one result, and verifies the index timestamp. A failed ready check removes the container from the load balancer within 15 seconds.

Every minute, a script searches four known phrases. Two are common course phrases, and two use unusual spelling. It records latency, result count, and the top document ID in Prometheus. The top ID matters because a ranking change can still return correct-looking counts.

I also added a daily fixture with 20 question-and-document pairs. The fixture checks that a known course page appears in the top five. On April 1, it caught a tokenizer update that had pushed 19 of the 20 correct pages below position 40.

## Updates Without Downtime

Course materials changed several times each week. My first update script deleted the old index and wrote a new one in place. A search arriving during that window got an error, and one student hit exactly that race.

The better design writes to a versioned directory. Each build lands in `/data/index/vN`, and a small manifest file records its checksum, document count, and creation time. After validation, the service changes one symlink. Old requests finish against the old file, while new requests open the new file.

A build takes 3 to 5 minutes. Validation loads the candidate index, runs the four probe searches, and compares 100 random query results with a snapshot. The snapshot isn't a quality judgment; it makes accidental changes visible.

I keep the previous two versions. A bad update can be restored in one command, and the manifest tells me which corpus commit produced it.

## Four Weeks in Production

The service saw 31,600 searches in its first four fictional weeks. The median latency was 38 milliseconds, and the 95th percentile was 86 milliseconds. Peak traffic reached 21 requests per second during a live workshop.

The biggest operational surprise was logging volume. Debug logs from the reranker added 1.1 GB in three days. I moved those records behind a sample rate of 2%, kept errors at 100%, and reduced daily logs to 55 MB.

The second surprise was stale browser links. Six documents changed path names, and helpers kept sending old URLs. I added redirects for those six paths and stopped renaming old pages without a redirect.

Cost stayed at €8 per month for the server and 40 GB of disk. More important, the three helpers stopped asking me to run searches for them.

## What I Learned

A small search service is mostly a set of promises: input limits, latency targets, health behavior, and rollback steps. Writing those promises down made the service easier to trust than the laptop script.

I still don't cache query results. With this traffic, the database answers quickly enough, and caching would hide ranking changes during course updates.

I plan to write about the reranker in a future article. Subscribe if you want to follow that work.
