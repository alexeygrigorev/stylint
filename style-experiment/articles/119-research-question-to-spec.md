# Moving from a Research Question to a Buildable Specification

I wrote this synthetic style exercise as a how-to guide. The research project, data, dates and measurements are fictional.

In January, a fictional community energy cooperative asked whether its 12 solar installations could shift laundry demand into sunny hours. That was an interesting research question and a poor software ticket. It contained no data schema, no intervention, no success threshold and no boundary around cost.

I made the same mistake in an earlier project. I spent three weeks building a recommendation panel before anyone defined what "better" meant. The panel showed five appliances, but the operators couldn't tell which one to turn on first.

In this post, I'll share:

- how I turned the question into a testable hypothesis
- how to specify the data before writing code
- how to choose a method and a comparison
- how to define success before the pilot
- how to write a scope that survives review

## 1. Write a Testable Hypothesis

Start by naming the intervention and the expected outcome because the original wording mixed weather, behavior and pricing. We narrowed the intervention to a two-hour appliance window based on the next day's forecast.

Our hypothesis said households would run at least 30% of weekly washing-machine cycles inside those windows.

That sentence forces these decisions:

- the intervention is one message with a two-hour window
- the unit of analysis is a household week
- the outcome is the share of cycles inside the window
- 30% is the minimum useful change

We rejected a broader hypothesis about total carbon savings. That outcome depends on grid mix, battery control and tariffs, and the cooperative couldn't change all three in one pilot. A narrower claim was easier to falsify.

## 2. Specify the Data Before Code

The next step is to write down the fields, granularity and limits. Our specification has one section per input, even when the input seems obvious.

The first version looked like this:

```text
meter_data:
  source: 15-minute interval meter export
  period: 2025-01-01 through 2025-12-31
  required fields: household_id, timestamp, kwh
  known issues: 11 households have gaps during meter replacement
appliance_events:
  source: smart-plug event log
  period: 2025-06-01 through 2025-12-31
  required fields: household_id, device_id, start_time, end_time, cycle_flag
  known issues: 14 devices report start time only
```

Writing this exposed a timing limit before implementation. Appliance events start six months later than meter data, so a full-year baseline is impossible.

Smart-plug coverage added a second limit: only 68 of 94 households had the devices, so the pilot could measure that sample alone.

We then agreed on the exact derivation of a cycle. A cycle starts when plug power exceeds 150 watts, continues while power remains above 80 watts, and ends after 10 minutes below that threshold. Runs under 25 minutes are discarded because they're mostly test loads. That rule is boring and essential.

## 3. Choose One Method and Comparison

A specification needs a method the team can actually execute. We considered a randomized rollout, a matched comparison and a before-and-after study. The cooperative had 94 households and eight weeks, so we used a matched comparison.

Households were grouped by baseline consumption, appliance ownership, household size and timezone. Within each group, we assigned 24 households to receive windows and 24 to continue as usual. The remaining 46 households stayed out of the pilot because their plugs had been installed after 1 December.

The analysis plan has these steps:

- compute each household's weekly in-window cycle share
- compare treatment and control groups within matched strata
- report the difference with a 95% confidence interval

We didn't promise a causal estimate beyond the matched sample. The specification says the result applies to plug-in washing machines in the 48 pilot households. That limitation is part of the method, not a later apology.

## 4. Define Success Before the Pilot

The cooperative needed a threshold that would justify continued work.

We wrote the success rules before assigning households:

- primary success: treatment households average 30% or more in-window cycles
- secondary success: treatment households average at least 10 percentage points more than controls
- operational success: at least 70% of households open two of three messages
- failure rule: below 10% in-window use, stop the current message design

We separate behavioral effect from delivery reliability in those rules. In week 2, 76% of households opened at least two messages, so the delivery path passed. At week 4, treatment households ran 22% of cycles in-window while controls ran 8%. The result encouraged us to continue, but it didn't yet meet the 30% primary threshold.

By week 8, the treatment share reached 34%, and the difference from controls was 19 percentage points. We could therefore say the two-hour message met the primary and secondary thresholds for that sample.

## 5. Write Scope and Stop Rules

Our scope section limits what the project will build.

Our scope has these four parts:

- one message channel, sent at 18:00 the evening before
- one appliance, measured by smart plugs already installed
- eight weeks of measurement and no automatic appliance control
- a report and reusable analysis notebook, with no production app

Each exclusion had a reason. Automatic control would require safety review, additional hardware and liability discussion. A production app would delay the behavioral test by months. The cooperative needed evidence before it asked members to install anything else.

We also wrote stop rules. If fewer than 70% of households receive messages, we stop and fix delivery. If more than 12% of participants ask to leave, we stop and interview them. If meter or plug data is missing for more than 20% of household weeks, we pause analysis rather than impute the missing weeks.

That scope made review fast. The board read five pages, asked four questions and approved the pilot in one 40-minute meeting.

## Lessons From the Specification

A specification is a set of promises about evidence. It names the intervention, the data, the comparison and the threshold before the first notebook runs. It also records what the project won't do.

The discipline slows down the first week. In this project, we spent 11 hours on the hypothesis, data inventory, success rules and scope. We saved that time later because the board, the analyst and the volunteers worked from the same five pages.

My next step is to turn the five-page specification into a template for the cooperative's smaller projects. I'll write about that template after two more pilots. If you want to follow along, don't forget to subscribe.
