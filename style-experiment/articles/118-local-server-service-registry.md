# Keeping Track of Services on My Home Server

I wrote this synthetic style exercise as a build log. The server, services, ports, dates and measurements are fictional.

My fictional home server named `atlas` runs 27 services for file sync, photo backups, home automation, media processing and three small websites. In January, a media transcoder stopped after I changed a Docker Compose file. A new service had taken port 8090, and the old one had exited quietly.

The outage lasted 11 hours while I was away. Fixing it took four minutes once I looked at the logs. The larger problem was inventory.

I had no record of where each service should run, who owned it or how to test its health.

In this post, I'll share:

- how I inventoried 27 existing services
- how I standardized service names and ports
- how I added logs and health checks
- how the registry catches changes now
- what still needs manual review

## The Inventory Started as a Spreadsheet

The obvious first attempt was a spreadsheet. I spent two hours in front of Docker output, systemd output and three old notes. The result had 27 rows, 14 blank owners and 9 uncertain ports.

The spreadsheet was useful for one weekend, but by February it disagreed with reality. I had added a `paperless-ngx` container and changed a backup scheduler, but neither change made it into the file because nothing forced an update.

I needed the registry close to the changes. A spreadsheet could document the server, but it couldn't participate in the deployment.

## Names and Ports Get One Home

I moved the registry into version control as `services.yaml`. Every service gets a stable slug, display name, owner and port. It also declares a Compose project and health URL.

The first 27 entries exposed several conventions I had been applying inconsistently:

- slugs use lowercase words and hyphens
- web interfaces live in 8100 through 8199
- exporters live in 9100 through 9149
- internal APIs live in 8800 through 8899
- one service may expose one HTTP port in the registry

The YAML entry for the photo backup is short:

```yaml
- slug: photo-backup
  name: Photo backup
  owner: martin
  port: 8124
  compose_project: backups
  health_url: http://atlas.local:8124/healthz
```

`martin` is a fictional family member who uses the service. The owner notices problems and can accept a maintenance window.

Reassigning ports took another evening. I stopped conflicting containers, edited 11 Compose files and restarted services in small groups. I updated two client URLs manually and left redirects in Caddy for 30 days.

## Logs and Health Checks

Each service now declares two checks. The process check verifies that the container is running or that the systemd unit is active. The HTTP check requests the declared health URL.

For services without a health endpoint, I added a tiny health handler in Python or used the existing `/health` route. The registry validates that a health response returns HTTP 200 and a JSON object with `status` set to `ok`. A response that takes more than two seconds counts as unhealthy.

The checker runs every 60 seconds and writes results to SQLite.

The row is intentionally plain:

```text
checked_at         service         healthy    status_code    latency_ms
2026-02-14 08:00   photo-backup    true       200            31
2026-02-14 08:00   media-cutter    false      000            0
```

A service must pass both checks for 48 hours before I mark it stable. Twenty-two services passed in the first week. Five failed at first because they answered only on localhost or returned HTML from their health routes.

## The Registry Catches Changes

The deployment wrapper reads `services.yaml` before it runs Docker Compose or systemd. The wrapper refuses to start a service whose declared port differs from the file. It also rejects an uppercase slug and a health URL that reuses another service's port.

On every push to the configuration repository, I run a separate audit:

```bash
atlas-registry validate --file services.yaml
atlas-registry compare --file services.yaml --live
```

The validate command checks schema types, duplicate ports and duplicate slugs. The compare command asks Docker and systemd for the current state and reports missing services, unregistered services, stopped registrations and port mismatches.

The first audit found nine discrepancies:

- three unregistered containers from old experiments
- two registered services that had been retired in December
- two port mismatches from local Compose overrides
- one duplicate health URL
- one service with a blank owner

I removed the three old containers and archived the two retired entries with an end date. The two overrides became explicit environment files in the repository. The audit now reports zero differences when nothing is being deployed.

## Alerts Without Noise

The checker distinguishes an outage from an expected maintenance window. A service can declare windows such as `Sun 03:00-03:20`. Failures there create a maintenance row rather than an alert.

The channel received 16 alerts in the first month. Twelve were real: failed health endpoints, container exits and certificate warnings. Four were false alarms during backups, so I raised the timeout and excluded that window.

The remaining alerts are useful. On 27 February the registry reported `photo-backup` as unhealthy 40 minutes before anyone uploaded a photo. The alert gave me time to move 84 GB of old exports off a full disk.

The registry can't decide whether a service is still needed. Its monthly report lists use and owner review, but the household makes the retirement decision.

Configuration stays honest only when deployment goes through the wrapper. I occasionally run Docker Compose by hand while testing. The audit turns a surviving change into a task.

## Lessons From the Registry

The registry still needs manual judgment. The monthly report can show that `weather-cache` is unused, but the household decides whether to retire it.

The registry works as a review tool. It forces me to name the owner, port, health URL and maintenance window before a service becomes permanent.

The system has 31 registered services now: 26 stable, three in testing and two marked for retirement. I'm adding a dependency field so the registry can warn me before a database restart affects four services.

I'll describe that dependency audit in a future post. If you want to follow along, don't forget to subscribe.
