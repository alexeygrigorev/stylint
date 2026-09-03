# Running a Tool Integration Spike Before Building the Feature

Last October, I planned a fictional invoicing feature that needed OAuth, PDF generation, and webhook retries. The estimate ranged from three to eight days because nobody had proved that the three parts worked together. I ran a two-day spike first, and the later feature took five days.

The vendor choices, code, costs, and dates are invented for a synthetic style exercise. A spike is useful because it tests the riskiest path before the project builds the comfortable parts around it.

In this post, I'll share the spike process:

- how I defined success before writing code
- why the first integration path failed
- the smallest working path I kept
- how I recorded costs and latency
- when I stopped the spike
- what moved into the real feature

## Define success first

I wrote a one-page file called `spikes/2026-10-14/invoice-goal.md` before opening a code editor. It contained the outcome, constraints, and stop time. The most important sentence said the spike would succeed only if a signed-in test account could create a draft invoice and render it to PDF. It also had to receive a payment webhook.

The constraints kept the spike honest. It had to use the production-like sandbox accounts, store no real customer data, and run from one command. It could leave temporary code in place, but each external call had to log duration and request ID.

I also set a stop time of 12 hours over two days. That limit mattered because integration work expands to fill every available hour. If the path failed, the correct output was a written reason and a second candidate, rather than a heroic rewrite.

The success rules were deliberately concrete:

- OAuth completes in the sandbox without storing a raw token
- PDF output opens at A4 size and includes a test tax line
- a fake payment webhook updates the invoice state within 5 seconds
- the whole path reruns from one shell command

I shared those rules with the fictional project sponsor. That turned the spike from an exploration into a test with a pass condition.

## Test the obvious path

The first path used a hosted identity service, a PDF library I already knew, and the payment vendor's webhook SDK. I expected the OAuth step to be easiest because I had used that identity service before.

I was wrong about that first step. The hosted service supported the authorization-code flow, but the invoicing sandbox required a audience parameter that the SDK hid. I spent 90 minutes reading generated client code before I found the setting. After that, authentication worked, but the token refresh request still returned a 401 on the second call.

The PDF step worked in 20 minutes. It generated a 61 KB invoice with the correct test tax line. I could have treated that as enough and moved on, but the goal required the full path.

The webhook step exposed a second issue. The vendor signed payloads with a timestamp prefix, while our test handler expected only a hexadecimal signature. Verification failed, and retries made it harder to see the first error. I stopped at hour six and wrote up both failures.

## Build the smallest path

The next morning, I removed the hosted identity service and used the vendor's simpler OAuth client. It exposed the authorization URL as data, so I could add the audience parameter directly. It also stored refresh tokens in its own sandbox vault.

The code was short:

```python
client = InvoiceOAuth(
    client_id=settings.client_id,
    redirect_uri=settings.redirect_uri,
    audience="invoice-api-sandbox",
)
token = client.exchange_code(code)
```

That path completed authentication in 35 minutes, including reading two vendor pages. It accepted a vendor-managed vault, which meant less control during local testing. For the spike, I accepted that tradeoff because the alternative was reimplementing refresh behavior.

I reused the working PDF function and replaced the webhook handler with a lower-level verifier. It read the raw request body, parsed the timestamp prefix, and compared the signature with a constant-time check. The fake webhook updated invoice state in 740 milliseconds.

## Measure the real costs

The spike produced numbers I could use in the estimate. The working path used two services instead of three, and I estimated recurring cost at about $19 per month, down from about $29. The identity service's fixed minimum caused most of the reduction.

Latency also changed in the next path. The hosted identity service added 220 milliseconds to token retrieval, while the vendor OAuth client averaged 90 milliseconds. PDF generation took 480 milliseconds, while webhook verification took 6 milliseconds. End-to-end payment confirmation still depended on the vendor and varied from 1.2 to 4.8 seconds in the sandbox.

I recorded the numbers in `spikes/2026-10-14/results.md`:

- two external services, down from three
- 11 minutes median time to create a draft invoice
- 61 KB median PDF size
- 740 milliseconds median webhook update
- $19 per month recurring tool cost

The numbers weren't precise production forecasts. They were enough to compare paths and explain why the invoice feature estimate was five days rather than three.

## Stop and write the decision

At hour nine, the full path passed every success rule. I stopped there even though two edge cases remained unhandled. The spike goal was to prove the risky path, and production hardening belonged to the feature.

I wrote a short decision record with the usual three sections. The unknown list included refunds, multi-currency invoices, and webhook replay behavior, and those items became tickets instead of surprise work.

The decision record also named the accepted downsides. I gave up some control with vendor-managed tokens, and the lower-level webhook verifier required our own tests. The PDF library added 38 MB to the container image. Each downside was easier to accept beside the measured benefit.

## Move it into the feature

The feature reused the OAuth wrapper, PDF renderer, and webhook verifier from the spike. I rewrote the temporary CLI as a FastAPI endpoint, added PostgreSQL storage, and put retries behind a queue.

The queue used exponential backoff at 1, 4, and 16 seconds, then moved failures to a dead-letter table. The spike had already shown that some webhook failures were transient, so the feature could define retry behavior instead of guessing.

Tests followed the same seams. A fake OAuth server tested the audience parameter, while a fixture PDF checked the tax line and page size. A signed webhook fixture tested both valid and expired signatures. Those tests covered the parts most likely to break after a vendor update.

The useful habit was stopping after proof. A spike answers a narrow question with the smallest runnable path. It should produce evidence, a decision, and tickets, rather than becoming the first accidental version of the feature. If I continue this exercise, I'll write about the webhook replay tests that stayed unknown after the spike. Subscribe if you want that follow-up.
