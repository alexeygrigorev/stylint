# The Launch Checklist for a Small AI Project

Last week a fictional legal-technology tool called ClauseDeck reached its first paying users. It summarizes supplier contracts and flags clauses that differ from a customer's playbook. The application was working in demos, but launching it exposed three processes I had treated as someone else's job.

I wrote this synthetic style exercise because this article is part of a writing experiment. Project names, dates, measurements and costs are fictional.

In this post, I'll share:

- how I turned usage notes into product documentation
- how I supported the first users without a support desk
- which monitoring and rollback switches I added
- what the checklist looked like after launch
- where the process still needs work

## The Launch Gap

Two engineers had built ClauseDeck in eleven weeks. The parser covered 42 legal templates, and the review screen let a lawyer compare the model's flags with the original text. Twelve people from two fictional firms agreed to use it during a four-week pilot.

Our first launch note said the product was available and linked to the sign-up screen, but that was insufficient. Within two days, users asked how to upload a password-protected PDF, what happened to rejected files and whom to contact when a flag looked wrong.

The first attempt at an answer was a long message in the shared chat. It helped the person who asked, but the next user asked the same question the following morning. The rule I took from it was simple: a small launch still needs published answers.

## Write Usage and Support Docs

I reviewed the demo notes and found 31 questions. Seven appeared more than twice, so those became the first documentation tasks. I grouped the remaining questions into upload behavior, model limits, data retention and billing contact.

Each usage page follows the same structure:

- the task the user wants to finish
- the file formats and size limits
- the numbered steps in the application
- the expected result and next action
- the most likely failure message

On the support page, we list the shared mailbox, the business hours, the request details and the response target of one business day. We also state that customer documents remain inside the project workspace for 30 days before deletion.

I tested every numbered step against version 0.9.4, and the comparison found two inconsistencies. The upload screen accepted files up to 25 MB, while the documentation promised 10 MB. The clause export button only appeared after a review, although a support note implied otherwise.

## Prepare Questions and Escalation

We kept a private FAQ beside the deployment configuration. Each entry has the exact user phrasing, the answer for support, the underlying condition and the version where the behavior was verified. Twelve entries were ready before launch, and nine more appeared during the pilot.

The escalation list has three levels:

- product questions go to the on-call engineer
- model-output concerns go to the reviewing lawyer
- confidentiality concerns go to the customer contact recorded during onboarding

Every ticket begins in a plain spreadsheet with these columns:

- company and date
- application version
- template type
- short summary
- answer and status

That structure is dull, but it made weekly triage possible without buying a ticketing system.

I also wrote three saved replies, each aimed at a common first response. One asks for the document identifier and template type. One explains that the parser skips scanned pages and suggests running OCR first, while the third confirms receipt and names the reviewer's next response window. These replies cut the first response time from about seven hours to under two hours in the second pilot week.

## Monitor the Important Paths

The first monitoring setup only checked whether the web server responded. That missed the failure users actually saw: an upload succeeded, background parsing failed and the review screen stayed empty. We added an event for each state change instead.

The dashboard now tracks four measurements:

- uploads received per hour
- parsing success rate over 30 minutes
- queue age in seconds
- reviews completed per business day

An upload that hasn't reached the parsed state after 90 seconds raises a warning. We page the on-call engineer when the parsing success rate stays under 92% for 30 minutes. The thresholds came from the two weeks before launch, when parsing succeeded for 97.8% of the 1,140 test documents.

We log application version, template identifier, parser duration and validation errors. The prompt configuration has a version identifier too, so we can compare output samples from two prompt versions.

## Plan Rollback and Recovery

The deployment includes three switches. Feature flags can disable bulk upload, automatic clause suggestions and the customer-visible export. The parser Docker image has a tagged previous version, and the database has a nightly backup plus point-in-time recovery.

Before launch, we practiced two incidents in a staging environment. In the first, we rolled the parser back from image 2026-08-14 to 2026-08-07. The rollback took 4 minutes. Customer records remained intact, but 18 queued documents had to move back to the pending state by hand.

In the second practice, we turned off automatic suggestions. Reviewers could still read contracts and add comments, so the application stayed usable.

In the recovery guide, we assign these actions:

- the on-call engineer confirms the failing version and chooses a switch
- the second engineer checks the queue and database state
- the customer contact receives an update within 30 minutes
- the reviewer samples model output after service returns

## The Checklist

The working checklist covered documentation, support, monitoring and rollback.

Before launch, we completed 19 of the 22 checklist items. The last three involved a customer playbook import, written retention confirmation and a four-user load test.

Seven items changed after launch, and the strongest addition defined the supported document types. The weakest told us to notify users without naming the audience, channel or timing.

The pilot produced no data loss. One customer found a parser defect in a template with nested definitions, and 5 of 46 flagged clauses needed the reviewer's correction. Those small numbers gave us a baseline for the next release.

## Closing Notes

The checklist did its best work before launch. It forced us to name an owner, a message and a test for each operational failure. That preparation made the launch feel like a scheduled change.

I need a better release-specific checklist next. Each new parser version should include its supported templates, regression documents, output sample and rollback note.

I'll write more about the reviewer feedback in another article. Subscribe to stay updated.
