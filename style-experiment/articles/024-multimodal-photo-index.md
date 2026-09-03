# Indexing Workshop Photos with Descriptions and Tags

I generated the workshop, photo set, and model output in this piece as a synthetic style exercise. The workflow mirrors what I do when a real photo collection becomes too large to browse.

After a two-day workshop in March 2026, I had 1,284 photos from three rooms and four instructors. They sat in a folder named `workshop_final_v2`, which explained nothing. I built a small multimodal index so future me could find the right image in seconds.

In this post, I'll share:

- how I tested captions on a small sample first
- what fields the photo record stores
- how project, location, and instructor tags work
- which privacy filters run before publication
- how search behaves on the finished index

## A Weekend of 1,284 Photos

The camera roll mixed four kinds of images:

- wide room shots
- whiteboard close-ups
- laptop screens
- candid discussions

Renaming files by timestamp helped, but it didn't answer the questions I actually had. I needed images for a recap article, instructor feedback, and next year's room plan.

My first manual pass covered 42 photos in about 35 minutes. It produced useful captions, and it also showed the hard cases.

Three examples drove the later design:

- a slide without its speaker
- a whiteboard with names from a prior session
- a screen containing an email address

So I treated manual review as the specification. The automated system had to describe the visible action, name the room, preserve useful technical terms, and mark sensitive content before an image became shareable.

## Describe One Photo Before Scaling

I started with a vision-language model (a model that accepts both images and text) on 60 sampled photos. I wrote one prompt and asked for three parts.

The response schema was simple:

- one sentence describing the activity
- visible objects and text
- a privacy decision with a reason

The prompt requested JSON so the results could go into a database without custom parsing. It also said to use `unknown` rather than invent names or institutions. That instruction reduced confident errors, although it didn't eliminate them.

Forty-nine of 60 captions were accurate enough to keep. Four needed a better time reference, such as "morning exercise" instead of "session". Seven required human review because the image contained readable text on a personal laptop or a printed list.

Those numbers set the process. Automation could sort and draft, while a person approved anything that might leave my machine.

## Store Captions and Tags

The index uses SQLite (a small embedded database) and one table called `photos`.

I kept the schema simple enough to review with one query:

```text
photo_id, file_path, capture_time
caption, objects, visible_text
room, instructor, project
privacy_status, review_note
```

Each image gets a UUID (Universally Unique Identifier) as its `photo_id`, so renamed files don't break references. The caption stays immutable after approval. If the model output changes, the row gets a new version and points back to the approved caption.

Tags have three layers, and the room and instructor fields come from a card visible in the first photo of each session. Project names come from the workshop schedule.

Free-form object labels come from the model and support queries such as "laptop", "sticky notes", or "network diagram".

Processing all 1,284 photos took 41 minutes on my laptop and cost about $3.10. That number made it easy to rerun the job after I improved the prompt.

## Add Location and Project Fields

At first I used a generic `location` string. It worked for "Room B", but a later recap needed to say which activity belonged in the workshop area rather than the lecture room.

I replaced the string with two fields:

- `place`: building or outdoor area
- `zone`: table, projector wall, kitchen corner, or hallway

This distinction sounds small until you search it. "standing exercise in Room B" returned 31 photos, while "standing exercise in Room B, projector wall" returned six. That narrower result was exactly what I needed for a layout review.

Project fields came from a schedule file rather than image content. Each session had a project ID, start time, and room. The indexer joined a photo by capture time to that interval. When a camera clock drifted by four minutes, the script assigned 18 photos to the wrong session.

I fixed the clock drift once, then added an overlap report. If a session boundary crossed a burst of photos taken within two seconds, the script put them into a review queue instead of guessing.

## Filter Before Anyone Sees Results

The privacy pass runs before an image becomes visible in the web interface.

It assigns one of three states:

- `private`: stays on my laptop
- `review`: person checks faces, screens, or printed names
- `shareable`: approved for a public recap

The model starts conservatively and flags a readable name, email address, phone number or screen with account information as `review`.

Crowd shots with small faces also go to review.

Of the generated set, 890 photos became `shareable`, 241 required review, and 153 stayed private. I agreed with 219 of the 241 review decisions. The other 22 had only generic laptop screens and no readable text.

I also wrote a rule for children and non-participants. Neither group appeared in the fictional workshop, but the filter still defaults to `private` when a face doesn't match a signed media consent record.

## Search the Finished Index

The interface is one local web page served by FastAPI (a Python web framework). It supports free text and filters in combination.

A typical command looks like this:

```bash
photos search "sticky notes" --room "Room B" --privacy shareable
```

Search uses SQLite full-text search over captions, object labels, visible text, and project names. It doesn't do semantic search, so "collaboration" may miss a caption that says "group discussion". For this collection, exact terms were more predictable.

Three searches covered most of my work:

- activity plus room
- object plus project
- instructor plus time range

Median time to a useful photo fell from about four minutes of folder browsing to 20 seconds.

## Index Effects

The photo index is now a workshop archive rather than a pile of files. It makes captions reusable, keeps sensitive images out of drafts, and gives every approved image a reason for that status.

The remaining weakness is vocabulary drift. Instructors said "walkthrough", "exercise", and "lab" for similar activities, and the index preserves those differences instead of deciding they're equivalent. My next step is a small controlled vocabulary for activity types.

I plan to write about that experiment after the next fictional workshop. Subscribe to follow along.
