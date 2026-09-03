# Checklist for Reviewing AI-Generated Interface Images

I wrote this synthetic style exercise as a how-to guide. The project, dates and measurements are fictional. In June 2026 I generated 40 interface mockups with an image model for `coinlog`, a small budgeting app. The developer received two broken screens: one had no disabled state, and the other used body text under the contrast minimum.

The model produces a convincing screen in about 20 seconds, and that speed is the trap. A generated mockup looks finished at a glance, so my review skipped the boring checks and caught problems only after implementation. I now run the same checklist before any image moves to implementation, and the full pass takes about 15 minutes per screen.

In this post, I'll share:

- how to fix the prompt and the device sizes
- how to check contrast first
- how to check spacing and alignment
- how to check states and labels
- which caveats matter before you ship
- what changed for the August batch

## 1. Fix The Prompt And The Device Sizes

We start by fixing the prompt in place, because a prompt that moves makes review results impossible to compare.

I wrote this prompt for `coinlog` after one batch returned screens for three different phones:

```text
Generate a mobile screen for a budgeting app called coinlog.
Device: 390 by 844 points, thumb-friendly layout.
Show the February spending screen with real values.
Palette: #1A1A2E background, #E94560 accent, white text.
```

The device, the palette and the data stay fixed across batches now. We fix the review sizes the same way. I check every screen at 390 points for phones and at 1280 points for desktop. Those two sizes cover 82 percent of the sessions in our analytics. You can pick different numbers, but pick them once and write them into the prompt.

## 2. Check Contrast First

Contrast fails more often than anything else, and it fails quietly. I paste the generated image into a screenshot tool and sample the pixel values of body text against its background. The model rarely reproduces the hex codes from the prompt exactly, so measuring beats trusting.

My pass rule is the WCAG AA threshold of 4.5 to 1 for body text and 3 to 1 for large headings. In the June batch, 14 of the first 40 mockups had body text between 2.9 and 3.8 to 1. Each one looked fine on my laptop and failed on a phone in daylight. I keep the sampled values for every screen in a small `contrast-notes.md` file, so the second review starts from numbers instead of memory.

## 3. Check Spacing And Alignment

The generated screens drift from any grid, so we measure instead of eyeballing.

I overlay an 8-point grid in the editor and look at three places:

- the gap between list rows
- the margin at the screen edges
- the space around buttons

Any gap outside 8, 16 or 24 pixels goes on the fix list.

Spacing isn't the only check, because alignment breaks in subtler ways. In one June mockup the balance header sat 6 points lower on the left than on the right. The offset survived every glance until I measured it.

## 4. Check States And Labels

A static image shows one state, so we ask the model for the rest. I generate pressed, disabled, empty and error views as separate images. Each image gets the same prompt plus one state line, which keeps the layout stable enough to compare.

Labels need a full read, and I mean reading every word. The generated interfaces fill space with plausible junk like "Logn" for "Login". The June batch also showed "USD" on one row and "$" on the next row of the same screen. Across the batch, 7 of 40 screens had a misspelled label, and 5 used two names for one currency.

## Caveats And Common Mistakes

The full pass takes me about 15 minutes per screen, and it has known limits.

Keep these caveats in mind before you trust a pass:

- pixel sampling catches low contrast, but it can't judge whether a font reads well
- state images can drift from the original layout, so compare the edges before the states
- the model regenerates the whole screen for a one-word fix, so keep the old image until the new one passes

For the August batch I compressed the whole pass into a block that goes into every ticket:

```text
contrast: body text at 4.5:1 or higher, sampled from pixels
spacing: rows and margins sit on 8/16/24 points
states: pressed, disabled, empty and error generated separately
labels: every string read aloud, currencies checked
sizes: 390 pt and 1280 pt both reviewed
```

The developer attaches the filled block to the ticket, so the review survives the trip to implementation. The block also turned the pass into something the developer can rerun without me.

## Results From The August Batch

The checklist turned the review from a glance into 15 minutes of measurements. Screens that reached implementation had defects 9 times in June and 2 times in August. Both August defects were flow problems that no pixel check can see. The remaining gap is flow, and I cover it with a 10-minute walkthrough of the full app on a real device before every release.

I'll write about the fix-request prompt format in a future post. If you want to follow along, don't forget to subscribe.
