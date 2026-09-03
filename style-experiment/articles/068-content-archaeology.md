# Finding Reusable Ideas in Old Notes

Last January, I consolidated 2,180 notes from four fictional note apps into SQLite. Only 214 had a usable title, and 87 were scattered project ideas across dated files. I spent three weekends doing content archaeology and turned one buried cluster into an article plan.

I invented the archive, dates, and counts for a synthetic style exercise. The process is real enough to reuse. You index the material, group related fragments, rank the clusters, and test one of them by writing.

In this post, I'll walk through the workflow:

- how I normalized four messy exports
- the metadata I added before search
- how I clustered notes by problem rather than tool
- the ranking rules I used
- how one cluster became a draft
- what still needs manual judgment

## Normalize the exports

Each app exported a different structure. One produced JSON with timestamps, one exported HTML, and two exported Markdown folders. I converted everything into SQLite so I could query the archive without opening files one by one.

The import script lived in `tools/notes-import.py`, and it wrote one row per note. It preserved the original filename and body text, together with the app name and dates. Where the export had no title, I used the first non-empty line and marked it inferred.

The first import failed on 63 files because they used inconsistent encodings. The second pass read bytes first and decoded only after detecting UTF-8 or Latin-1, which fixed 61 files. I logged the remaining two as errors rather than guessing.

I also removed three categories immediately:

- credentials and account recovery codes
- duplicate exports with identical content hashes
- meeting notes that belonged to another person

After cleanup, the database held 2,127 notes. The reduction looked small, but it kept private data out of the search index and removed noise that would have made weak clusters look larger.

## Add useful metadata

Text search alone wasn't enough. A 2019 fragment named "batch embeddings" and a 2025 fragment named "semantic cache" became related only after I saw that both addressed slow personal search. I added three fields before clustering.

I called the first field `kind`, and it marked each note with a single type. A note could be an idea, a quote, a snippet, or a project fragment. It could also be an exercise, and that distinction separated examples from raw inspiration. Manual labeling of 2,127 notes sounded painful, but rules covered 73 percent of the labels. For example, notes containing code fences and no narrative sentences became `snippet` candidates.

I called the second field `project_hint`. It captured a project name only when the note mentioned one directly. I kept the hint lowercase and unchanged, so `rag-workshop` and `RAG Workshop` remained separate until a later normalization step.

The third field was `status`, with these values:

- `raw`: no review
- `usable`: has enough context to understand later
- `fragment`: interesting but incomplete
- `dead`: no longer relevant or understandable

I reviewed high-risk categories in batches of 100, usually in 20-minute sessions. My error rate was highest for snippets copied without a source. I marked 118 as `dead` because they no longer matched any known context.

## Cluster by problem

My first clustering attempt used tool names. That produced one large group around Python packages and missed the actual reason I had saved most notes. So I switched the clustering question from "What tool is this?" to "What problem did I want to solve?"

I used embeddings to retrieve 12 nearby notes for each item, then grouped them by hand in `notes/clusters.md`. The retrieval made candidates visible, but I wrote the cluster names. That kept the taxonomy grounded in problems rather than vocabulary.

The clusters that emerged were concrete:

- personal search and retrieval latency
- course exercise generation
- article pipelines and reuse
- community question routing
- small dashboards for private data
- teaching notebooks that became libraries

Personal search was the largest cluster, with 168 notes. Article pipelines had 96, course exercises had 71, and the remaining clusters had between 18 and 54 notes. A few notes stayed unclustered.

The manual pass also revealed a weakness in my note-taking habit. Many saved links lacked one sentence explaining why they mattered. Those notes could be retrieved by title, but they couldn't join a problem cluster without reopening the source.

## Rank the clusters

I scored each cluster on these four factors: Each factor got a score from 1 to 5, and I wrote a sentence justifying every score.

The personal-search cluster scored highest. It had 168 notes, a recurring problem in three projects, and two experiments. Its main weakness was saturation: I had already published two articles about related search tools, so a new piece needed a more specific claim.

Article pipelines scored 4 on usefulness and 3 on material. It had enough notes, but several ideas duplicated existing content. Course exercises scored lower because the notes described goals more than examples. Small dashboards scored high on effort, so I postponed it.

Rather than trusting the total score, I looked for a cluster with surplus evidence. Personal search had the strongest surplus of dates, code fragments, measurements, and repeated complaints. That made it possible to tell a chronological build log instead of writing an opinion essay.

## Turn one cluster into a draft

The chosen cluster became an article called "Slow Personal Search". I copied 32 relevant notes into `drafts/slow-personal-search/research.md` while preserving their original dates and source paths. Seeing 2019, 2022, and 2025 entries side by side exposed the progression without rereading every export.

I wrote a one-paragraph thesis first: my search needed to become slower during indexing so it could become faster during daily queries. That sentence came from three notes complaining about premature caching and stale results. It gave the draft an argument instead of a list of tools.

Then I built this timeline from the notes:

- 2019: keyword search over 300 markdown files
- 2022: embeddings for 4,000 chunks, with slow initial indexing
- 2023: caching with no invalidation rules
- 2025: versioned cache and source freshness labels

The timeline showed an honest failure. The 2023 caching experiment made repeated queries faster, but stale results damaged trust. That failure became the center of the draft, and the newer cache design became evidence for a rule rather than a product claim.

The resulting outline used five sections. It moved from query logs through the first index and the cache mistake, then covered the newer design and current routine. Each section mapped to dated notes, so I could add measurements without inventing a structure after the fact.

## Leave room for judgment

Automation helped with normalization, retrieval, and ranking, but three decisions stayed manual. I chose the cluster name, the thesis, and the draft boundary. Those choices determined whether the material became one coherent piece or another pile.

I also kept a rejection list in `notes/clusters.md`. For example, course exercise generation looked attractive, but it lacked current examples. I wrote that reason next to the cluster so future me wouldn't reopen the same dead end every quarter.

The archaeology changed how I take new notes. Every saved item now gets one sentence explaining the problem it addresses. That small habit adds perhaps 15 seconds, and it makes the next round of clustering much easier.

If I continue the exercise, I'll write the "Slow Personal Search" draft and show how each section traces back to the dated notes. Subscribe if you want to see whether the reconstructed idea survives contact with drafting.
