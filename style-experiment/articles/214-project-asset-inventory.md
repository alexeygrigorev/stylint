# Creating an Inventory of Assets Across Side Projects

I wrote this synthetic style exercise as a build log, and all the projects, paths and numbers in it are fictional. In January 2026 I needed a chart-drawing helper that I knew I had written for an old dashboard project. Finding it took 50 minutes across 14 repositories, and I ended that evening without it.

The next morning I searched my projects folder instead. It held 23 local repositories, and only 14 of them had a remote on GitHub. Three of the local ones had never been pushed anywhere, and two lived only on an old laptop that I hadn't booted since summer.

My own code had scattered across machines that only I knew about. So I spent a weekend building an inventory file that lists every asset with its path, license, owner and reuse potential.

In this post, I'll share:

- why memory and platform search both failed
- how the sweep script walks the projects folder
- which fields every entry holds
- how I mark reuse candidates once a month
- what the inventory changed in one quarter

## Twenty-Three Folders And No Map

My first attempt used the GitHub search box across my own repositories. It searched only default branches, and it matched only repos with the words in code or README text. My unpushed folders were invisible to it, and one of them, `dashboard-2022`, held the exact helper I wanted.

A second search on my laptop was faster but just as blind. The desktop search matched file contents, and it knew nothing about licenses, owners, or activity. The rule I took from that morning: an inventory that depends on memory misses whatever memory drops.

## The Sweep Script

I wrote `sweep-projects`, a Python script that walks `~/git` and records what each repository contains. For every folder with a `.git` directory, it reads the LICENSE file and the README intro. It also records the last commit date and the main language from the file extensions.

One pass covers all 23 folders in about 90 seconds:

```bash
uv run python tools/sweep_projects.py --root ~/git --out inventory.csv
```

The script writes one row per project, and reruns cost nothing because only file reads happen. Rows for deleted projects stay in place with a `gone` note. That decision mattered in February, when I removed two folders and still wanted their history.

I kept the whole thing as a CSV instead of a database. The file stays readable in any editor, syncs with my usual folder backup, and diffs cleanly in git. A database would have added a server process for 23 rows. Versioning the CSV in git also gives every change a date, which turned the file into a small history of the projects.

## Fields In Every Entry

Each row has six fields:

- path on disk plus the remote URL if one exists
- license, as detected from the LICENSE file
- owner, meaning who may change and reuse the asset
- last commit date from the git log
- main language from the file extensions
- reuse note, empty until I judge the asset

The owner column looks silly with one name in every row. I keep it anyway, because two projects already have a collaborator, and a future collaborator costs an afternoon of confusion otherwise. The license column earns its space on day one, since reuse without a license is just guessing.

The columns also grew over time. The first version had four fields, and the remote URL plus the reuse note arrived after the first month of use.

## Marking Reuse Candidates

The reuse note turns a plain list into a tool. I go through the rows once a month and mark anything another project could adopt.

The February pass marked five assets:

- the chart helper, now copied into two projects
- a retry-with-backoff decorator from the queue experiment
- an SQLite migration helper with clean tests
- a markdown-to-newsletter converter used once in 2024
- a scraping utility for the course listings

Not every candidate survives a second look. The January pass marked a settings loader that looked generic, and it turned out to depend on two project-specific config files. I unmarked it in February, and the note now records why. Each note also gets a date, because a judgment from November may not hold in June.

Only two of the five had clean licenses, so reusing the other three would mean license work first. The chart helper needed ten minutes to extract, and it has saved me about three hours across two projects since.

## The Inventory After One Quarter

The sweep runs on the first Saturday of every month, and it takes 90 seconds plus about 20 minutes of marking. I found the chart helper in two minutes the last time I needed it, and I have stopped rediscovering my own code. The monthly pass also surfaces dead projects, and I archived four of them in March with a clear conscience.

The file still knows nothing outside `~/git`, so design files, datasets, and note collections stay uncounted. The description field also depends on whatever the README offers, and six projects had no README at all. I wrote three one-line READMEs in February to patch the worst gaps. The rule I took from that chore: if a description can't be generated, write one.

I'll write about extending the sweep to design assets in a future post. If you want to follow along, don't forget to subscribe.
