# Closing the Prototype-to-Production Gap in Small Steps

I wrote this synthetic style exercise as an analysis piece, and the project, numbers and dates in it are fictional. In April 2026 I turned a weekend prototype, a question-answering assistant over 2,300 archived support tickets, into an internal service that nine colleagues use daily.

The prototype took one evening and about 300 lines of Python. Production took eleven more weeks, and the gap broke into five steps that I closed one weekend at a time.

In this post, I'll share:

- persistence, because one restart wiped 60 saved conversations
- authentication, because a demo runs as one trusted user
- tests, because a demo only has to work once
- deployment, because a laptop is a poor runtime
- support, because production code has an owner on call
- what the sequence taught me about sizing steps

## 1. Persistence That Survives A Restart

The demo kept every conversation in a Python dictionary. A reboot on 14 April wiped 60 saved conversations, one of them a comparison a colleague wanted to show her team the next morning.

The fix arrived as SQLite first, about 90 minutes including the schema, and Postgres two months later when a second instance needed shared state. Each step fit into one evening, and neither required touching the answering logic. SQLite held up without complaints for those two months, and the later migration ran as one plain SQL export.

A demo that only counts requests can skip this step entirely. Mine kept user state, so persistence came first.

## 2. Authentication Before Every Request

The prototype ran on my laptop under my login, which counted as authentication at demo scale. The service couldn't stay that way once it moved to a shared host. In the first production week I put a single API key in front of it, and month three brought single sign-on.

The intermediate step mattered more than the final one. Eleven people received keys in week one, and 9 still use the service weekly. Single sign-on replaced the keys only after the user list stabilized, and the two steps never overlapped.

My mistake in this dimension was deploying a staging URL without the key. A teammate pasted real customer text into it within a day. The rule I took from it: deploy with authentication or keep the URL unshared. The steps also closed in risk order, and a shared host without keys felt riskier than any missing test at that point.

## 3. Tests That Run Without Me

I tested the prototype by clicking through three happy paths. That worked until the first schema change, which broke retrieval on 19 May and stayed broken until a user reported it.

The production version has 12 integration tests around retrieval and answer formatting. They run on every push through GitHub Actions and finish in about three minutes. The tests use a frozen copy of 40 tickets stored at `tests/data/tickets-2026-05.json`, so a score change means the behavior changed. I regenerate that file only when the archive format changes.

A test that runs only on my laptop protects nobody else. Moving it into CI was the step that made the tests real.

## 4. Deployment As A Boring Step

Deployment started as `python main.py` in a terminal window on my desk. The service now ships as a 480 MB container with a health check and a one-command rollback. A deploy takes about four minutes, and I have rolled back twice, both times in under a minute.

The gap here was repeatability. A prototype can run from a terminal for months, and nothing breaks until the day I travel and the host reboots. The container turned deployment from a personal favor into a documented step. The deploy script is 30 lines of bash, and a colleague ran it successfully on the first try in June.

One caveat belongs here: I run a single instance with no autoscaling, which is enough for nine users. At 900 users the same step would look completely different.

## 5. Support With An Owner And A Queue

A prototype has no users to disappoint, so it needs no support. The service collected 34 requests in its first production month, and 9 of them needed a human answer beyond the standard reply.

Support changed the code more than any other step. Request logging arrived in the first support week, because I couldn't answer questions about failures I hadn't seen. I also added a response-time rule: every question gets an answer within one business day, even when the answer is a promise to look later.

The queue has one owner, and that owner is me. Nine questions a month works out to about two per working week, which fits into a lunch break. Distributing the queue can wait until the volume justifies a rota, which 9 users don't justify.

## Closing Notes

Eleven weeks separate the one-evening demo from the service my colleagues use. The five steps closed the gap in order, and each one stayed small enough for a weekend or a pair of evenings.

Two things still lag behind: cost tracking happens by hand once a month, and the support queue depends on me noticing pings on my phone. Both are honest gaps for a nine-user service, and both have obvious next steps.

I'll write about the cost numbers in a future post. If you want to follow along, don't forget to subscribe.
