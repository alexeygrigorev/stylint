# Turning Experimental Notebooks into a Teaching Path

This synthetic style exercise follows a fictional cleanup I ran in February. I had 34 experiment notebooks from two years of evening work. Most notebooks mixed working code with dead ends and missing imports.

I teach a small weekend workshop and I reuse my own experiments as examples. I've copied cells by hand for four cohorts and I don't want another scramble. I keep 212 cells across notebooks in one folder, with imports from six different data files.

I built PathBuilder, a short Python script that extracts runnable examples and orders them by concept. It reads notebook JSON, scores each cell, and writes a teaching folder. The script started as a 60-line filter I wrote in January.

In this post, I'll share:

- why raw notebooks confuse new learners
- how I score cells for teaching value
- what order turns examples into a path
- how exercises and cleanup keep the path usable
- where the path still needs live explanation

## Raw Notebooks That Confuse Learners

My worst workshop moment came last November. I opened a notebook with 48 cells and I scrolled past three broken imports before reaching the example. Eight students waited while I fixed a file path that only existed on my laptop.

I had prepared for two hours and I had tested the first five cells only. The middle of the notebook called a CSV from `/tmp` and that file had vanished weeks earlier. I improvised with a smaller dataset and I lost 20 minutes of class time.

A second failure came from mixed skill levels in one file. In the same notebook, I introduced Pandas filtering and then jumped to custom loss functions without warning. Beginners felt lost and advanced students felt bored in the same ten minutes.

The rule I took from those sessions: I order teaching material from one concept to the next without hidden state. I also keep every cell runnable in order.

I chose a separate teaching folder because I don't want to edit originals during class prep. I keep cleaned scripts, small datasets, and exercise prompts in that folder. That split keeps experiments messy and lessons runnable at the same time.

## Scoring Cells For Teaching Value

PathBuilder reads each notebook as JSON and it scores every code cell on four checks. I check for successful execution, short runtime, clear outputs, and limited dependencies.

The scoring run covers all notebooks in about 90 seconds on my ThinkPad. It processed 212 cells in February and it kept 64 cells with a score of eight or higher. I reviewed the 64 survivors by hand in about two hours.

The scorer keeps cells that meet these conditions:

```text
runs without errors
finishes in under 30 seconds
uses at most two data files
produces a chart or a table
```

I review borderline cells with a score of seven because the cutoff misses useful examples. One borderline cell showed a clean train-test split with an extra debug print. I removed the print and I kept the cell after a ten-second edit.

I don't keep cells that download data during class. Downloads fail on workshop WiFi and they waste ten minutes while everyone watches a progress bar. I replace downloads with a 2 MB sample file stored next to the lesson.

One mistake taught me to record the source notebook for every kept cell. I reused an example in March without knowing which experiment it came from. I added a source field with notebook name and cell index the same week. That field now saves me about 30 minutes per workshop.

## Ordering Examples Into A Path

Order matters more than coverage for beginners. My first path grouped cells by file origin and students jumped from plotting to tokenization in one step. Quiz scores averaged 54 percent and two students asked for a slower sequence.

The second order follows concept dependencies instead of file history. I start with data loading, then filtering, then grouping, then a first model. Each step uses only concepts from earlier steps plus one new idea.

The path file lists the sequence in plain text:

```text
01-load-csv.py
02-filter-rows.py
03-group-and-plot.py
04-train-baseline.py
05-evaluate-errors.py
```

I run the five files in order before every workshop and I confirm each one finishes in under a minute. That check takes six minutes and it catches broken paths after library updates. The February run caught a Pandas rename that broke step three.

I picked a short sequence because a two-hour session fits a few examples with discussion. Extra steps rush the middle and missing steps leave advanced students idle.

## Exercises And Cleanup That Keep Lessons Usable

Each step ends with one small exercise that takes under ten minutes. I write the prompt, the expected output shape, and one hint in the file header. Students work for seven minutes and we review for five minutes before moving on.

The exercise format stays fixed across steps. I state the task, I show the starting code, and I name the function or column to change. That consistency lets students focus on the concept instead of decoding instructions.

Cleanup runs after every cohort. I archive student questions, I delete one-off debug files, and I refresh dataset timestamps.

I ask students for one confusing line per step on an exit card. The February cards named 11 confusing lines and I rewrote nine of them before March. Two lines stayed because they covered optional details for advanced readers.

I don't automate exercise grading because the groups stay small, around 14 students. I read each solution during the break and I note common errors for the review.

## Reflection And Next Steps

The teaching path cut my prep time from six hours to about two hours per workshop. Student quiz averages rose from 54 percent to 71 percent across two cohorts. Live debugging dropped from 25 minutes per session to under eight minutes.

I still explain two transitions live because the written text feels thin. The jump from grouping to training needs a whiteboard sketch and one extra example. I plan to add that example before the June cohort.

I plan a short review pass that re-runs all steps on a fresh machine every month. I'll record runtimes and package versions in a log and fix drift before class.

I'll write about that monthly re-run setup in a future post. If you want to follow along, don't forget to subscribe.
