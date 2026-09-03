# Clustering Support Tickets Without Pretending They Are Clean

I wrote this article as a synthetic style exercise, and I invented the support queue, dates, and measurements. In the fictional project, I clustered 4,812 support tickets for a course platform during the first three weeks of August 2026.

The team needed to decide which support problems deserved engineering time. Reading tickets one by one was too slow. My first spreadsheet grouped messages by the page that generated them, and that method hid the most common complaint: billing.

In this post, I'll share:

- the first manual labeling pass
- how I normalized ticket text
- the clustering method and its settings
- how I reviewed mixed-intent tickets
- what changed in the support workflow

## Manual Labeling

I started with 250 tickets sampled from 4,812 messages. I read each message and assigned it one of six labels.

Billing and login were first. Video playback, certificate download, assignment upload, and "other" completed the set.

Two hours in, the sample taught me why this was hard. A single ticket often contained a login error and a billing question. Forcing it into one label lost information, so I added a second column for secondary labels.

The revised sample looked less orderly, but it described the queue more honestly. Of the 250 tickets, 71 mentioned billing, 58 mentioned login, and 39 mentioned video playback. Only 31 had exactly one concern and no related complaint.

## Normalize the Text

The raw text contained enough variation to make exact matching useless. Students wrote "payment failed", "card declined", and "money left my account twice" for related issues. I used a small Python script to normalize the text before clustering.

```python
def normalize_ticket(text: str) -> str:
    text = text.lower()
    text = re.sub(r"order[^\w\s]*s?\s+#\w+", "order id", text)
    text = re.sub(r"https?://\S+", "link", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
```

This removed payment processor IDs and URLs that made unrelated tickets look identical. It preserved sentence structure, so phrases such as "can't log in after paying" stayed intact. I kept the original message in the same database row.

I also removed 214 automated messages from subscription providers. Their wording dominated two preliminary groups and made human questions harder to see.

## Clustering Method

For the next version, I embedded each normalized ticket with a small sentence-transformer model. I chose `all-MiniLM-L6-v2` because it ran on my laptop and took about 11 minutes for all 4,812 tickets. The full run used 2.1 GB of RAM.

I used HDBSCAN, a density-based clustering method that leaves outliers unassigned. That behavior mattered because clean k-means groups would have forced every ticket into a category.

I tested three settings on the labeled sample. `min_cluster_size` of 25 produced 14 groups, 40 produced 9, and 60 produced 6. I chose 40 because it kept a separate group for playback on television browsers while still merging spelling variants of the same issue.

The resulting nine groups had these uses:

- billing and duplicate charges, with 731 tickets
- login and password reset, with 684 tickets
- video playback and browser errors, with 590 tickets
- certificate names and download permissions, with 341 tickets
- assignment uploads and file limits, with 278 tickets
- course access after payment, with 253 tickets
- mobile application crashes, with 190 tickets
- team and invoicing requests, with 166 tickets
- unassigned outliers, with 1,579 tickets

## Review Mixed Tickets

The large outlier count looked like failure until I sampled 100 of those tickets. Seventeen were one-line thank-you notes, 23 were unique account changes, and 31 combined two known topics.

The remaining 29 included typos, attachments without text, or requests for courses that didn't exist.

I didn't try to force every outlier into one exact label. Instead, I built a review table with four columns.

The columns held the primary group, confidence, secondary group, and next action. I marked a ticket "route now" when the primary group covered more than one concern.

That review changed the treatment of course access. The clustering run separated payment from login, but 83 sampled tickets asked for access after a bank had already taken payment. I gave that group its own support response and a direct handoff to the payment provider.

I also kept a 60-ticket audit sample. I checked whether the same two reviewers assigned the same primary group to each ticket. They agreed on 49 of 60. Most disagreements involved a team invoice that also mentioned login access.

## Workflow Changes

The clusters didn't replace human review. They changed where I spent attention, while support could answer playback and password questions with templates.

I summarized the results for the team in one page. It included the nine group sizes, the outlier sample, the reviewer agreement rate, and the date of the data extract. It also stated the caveat that one month of tickets may overrepresent a seasonal payment problem.

Three weeks later, the duplicate-charge group had fallen from 731 tickets in the old extract to 96 in the new week. Login volume stayed about the same. That comparison was directional because support staffing and release dates also changed, but it matched the fix we shipped.

## Lessons

Clustering made the support queue navigable. It found large groups, exposed mixed concerns, and left unusual tickets visible rather than hiding them in an "other" bucket.

My rule from this project is to sample before trusting a cluster. Group size shows volume, while a labeled sample and disagreement audit show whether the group means something you can act on.

I plan to write separately about the response templates and the payment escalation path. Subscribe if you want to see how those changes held up over a full quarter.
