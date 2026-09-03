# Designing Error Messages for a Telegram Assistant

I wrote this synthetic style exercise as a build log, and all project details are fictional. In May 2026 my Telegram assistant served about 900 messages a week, and its only response to a crash was silence. Users saw a chat that stopped answering, and I saw nothing until someone complained two days later.

In this post, I'll share:

- why silent failures were worse than crash messages
- what my first generic reply got wrong
- the rules every error reply follows now
- how quiet retries cut the noise in the chat
- where the design still falls short

## Silent Failures

The assistant runs as a long-running Python process on one VPS, wrapped in systemd, the standard Linux service manager. When a handler raised an exception, the framework caught it, logged a traceback to journald and sent nothing to the chat.

The logs kept the evidence, but logs have no push channel. My mistake was treating log files as user feedback. The rule I took from it: if the chat stays silent, the user becomes your only monitoring.

I found the silence by accident. A friend wrote that the bot had ignored her evening message, and journald showed a KeyError from 22:14 the same night. During the last week of May I counted 12 crashes that users experienced without any reply from the bot. Eleven of the twelve produced tracebacks that journald kept for 90 days, and nobody read a single one in time. Two of them looked to the user like the bot ignoring a direct question, which is a rude way to behave.

## One Apology For Everything

I first wrapped the handlers in a global try/except block. Any exception produced the same chat reply: "Something went wrong".

Within two weeks that message had appeared 34 times and told me nothing on every occasion. A quota error and a database timeout got identical text, so I gave every report the same answer: restart and hope. A friend sent three messages that all failed on a rate limit, received three identical apologies and concluded the bot had died. That conversation pushed me to redesign the replies instead of patching the wrapper.

The mistake was hiding the cause behind an apology. The rule I took from it: an error reply names the cause, or it names nothing.

## Rules For Error Replies

Every error reply now follows three rules, checked against the last 40 failures:

- name the cause in plain words, such as "Telegram rate limit" or "database timeout"
- name the next action, such as "retrying in 60 seconds" or "nothing was saved"
- include a short error id so I can find the matching log line

One real reply from June looks like this:

```text
Summary failed: Telegram rate limit (429).
The summary will retry in 60 seconds. Nothing was lost.
Error id: 2026-06-04-312
```

Each error id combines a date plus a counter, and it greps straight out of journald. Support replies dropped from about two days to ten minutes, because users paste the id and I read the matching log line.

I replayed 40 logged failures from May against the new format. Every reply fits on two lines, and each one names a cause I can grep in under a minute.

## Quiet Retries

Some failures repair themselves within seconds, and announcing them is noise. The retry layer now separates transient errors from permanent ones before any message goes out.

Rate limits and timeouts retry twice with a 30-second gap, and the chat hears nothing unless both attempts fail. Parse errors and auth failures skip retries entirely, because trying again changes nothing. The layer is about 60 lines with a small counter dict, and it retries inside the handler instead of a job queue. The change cut error replies from about 30 per week to 6, and the six that remain now need a human decision.

A retry storm on 21 June produced around 400 silent retries in one night, and the chat looked perfectly healthy while the quota burned. I accepted that trade on purpose. A tiny dashboard with one counter per error id would fix the blind spot, and it stays on the backlog for August.

## Limits After Three Weeks

Multi-step tasks still confuse people. When the nightly job fails at step three of five, the reply names the step, and users still ask whether the whole task failed. The reply needs a progress line, and I haven't built it.

Quiet silence can also go too far. Retries log to journald only, so a week full of rate-limit storms looks like calm from the chat side.

The error id also resets at midnight, so two failures on one date differ only by counter. A UUID would be safer, and the counter has been enough so far.

## Closing Notes

The arc ran from silence to noise to structure: logs nobody read, then one apology for everything, then cause-plus-action replies with quiet retries. Error handling turned out to be a product surface, and it now gets the same editing attention as a feature.

Response time to unknown failures dropped from days to minutes, at a cost of about 200 lines across two modules. The next problem is progress reporting for multi-step jobs.

I'll write about that progress line in a future post. If you want to follow along, don't forget to subscribe.
