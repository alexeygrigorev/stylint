# Writing a Scope `Contract` for a Side Project

I wrote this synthetic style exercise as a how-to guide. The project, dates and measurements are fictional. In January 2026 I stopped a side project after five weekends, because it had grown to three user types and nine half-finished features.

The failure had a boring cause. I never wrote down what the project would include, so every good idea looked like part of the job. Since February I've started every side project with a scope agreement, a one-page file that fixes what the project will and won't include.

Writing the page for the first time took me about 45 minutes with nothing more than a text editor. The four steps in this post produce that page in order.

In this post, I'll share:

- how I name the one user
- how I draw the single path through the app
- how I set done criteria and a time budget
- how I test new ideas against the page
- which caveats come with the method
- what changed after the month ended

## 1. Name The One User

Pick one person and write one sentence about them. For my current project, a training log, the sentence is "a runner who trains for one race per season", and that runner is me. I keep the sentence at the top of the page, because every later decision refers back to it.

A test keeps this honest. If you can't name the person and one job they spend their evenings on, the project isn't ready for a scope page. "Everyone who cooks" failed that test for me in January, and the failure cost five weekends.

## 2. Draw The Single Path

Write the one path a user takes from opening the app to the result they wanted. My training-log path has five steps, from "open app" to "see this week's mileage".

Everything off the path goes into a second list called "later". The later list holds 14 entries today, and none of them shipped in March. The list keeps good ideas alive without letting them into the month.

The whole agreement fits in a file called `scope.md` at the repo root, and mine looks like this:

```text
# scope agreement - training log
user: a runner who trains for one race per season
path: open app, log a run, see weekly mileage, export CSV
done: four weekends, five path steps working on my phone
later: social sharing, training plans, shoe tracking, widgets
```

The file has four sections and 15 lines, and it fits on one screen. If the page needs scrolling, the scope has grown past one month of evenings.

## 3. Set The Done Criteria

Done criteria turn the month into a test you can fail. Write them as checks a stranger could run, and give every check a number.

The training log has four done checks:

- the run form saves an entry in under 3 seconds
- the weekly mileage view renders on my phone without a network call
- the CSV export opens in LibreOffice without manual fixes
- the app survives one full session in airplane mode

After the four weekends I ran the checks on my phone in 20 minutes. Three passed, the offline check failed, and the failure ended the month instead of extending it. A finished small project beat an unfinished bigger one, which was the lesson I missed in January.

## 4. Test New Ideas Against The Page

New ideas arrive anyway, so give them a gate. When one shows up, I ask a coding agent to compare it with the page.

The prompt is two lines:

```text
Read scope.md in this repo.
Does this idea fit the user, the path and the done checks: [idea]?
```

The agent answers with the matching section, or it names the conflict. Most ideas go to the later list, and two or three per month genuinely replace something on the path. The gate also works on my own ideas, which are the harder ones to refuse.

## Caveats And Pushback

The method has three known costs:

- the page drifts after the project changes direction
- one user makes the app strange for a second user later
- the later list grows into a shadow backlog nobody reads

A Sunday re-read catches most drift in 10 minutes. The done checks catch the rest, because a check that no longer matches the screen is loud. When a change survives both reviews, I update the page first and write the code second.

The one-user limit is real. When a second runner borrowed the app in April, I gave them a separate data file and changed nothing else. A shared multi-user version would have needed a different page and a different month.

## After The Month Ends

The agreement changed what a finished side project feels like. January produced nine half-features and a stopped repo, while March produced a small app that does one job for one person.

The method doesn't kill side ideas. My later list holds 14 of them, and the March build pulled two improvements from it. The approach still assumes I can name the user from my own life, and a project for a stranger's needs would need interviews first.

I'll write about what happened when the second runner stayed in a future post. If you want to follow along, don't forget to subscribe.
