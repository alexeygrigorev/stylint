# Writing a Script to Find Orphaned Article Assets

I wrote this synthetic style exercise as a build log, and all project details are fictional. In May 2026 the media folder of my site passed 2.1 GB, and it held 640 images for a site with 95 articles. A spot check suggested that at least 150 of those images appeared in no article at all.

The orphans came from five years of deleted drafts and replaced screenshots. Every time I rewrote a section, the old image stayed in the folder, because deleting it felt risky. Site backups then copied the dead weight every month, and the folder grew by about 40 MB per week.

In this post, I'll share:

- what a filename grep missed
- how the script collects references from the site
- which files sit on the exclusion list
- how the dry run works
- what delete mode removes and restores
- what the first month of runs changed

## A Filename Grep That Missed

My first attempt was a shell one-liner. For each asset in `media/` it grepped the article folder for the filename and printed the assets with no match. A one-liner was fine at 50 files, and it fell apart at 600. The list came back with 212 orphans, and I nearly ran a delete against it.

The list was wrong in both directions. It missed `cover.png`, because three articles referenced the file through a template variable. It also counted `icon-rss.png` as an orphan, because the reference lived in the site config instead of an article. My mistake was assuming that articles are the only place a site mentions its images. The rule I took from it: the scan has to read every file the renderer reads.

## Collecting The References

In June I wrote `find-orphans.py`, a Python script that walks the whole site directory and collects every string that looks like a media reference.

The scan covers four places:

- article markdown, including frontmatter fields such as cover and preview
- templates, where default social-card images live
- the site config, which holds icons and feed art
- a short manual list in `orphans.toml` for special cases

For each asset under `media/`, the script then checks whether its filename appears anywhere in that reference set. The match includes the parent folder name, which removed the false hits from same-named screenshots in different years.

I looked at existing cleanup tools first, and they all worked like my one-liner did. They grepped one folder for filenames and trusted the result. Writing my own script took an evening, and it reads the site the way the site generator reads it.

The reference collection is one function of about 30 lines:

```python
def collect_references(paths):
    refs = set()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        refs.update(MEDIA_RE.findall(text))
    return refs
```

The regex looks for quoted strings and markdown targets that end in an image suffix. The full scan runs over 140 files in about half a second.

## The Exclusion List

Some assets should survive even with no reference at all.

The script reads its exclusions from `orphans.toml`:

```text
exclusions = [
  "media/favicon-32.png",
  "media/social/default-card.png",
  "media/logo/*",
]
```

The default social card gets its reference from a template variable the regex can't see, so it goes on the list by name. The logo folder holds files the theme loads by convention. The manual list gained a third entry after the first delete, and that story shows up in the delete mode section.

## The Dry Run

Dry run is the default mode, and it prints the orphans with their sizes while deleting nothing:

```text
$ uv run python find-orphans.py
orphans: 178 files, 412 MB
  media/2022/dashboard-old.png      1.2 MB
  media/2023/course-slide-14.png    380 KB
dry run: nothing deleted, pass --delete to remove
```

I ran the dry run three times across one week and compared the lists. The count moved only when I published a post, and that stability convinced me the scan was complete.

## Delete Mode

Delete mode asks for the `--delete` flag and refuses to run unless `git status` is clean. Instead of unlinking files, the script moves them to `media/_trash/` and writes a dated manifest such as `deleted-2026-06-14.txt`. The manifest records the original path, the size and the reason each file looked orphaned.

The first real run on 14 June moved 178 files and freed 412 MB. One article broke immediately: a 2022 post referenced `dashboard-old.png` through a shortcode parameter the parser doesn't read. I restored that file from `_trash/` in about two minutes and added the shortcode to the manual list in `orphans.toml`.

My mistake was trusting the parse coverage on the first delete. The rule I took from it: the first delete run happens on a day with time to restore.

## Results From The First Month

The folder dropped from 2.1 GB to 1.6 GB, and a weekly cron job keeps it there. The job runs on Sunday mornings, and the delete list stays at about 5 files between cleanups. I also run the dry run once before every backup rotation, so the weekly archive shrinks with the folder.

The script still can't see references that JavaScript builds at runtime. One interactive chart loads three images that the scan wants to remove. Those files stay on the manual list until I find a better check.

I'll write about the trash folder rotation in a future post. If you want to follow along, don't forget to subscribe.
