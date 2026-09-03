# Generating a Fast Photo Gallery for a Workshop Recap

I wrote this synthetic style exercise as a build log, and all project details are fictional. After a March 2026 workshop with 24 participants, I promised everyone a recap page within a week. The photos totaled 183 files and about 1.9 GB, and the largest single image was 8 MB.

My workshop site is a static page on a 5-euro VPS. A gallery of raw files would weigh more than everything else on the site combined. The photos needed real resizing before they went anywhere near the server.

In this post, I'll share:

- how the photo dump looked before any tooling
- why the hosted gallery attempt failed
- how the generator resizes images and reads captions
- how the HTML template stays small
- what the deploy step and the final size look like
- what changed by the second recap

## The Photo Dump

The dump had three sources and no order. File names looked like IMG_4021.jpg and DSC_8832.NEF, and about 30 photos were near-duplicates from the same exercise. My phone contributed 96 shots, and two participants sent the other 87 through a file request.

The 12 RAW files from one participant's camera were a separate problem, because browsers render them badly. I converted them to JPEG first and resized them like the rest.

I spent one evening just deleting, and the pile shrank from 183 to 141 usable photos. That evening produced the rule for every later recap: curate before any tooling touches the pile.

## First Try On A Hosted Service

The obvious first move was a hosted gallery service. I uploaded 60 test photos to a free tier on a Tuesday evening.

The service wrapped them in a viewer I couldn't customize. Albums sat behind a login wall, and the free tier stopped at 2 GB of storage. The upload also took 25 minutes for 60 photos on my connection, which made every caption fix a new wait.

I wanted the gallery on my own domain, with my own captions and no login. That requirement killed the hosted option in about 20 minutes, and it sent me back to static files.

## Resizing And Captions

So I wrote `gallery-gen`, a small Python script that turns a folder of photos into a static page. The script uses Pillow, a Python imaging library, for resizing. Every image gets a 1,600-pixel longest side in WebP at quality 80, plus an 800-pixel thumbnail for the grid.

The size function is four lines:

```python
def resize(src, dst, longest=1600, quality=80):
    img = Image.open(src)
    img.thumbnail((longest, longest))
    img.save(dst, "WEBP", quality=quality)
```

The 141 curated photos came out at an average of 190 KB each, about 27 MB in total against 1.9 GB of originals. I tested quality 60 as well, and it saved another 4 MB per hundred photos at a visible loss on whiteboards. Quality 80 kept text on slides readable, which matters more for a workshop than raw file size.

Captions live in a `captions.yaml` file next to the images. Each photo gets one line there, and I wrote 60 public captions in about 40 minutes on a train.

Three lines from the file show the format:

```text
IMG_4021.jpg: the retrieval exercise, 12 minutes in
IMG_4088.jpg: the winning team and their 94% score
DSC_8832.jpg: closing retro at the whiteboard
```

A missing caption is a build error, so the gallery can't ship with an unnamed photo.

## The HTML Template

The template is one HTML file with a CSS grid of thumbnails and a full-size view per photo. Without images, the HTML weighs 6 KB and the CSS adds 3 KB.

One rendered grid cell looks like this:

```text
<a href="img/IMG_4021.webp">
  <img src="thumbs/IMG_4021.webp" loading="lazy" width="800" alt="the retrieval exercise">
</a>
```

Lazy loading keeps the opening view at about 12 thumbnails. The caption renders under each thumbnail in small text, so the recap explains the exercise without a second visit. Clicking a thumbnail opens the raw WebP file, with no JavaScript in between, and I accepted that trade to keep the page dependency-free.

## Deploy Step And Page Weight

Deploy is one rsync command after the build.

Build and deploy together take two commands:

```bash
uv run python gallery_gen.py photos/ --out site/gallery/
rsync -avz --delete site/ deploy@workshop-site:/var/www/html/
```

The full run takes about 50 seconds for 141 photos, and rsync sends only changed files after the first push. The gallery folder sits outside the site's git checkout, because I don't want 27 MB of binaries in the history. A backup job copies the originals to an external drive every Sunday.

The finished gallery weighs 27 MB with all 141 images, against 1.9 GB for the raw pile. Lazy loading keeps the opening view at about 1 MB, and the grid renders in about 1 second on my phone over 4G. The hosted test from March needed 9 seconds to reach a login wall.

## After Two Recaps

The generator turned a two-evening chore into a 40-minute caption session and one command. April's recap, with 209 photos from a second workshop, reused the same template, and the only change was a wider thumbnail grid.

The gallery still has limits. There's no lightbox, so readers use the browser back button between photos, and two participants asked for one in March. EXIF rotation also caused one bad surprise, because Pillow ignores the orientation flag on some phones, and one photo still stands on its side.

I'll write about EXIF-based date grouping for the grid in a future post. If you want to follow along, don't forget to subscribe.
