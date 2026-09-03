# Figuring Out Why a Server Ran Out of Disk Space

For this synthetic style exercise, the server, measurements, and dates are fictional. At 02:14 on April 8, 2026, monitoring paged me for a small Ubuntu server that hosts two course tools and a personal API. The root filesystem was at 98% capacity. The application still responded, but file uploads failed and background jobs stopped writing logs.

In this post, I'll share:

- what I preserved before deleting anything
- how I found the actual growth
- what had filled 68 GB
- which retention rules I added
- what monitoring missed

## Preserve before cleanup

My first rule was to collect evidence before removing files. I had already lost a useful inode count once by running cleanup during an unrelated outage, so I kept the commands short.

I logged timestamps, `df -h`, `df -i`, and mount points. Then I saved the output of `du -xh --max-depth=2 /` to a file under `/root/forensics`. That directory lived on the same full filesystem, but the report needed only 41 KB.

Finally, I listed the ten largest open deleted files with `lsof +L1`. A process can hold a deleted log file and keep consuming space. Restarting the wrong service at the wrong moment can erase the clue.

The evidence directory ended up with a short timeline:

```text
02:14 page: root filesystem at 98%
02:17 captured df, inode, and du reports
02:21 identified 15 GB in Docker writable layers
02:29 truncated one runaway container log
02:34 root filesystem at 51%
```

That sequence mattered more than any single command. When I later wrote the retention script, the timeline showed which growth source returned first and which cleanup action was safe.

## Narrowing the search

The `du` summary showed 68 GB under `/var`, with 54 GB under `/var/lib`. Drilling one level deeper pointed to Docker's directory. A second pass on `/var/lib/docker` showed 39 GB in image layers and 15 GB in container writable layers.

That number still looked strange. The application images were about 900 MB each, and only three versions should have been present. I inspected each container and image with `docker system df -v`. Two abandoned experiments from January had created 11 GB of build cache, and one container had accumulated 14 GB of logs in its writable layer.

The last 4 GB came from a Postgres volume. That was normal for its dataset, so it didn't need emergency attention.

## Immediate recovery

I needed enough space for uploads before doing a careful image cleanup. I truncated the runaway container log through its file descriptor, then restarted that container. This released 14 GB without deleting the application volume. The rule I took from an earlier incident held: the agent should never have direct access to production. I made the command myself and checked the target twice.

Then I removed build cache for the two January experiments and pruned dangling image layers. `docker system prune` alone reclaimed another 11 GB. I avoided `--volumes` because the database and upload volumes were exactly what I wanted to preserve.

Within 20 minutes the filesystem was at 51%, and uploads worked again. The background jobs also began writing normally.

## Retention rules

Emergency cleanup is only a delay if growth returns.

I wrote a small script that reports and enforces four limits:

- keep at most three application image tags per service
- prune build caches older than seven days
- rotate application logs at 100 MB and keep five rotations
- fail a nightly check if root use passes 80%

The script runs from systemd and writes a summary to `/var/log/disk-retention.log`. It uses `docker image prune --filter "until=168h"` and calls `logrotate` with a project-specific configuration. It never touches named volumes.

For the course tools, I also moved raw upload files to object storage after processing. The server keeps metadata and a 14-day local cache. That reduced the upload directory from 9 GB to 1.2 GB over the following month.

I tested the retention path on a copy before enabling enforcement:

```bash
sudo /usr/local/bin/disk-retention --report-only
sudo /usr/local/bin/disk-retention --prune-dry-run
```

The first run listed 22 unused image tags and 4.1 GB of eligible build cache. The dry run printed every deletion without touching it. Only after those reports looked safe did I allow the nightly service to enforce the rules.

I also ran one restore test for the upload cache. I copied a processed file back from object storage, compared its SHA-256 checksum with the archived original, and confirmed the course page served it correctly. That test took eight minutes and turned the storage move from an assumption into a verified path.

## Monitoring gaps

The 90% disk alert worked, but it fired too late for a 14 GB log. Disk usage had been rising steadily for eleven days. A simple trend check would have warned me two or three days earlier.

I added a second alert at 75% and a daily growth report. The report lists the five largest directories and compares them with yesterday's snapshot. I also added a check for deleted files still held open by Docker.

Two smaller warnings had been visible before the incident. A health endpoint took 1.9 seconds instead of its usual 180 milliseconds, and one job retried because it couldn't write a temporary artifact. Neither alert was tied to disk. They're now part of the same dashboard.

I recorded the incident in the team's operations notebook. The entry includes the evidence files, the cleanup commands, and the four retention rules. I also added a short decision note explaining why I avoided `--volumes`: the database and upload directories were the only irreplaceable state on the server.

## Lessons Learned

Disk failures are usually retention failures. I allowed something to grow until it collided with something else.

My sequence is now stable. I capture evidence, release space from the safest large consumer, then fix retention. The before-and-after report explained the growth better than the freed disk did.

I'll describe the nightly retention checks in more detail later this year. Subscribe for future infrastructure notes.
