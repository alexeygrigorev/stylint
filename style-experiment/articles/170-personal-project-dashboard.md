# Building a Dashboard for Side Projects and Deadlines

This synthetic style exercise invents the projects, dates, and measurements. In January 2026, I had 11 active side projects in four tools: two task managers, a notes folder, and a spreadsheet. One course deadline appeared in only three of them, and I found it two days before the due date.

I didn't need another productivity method. I needed one page that could answer three questions: what is active, what is next, and what did I touch this week?

In this post, I'll share:

- how I chose the dashboard's data model
- which status fields survived testing
- how next actions stay visible
- how the weekly snapshot is generated
- what still remains manual

## Start With the Data Model

My first attempt imported every task from every tool. It produced 640 rows and hid the two deadlines I actually cared about. The dashboard was comprehensive and useless.

So I reduced the unit to a project record. Each project has a name, state, deadline, owner, repository URL, and one next action. Tasks stay in their original systems. The dashboard only knows the first step I've committed to.

The initial model had these fields:

- project name
- state
- deadline
- repository URL
- next action
- last touched date
- weekly goal

Eleven projects looked manageable on paper. When I added three dormant projects, the list told a more honest story about my available evenings.

I put the data in a SQLite database and kept a YAML export for review. The schema has 14 columns, and a Python script validates dates, states, and URL formats on every sync.

## Choose Few Statuses

My first version allowed states such as "waiting", "paused", "exploring", "blocked", and "maintenance". They felt precise, but I couldn't decide where several projects belonged.

After six weeks, the production dashboard uses only four states:

- active
- paused
- waiting
- done

Active means I plan to touch it this week. Paused means I don't plan to touch it, but I want to keep the context. Waiting means another person or event controls the next move. Done means the deliverable exists.

A project can have a deadline while paused. The deadline still appears, but the row uses a muted color and shows "paused" next to the date. That distinction prevented a false sense of urgency.

I also added a rule for aging rows. If an active project has no changed next action or repository commit for 21 days, the dashboard marks it stale. In February, that rule moved four projects to paused.

## Make Next Actions Concrete

The useful next action fits one line and starts with a verb. "Improve search" was accurate and useless. "Run 20 queries and record which documents miss" told me what to do after dinner.

Every evening sync shows only the next action:

- prepare 10 evaluation queries for Localpress
- deploy the static preview for Coursekit
- write the migration for two new invoice fields
- review the 32 unanswered workshop questions

When I complete an action, the script moves the project back to the top of the review list. It doesn't invent the following step. The empty field is a prompt to spend two minutes planning.

The dashboard groups actions into three time buckets: today, this week, and later. The later bucket is capped at 12 items. Anything beyond that has to return to its project notes instead of pretending to be a plan.

I also show the last repository event next to each action. For three projects, the next action depended on a pull request. Seeing "PR open for 6 days" led me to review them before starting anything new.

## Generate the Weekly Snapshot

Every Monday at 08:00, a Python script builds a one-page snapshot and sends it to my notes folder. It uses a cron job on the same small server that runs the dashboard.

The snapshot has four sections:

- projects touched in the last 7 days
- deadlines in the next 30 days
- stale active projects
- one selected focus project

Last week's fictional snapshot said I touched 7 of 14 projects. I made 31 commits, closed 9 next actions, and created 11 more. Two deadlines fell within 14 days. Three active projects had been untouched for more than three weeks.

Those numbers changed my plan. I paused Localpress and moved Coursekit's static preview to Monday evening. The full review took 18 minutes instead of the previous 50-minute tour through four tools.

The snapshot also compares planned weekly goals with completed actions. I don't treat it as a performance score. A week with 3 finished actions can be correct if one of them was a migration.

The generated page uses no JavaScript and weighs 18 KB. That makes it easy to open on my phone when the main dashboard is unavailable.

## Keep the Manual Part

Some data resists automation. Repository commits show activity, but they don't show whether the activity was useful. A project can have 20 commits and still have no deliverable.

So I keep two manual rituals: a five-minute evening review and a Monday decision. The dashboard prepares both, but it doesn't choose the focus project for me.

I also enter new projects by hand. The form asks for the first next action before it saves the project. That small friction has stopped three ideas from becoming rows with no next step.

## What I've Learned

A useful personal dashboard is mostly editing. Four states, one next action per project, and one weekly page did more than another integration.

The next version will add a one-month review, but I'll keep it separate from the Monday snapshot. Monthly decisions need trends; Monday decisions need the next action.

I'll write more about connecting this dashboard to project repositories in a future post. Subscribe if you want the update.
