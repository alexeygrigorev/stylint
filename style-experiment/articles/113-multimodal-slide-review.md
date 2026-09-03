# Using Vision Models to Review Slide Layouts

I wrote this synthetic style exercise as a build log. The slides, model outputs and measurements are fictional.

On 21 August I had 42 slides for a workshop about retrieval evaluation. My review process had become a slow scan for obvious layout problems. I had found a clipped code block only while projecting the deck on the venue screen in July.

I wanted a repeatable layout check before the next event. The topic was visual: overflow, contrast and alignment are easier to point at than to describe. I also wanted the model to review the story order, so I gave it a slide deck rather than isolated screenshots.

In this post, I'll share:

- how I exported and labeled the slides
- which review prompt I used
- what the model found in the first pass
- which findings were false alarms
- how I changed the deck and the review workflow

## Preparing The Deck

The deck was in Google Slides. I exported it to PDF, then used `pdftoppm`, a command-line tool for converting PDF pages to images. It created one PNG per slide in about 20 seconds at 150 dots per inch.

I kept the original filenames because slide numbers were the shared key between findings and edits:

```bash
pdftoppm -png -r 150 slides.pdf slide
```

That command produced `slide-01.png` through `slide-42.png`, and I checked a dense code slide, a two-column comparison and the title slide. The images were sharp enough to read 18-point text.

I had used one client screenshot in the workshop, so I replaced it with a synthetic placeholder before upload. I put fictional names and a fake response payload in that placeholder. This privacy check has to happen before a deck leaves my machine.

## The Review Prompt

I used GPT-5 with image input through the API. The prompt asked for findings in four fixed categories: contrast, overflow, alignment and narrative order. It also required a slide number, a location on the slide and a concrete suggested change.

I sent this prompt with each batch of six images:

```text
Review these workshop slides for layout and narrative problems. For every issue, return the slide number, the location, the category (contrast, overflow, alignment, or narrative order), the observed problem, and one concrete change. Do not rewrite the content. Do not invent text that is unreadable. If a slide has no issue, do not list it.
```

Batches of six kept each request below 4 MB and made responses easier to compare. All seven batches took 3 minutes and 10 seconds and cost about $0.42.

I deliberately separated layout review from fact checking. The model could see arrangement and visual hierarchy, but it had no access to the speaker notes, the source links or the workshop exercises.

## The First Findings

The review returned 29 findings. I copied them into a spreadsheet and marked each one as real, false alarm or subjective. Nine were real defects, eleven were low-priority judgments, and nine were wrong.

The three most useful findings were:

- slide 14: a Bash command extended beyond the content box
- slide 23: dark gray text on a dark image with a measured contrast ratio of 2.7 to 1
- slides 30 to 34: the exercise explanation appeared after the exercise slide

The overflow finding matched a long `pg_dump` command. The contrast finding identified a caption I had placed directly over a photo. The narrative finding exposed an editing accident from 19 August, when I inserted a practice slide without moving its instructions.

I shortened the command and replaced some options with a short comment. On slide 23, I moved the caption under the photo and set the caption color to near-black on white.

## False Alarms And Human Review

The false alarms fell into clear groups:

- the model twice reported overflow on slides with intentional full-bleed images
- in those cases the image extended behind the text, but no glyph crossed the slide edge
- it once interpreted a deliberate blank area as missing content
- six findings invented small footnote text and then objected to that invented wording

The narrative findings needed the most filtering. The model preferred chronological order, but two intentional forward references worked better for teaching. One section previews a section that arrives later, and that preview gives learners a reason to care about the intermediate metric.

My review rule became simple: visual issues need one look, while narrative suggestions need the speaker notes. I accepted 8 of 11 narrative and alignment suggestions. The other three conflicted with how I planned to speak through the sequence.

The model didn't replace the projector test. It caught problems before that test, so the final rehearsal focused on timing instead of pixel defects.

## Revising The Deck

The first revision removed 137 words across five slides and changed six layouts. I reduced code font from 22 to 20 points only on slide 14, after replacing the long command. Every other slide retained its original type scale.

I standardized slide containers:

- text remains inside an 8-pixel margin around the content box
- code blocks use a single fixed-width layout
- image captions sit below images on white background
- each section has one title slide and one practice slide

Those rules sound obvious, but the deck had accumulated exceptions over four editing sessions. Putting them in one list made future drift easier to spot.

On 22 August I reviewed the revised deck again, and the second pass returned 12 findings. Seven were duplicates of accepted suggestions, three were minor alignment notes, and two were new false positives caused by the synthetic placeholder. I accepted one alignment note and moved another image 16 pixels.

## Lessons From The Slide Review

The model worked best as a first-pass reviewer with a fixed vocabulary. It found the clipped command and low-contrast caption in minutes, and my own scan had missed both.

The deck improved because I filtered the output against intent. Visual findings could be accepted with little context. Narrative findings required the notes and the planned delivery, and six of the model's objections collapsed once I read the actual footnote text.

The review still doesn't test readability from the back row or color perception under venue lighting. I'll keep the projector rehearsal for those. My next iteration adds a checklist for reading order inside complex diagrams.

I'll describe that checklist after the next workshop. If you want to follow along, don't forget to subscribe.
