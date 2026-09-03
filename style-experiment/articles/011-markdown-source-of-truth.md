# Markdown Remains My Canonical Version

I wrote this piece as a synthetic style exercise. The note repository, dates, and measurements below are fictional, while the reasoning reflects choices I would test.

I started 2024 with 1,284 notes spread across three apps. One app charged €8 per month, while another hid its export menu. The third wrote attachments into a database I could examine only through vendor tools. I moved everything into plain Markdown files in a Git repository.

In this post, I'll share:

- why a trial migration to a hosted app failed

- how Git diffs changed the way I revise notes

- the small tooling I use around the files

- the costs and limitations I accept

- what the experiment taught me about durable writing systems

## The migration that failed

The first attempt looked sensible. I exported the notes to HTML, imported them into Notesphere, and used its built-in sync for about five weeks. Search felt quick, and the mobile app handled photos without much setup.

Then I wanted to rename a course tag across 219 notes. Notesphere offered a bulk editor, but it gave me no preview of the changes. The operation ran, two embedded images disappeared, and the undo history only went back 20 steps. That was enough to end the trial.

The rule I took from it was simple: I need to look at a bulk edit before I commit it. The note app had made the easy path convenient and the review path invisible.

That caveat matters because hosted apps solve real problems for people who mainly capture thoughts. Those people rarely reorganize their libraries. My problem was revision, and it placed me closer to software maintenance than casual journaling.

## Diffs make review cheap

The Markdown move began as an escape, but Git turned it into a better workflow. Every note became a text file, and every meaningful edit became a commit. The repository now has 3,412 commits over 19 months.

When I changed the tag across those 219 notes, I did it with a short Python script. Before committing, I reviewed the diff in chunks of 40 files. The script had incorrectly rewritten links in 11 files, and I saw all 11 before the change entered the main branch.

That review cost about 35 minutes. It also removed the quiet anxiety that comes with a bulk operation inside an opaque store. The files let me ask what changed, who changed it, and whether I can reverse one piece of the change.

The benefit went beyond accidents. When I restructured my reading notes in March 2026, the diff showed 84 renamed files and 112 content edits. I could reject three renames without disturbing the rest.

## The tool stack stays boring

The repository is deliberately plain. It contains folders by year, a `notes/` directory for durable material, an `inbox/` directory for captures, and an `attachments/` directory. Each folder has fewer than 300 items, so file listings remain readable.

I edit with any text editor, search with `ripgrep`, and synchronize through a private Git remote. I also use `notecheck`, a 340-line Python utility, for repository checks. It looks for empty links, missing attachments, duplicate note titles, and todo items left in the durable folder.

I run one command after every writing session:

```bash
uv run notecheck --strict notes/
```

The command reports broken links, duplicate titles, and stray todo items. In August 2026, it found 23 broken attachment references after a folder rename. Fixing them took 12 minutes because every report included the file path and line number.

For retrieval, I added a local index built by another 180-line script. It reads Markdown headings and body text, then stores embeddings in SQLite. That gives me semantic search without another vendor becoming responsible for the files.

## The costs I accept

Markdown and Git are flexible, but they aren't magical. Mobile capture still needs care, and mobile editing remains clumsy around links. I tried four editors this year and settled on one that supports Git through a companion app.

Image handling creates most of the manual work. I compress large photos before committing them, and the repository is now 2.1 GB. A busy week can leave 40 captures in `inbox/`. On Sundays I spend 20 to 30 minutes moving them into durable folders and removing duplicates.

Collaboration also has a higher floor. My spouse can read the notes easily, but she has no reason to learn branch workflows. For shared household material, we still use a separate hosted document. That split is imperfect, and I would rather accept it than force one system onto both jobs.

The security work is mine as well. A hosted app can manage device revocation and encrypted backups for me. With files, I need to remember that the private remote, laptop backups, and phone copies are part of the design.

## Lessons from the move

The hosted app offered convenience and took away review. The Markdown repository asks for more setup and returns inspection. For my writing and teaching notes, that trade has held up for 19 months.

Portability also changed my behavior. Because drafts are ordinary text, I reuse them in course material, articles, and slides without an export step. That reuse removed about an hour of copying per month, according to my coarse project log.

The system's value comes from readable files, reviewable changes, and boring tools. Those properties make it easy to repair, migrate, or abandon a piece without losing the content.

I plan to test a smaller local search index this autumn and describe its retrieval errors in a future article. If you want to follow the next experiment, subscribe for updates.
