# Creating Stable Anchors in Fast-Changing Documentation

I rewrote 214 documentation pages for CourseDesk during the last three months. I
wrote this synthetic style exercise with fictional CourseDesk dates, filenames,
and measurements. The rewrite fixed 61 broken links from older course pages, but
it broke 39 links in student notes that referenced section headings.

The obvious response was to tell students to update their notes. That didn't
solve the actual problem because people shared headings in Slack, homework
answers, and private checklists. Those copies don't come back to the
documentation for an update.

In this post, I'll share:

- what counted as a stable anchor,
- how I named canonical terms,
- how I redirected old headings,
- how I tested the links on every release,
- what still breaks after six releases.

## Define the anchor problem

I started by logging every link that students reported. Between January and
March 2026, they reported 83 links, and 31 of them referenced heading anchors
such as `#install-postgres`. Only nine of the reported page links were broken,
while the rest used an old domain or a moved slug.

The heading links were worse: we had changed 27 headings while simplifying the
documentation. That improved the page for a new reader and destroyed the URL for
everyone who had written a note.

I set a rule: a heading can change once its meaning changes, and it needs a
redirect when it changes for style. "Install Postgres" can become "Prepare the
database" only if the instructions change. It shouldn't move just because a
documentation review prefers a verb phrase.

## Choose canonical terms

The next failure came from vocabulary. In March, the same action appeared as
"create a course", "add a course", and "start a course". Search found all of
them, but people copied different URLs into their notes. I asked three teaching
assistants to audit 40 pages and choose one term for each action.

We settled on the action vocabulary in `docs/style/terms.md`. The 28-line list
uses five main verbs, and it marks every forbidden substitute. For example, we
don't use "launch" for publishing, "user" for a student, or "collection" for a
course.

Each term got one heading and one URL. Other mentions stayed in body text, but
the canonical heading became the place to link. For example, the existing page
`/docs/submit-homework#upload-file` now owns upload behavior. A release-note
writer can change nearby text without moving that anchor.

## Build the redirect table

I first tried a catch-all redirect in the static-site server. It turned
`/guide/name-a-course` into `/docs/create-a-course` by stripping the prefix.
That fixed the April links and silently sent `/guide/name-a-course-v2` to the
wrong place.

So I moved redirects into a table. Its four columns record the old path, the
source anchor, the new path, and the destination anchor. The generator turns
each row into an exact rule. If a row is wrong, the table exposes one wrong
destination instead of hiding it inside a prefix match.

The first table covered 117 redirects from four years of guides:

```yaml
redirects:
  - from: /guide/adding-students
    to: /docs/enroll-students
  - from: /guide/adding-students#import
    to: /docs/enroll-students#upload-roster
  - from: /docs/homework
    to: /docs/submit-homework
```

The build fails when two rows have the same source or when a destination doesn't
exist. This caught 14 stale destinations during the first run. It also found
nine redirect chains, which we collapsed into direct links.

## Test anchors in CI

Anchors decay quietly, so I put three checks into GitHub Actions. The checks run
after the documentation build and take 41 seconds on our fictional runner.
Together they cost less review time than one broken-link report.

The checks are:

- every internal link resolves to a page,
- every anchor resolves to a heading,
- every redirect source is unused in current markdown.

I added one more check for the reverse direction. The test reads a manifest of
86 public anchors and requests each one after deployment. Course exercises,
third-party tutorials, and student notes are most likely to use those URLs.

```text
docs-anchors.txt
/docs/create-a-course
/docs/enroll-students#upload-roster
/docs/submit-homework#upload-file
```

A link can leave the manifest only after a deprecation note has been on the page
for one release. That gives writers a deadline and gives readers a visible
replacement before the old anchor disappears.

## Current status

We shipped six documentation releases since April. We changed the pages in 38
of them, and the redirect table gained 43 entries. External broken-link reports
dropped from 11 per month to two. Both recent reports came from links made before
2023 that were never in our manifest.

The system still has limits. It can't protect a heading in a PDF someone
downloaded in 2024. It also can't tell me that a stable anchor references text
that no longer answers the question. I reviewed the 86 protected anchors in
June and found 17 that needed a short update even though their URLs were
healthy.

## Lessons from the rewrite

Stable documentation depends on stable public addresses, and a redirect table
makes those addresses reviewable. A heading is easiest to maintain when the team
treats its URL as an interface.

The rule I took from the rewrite: change the page freely, but change a public
anchor deliberately. Next quarter I plan to apply the same manifest to API
reference headings. Subscribe if you want to see how that behaves under a larger
release.
