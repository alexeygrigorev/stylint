# Turning Voice Notes into Captions for Screenshots

I invented Shelfcount, an inventory app, and all 121 screenshots for this synthetic style exercise. In the fictional 12 May 2026 session, I reviewed the images after store visits and couldn't remember why 30 of them existed. Their original context was still in my head that day, and it was gone by the next week.

In this post, I'll share:

- why filename captions failed
- how I capture context while taking a screenshot
- how voice notes become short captions
- how I filter names and sensitive details
- how the same caption adapts to different publication surfaces

## Filenames Lost the Useful Context

My original workflow named files with a timestamp and project prefix. A file called `shelfcount-2026-05-12-1032.png` told me when I took the image, and nothing about the screen, store, or decision.

I tried adding text captions immediately after each capture. That worked for three screenshots and failed on a 40-minute store walk. Stopping to type interrupted the task, so I skipped captions and promised to write them later, but later usually meant never.

The missing context was specific. Two screenshots looked identical, but one showed a scanned barcode that loaded slowly, while the other showed the fallback screen after a scanner timeout. A generic caption would hide the difference that mattered.

My rule from that week was to capture the observation at the same time as the image, even if the first version is rough.

## Capture While Reviewing the Screen

I now keep the screenshot and a voice note together in one intake folder. Each note lasts 10 to 25 seconds and contains the same six fields rather than a polished script.

A Shelfcount note sounds like this:

```text
Shelfcount, Northside Market, aisle scanner. This is after scanning the
second damaged label. The price shows quickly, but stock count stays
empty until refresh. Keep this if we change the loading state.
```

The note contains the same six fields:

- project
- place
- screen
- trigger
- observed behavior
- possible decision

Those nouns do most of the work later, so I don't try to write a polished sentence while walking.

The folder receives two files with the same minute-level timestamp:

- `2026-05-12-1032-shelfcount.png`
- `2026-05-12-1032-shelfcount.m4a`

When the timestamps differ, a pairing command asks me to match them. It doesn't guess, because one wrong pairing is more expensive than two quick confirmations.

I record 78 paired notes across the Shelfcount review. That number excluded 14 screenshots taken for unrelated invoices, which I filed in their own project folder.

## Turn Speech Into a Draft Caption

At my desk, Whisper runs locally and produces a transcript for each audio file. A small Python script then asks a local model to compress the transcript into a caption of at most 140 characters.

The script enforces three rules:

- keep the concrete nouns
- state the observed behavior
- remove filler and greeting words

The 25-second note above became this caption:

```text
Northside Market aisle scanner after a damaged-label scan: price loads, stock count remains empty until refresh.
```

The caption is longer than a filename, and it answers the questions a future reader will actually have. It also preserves "damaged label", which separated the image from the normal scanning flow.

I review every caption before it enters the project catalog. I accept automated transcription here because the notes are short, the vocabulary is stable, and the review step limits the risk.

For ambiguous phrases, the script leaves a marker instead of inventing a noun. If the transcript says "this button", the draft caption says `[unclear button name]`. I resolve those against the screenshot during review.

## Filter Names and Sensitive Details

Store visits create privacy problems that filenames never exposed. A note may include a person's first name, a supplier price, or a store's internal shrinkage figure. The caption must keep enough context for engineering while dropping details meant for one conversation.

My filter has two passes. The first pass removes obvious personal names using a small allowlist of product, place, and feature terms. The second pass flags money amounts, phone numbers, email addresses, and a list of internal report names.

The filter outputs three categories:

- keep
- replace with a generic noun
- remove and explain why

"Marta at Northside" becomes "staff member at Northside", and a negotiated wholesale price becomes "discounted supplier price". A customer account number is removed completely, and the caption keeps only the screen state.

I keep the original note in a local folder with restricted permissions, while the reviewed caption goes into the project catalog. This separation matters because captions can be copied into issue trackers, slide decks, and blog posts.

The filter caught 19 details in the 78 notes. It missed an internal team nickname, which I removed manually and added to the flag list.

## Adapt Captions for Each Surface

We use the reviewed caption as the stable description, while the publication surface determines how much context appears around it.

An issue tracker gets the caption, the timestamp, and the affected build. A slide deck gets a shorter caption, because the speaker supplies the surrounding story. A blog screenshot gets a self-contained caption that names the product and screen.

The same Shelfcount image therefore has three publication variants:

```text
Issue: Stock count stays empty after damaged-label scan until refresh.
Slide: Stock count remains empty until refresh.
Article: Shelfcount aisle scanner after a damaged-label scan: price loads, stock count stays empty until refresh.
```

A script writes the first draft of each variant from the catalog record. I still review the surrounding paragraph because a caption can be technically correct and still imply the wrong cause.

The final catalog contains 87 reviewed captions. Sixty-two describe normal behavior, and 25 describe failures or load states. Those 25 were disproportionately useful when we redesigned the scanner screen.

The habit that survived is small: pair an artifact with a rough spoken observation, then revise once. I plan to write about the intake folder and pairing checks in a future article. Subscribe if you want the follow-up.
