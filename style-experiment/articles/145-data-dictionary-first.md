# Starting a Data Project with a Data Dictionary

Last year a fictional city called North Harbor asked me to help with its open-data program. Twelve departments published 240 datasets, but the portal contained only titles and short descriptions. One analyst spent two days discovering that `permit_status` used five undocumented values.

I wrote this synthetic style exercise as part of a writing series. The city, departments, datasets, dates and measurements are fictional.

In this post, I'll share:

- how I inventoried the existing datasets
- how I defined fields and types
- how I assigned owners and examples
- how I recorded caveats and data quality rules
- what changed in the first 12 weeks

## Inventory Existing Datasets

We started with a two-week inventory rather than a new portal. I exported dataset metadata to a CSV file, then added one row for every published table and API endpoint. The first pass found 240 datasets, 38 duplicates and 17 endpoints that returned HTML instead of CSV or JSON.

Each inventory row got these columns:

- dataset identifier and publisher
- update frequency and last successful run
- access method and file size
- license and classification
- known downstream users

The inventory revealed the project's first useful fact. Only 63 datasets had changed during the previous six months, while 91 had no recorded update since publication. That gave us a natural order: document the active datasets first.

I tagged 42 datasets as sensitive because small populations made households easy to infer. Those datasets needed review before we copied their fields into a public dictionary.

## Define Fields and Types

For each active dataset, we listed every column in a shared YAML file. YAML stores descriptions, constraints and examples beside the field name, while Git records who changed each definition.

The field record has five required parts:

- name in snake case
- physical type in the source system
- logical type for users
- description in one or two sentences
- allowed values or range

A street-paving record shows the physical and logical distinction. The source stored `completion_date` as the integer `20260418`, but the dictionary typed it as a date and told users to convert it first.

We chose strict types after finding 1,180 missing values stored as `"N/A"`, `9999` and blank strings across 12 datasets. In the dictionary, blanks mean unknown, while `9999` means no applicable value. The ingestion pipeline rejects any other placeholder before it reaches the warehouse.

## Assign Owners and Examples

Every dataset needed one accountable owner and one technical contact. The owner answers definition and release-timing questions, while the technical contact handles extraction failures, schema changes and ingestion schedules.

The ownership record contains:

- department and owner name
- technical contact
- escalation contact for time-sensitive incidents
- review date
- next scheduled publication

Assigning owners was slower than writing field definitions. Some datasets had been published by a former employee, and two departments believed the other owned their shared address table. One-hour departmental meetings resolved 29 of 34 orphaned datasets.

Each field also needs realistic examples: a normal value, a boundary value and a missing-value case. For `building_height_m`, those were `12.4`, `0` for accessory structures and an explicit null for a missing record.

Examples caught several bad assumptions. A budget analyst expected negative expenditures to represent refunds, while the finance team used negative numbers for corrections. After a meeting, the dictionary required a `transaction_reason` field with that distinction made explicit.

## Record Caveats and Quality Rules

In the caveat section, we treat the dictionary as operational documentation rather than a plain schema. We wrote one caveat for every interpretation problem, including seasonality, delayed reports and boundary changes.

Caveats follow a fixed form:

- what the user might misread
- the departments or years affected
- the recommended filter or adjustment
- the date the caveat was confirmed

The building-permit dataset had the clearest example. Inspectors enter completion dates only after final approval, and approvals stop for two weeks in December. Average completion time therefore rises every January, even when inspection activity stays stable.

We encoded quality rules beside the field definitions. A rule has a name, SQL expression, severity and expected action. The permit dictionary contains 22 rules, including 15 warnings and 7 blocking checks. A blocking check stops publication, while a warning enters a review queue.

The first rule run found 260 orphaned permit records because the issuing system had allowed a canceled category. We corrected 241 records from the source database and marked the other 19 as invalid.

## Roll Out in 12 Weeks

We didn't attempt to document all 240 datasets immediately. The first release covered 18 active datasets from three departments: permits, waste collection and public parking. This gave us enough variety to test dates, categories, geographic fields and monetary values.

The rollout had four stages:

- document five datasets and review them with the owners
- publish the dictionary generator and feedback form
- onboard the remaining 13 datasets
- connect quality rules to the nightly publication check

The generator reads the YAML files and creates a static HTML page for each dataset. It fails the build when a field lacks a type, owner, description or examples, preventing undocumented emergency changes.

At week 12, the portal had these results:

- 68 documented datasets
- 112 field-level caveats
- 94 quality rules

The team answered 31 dictionary questions, and 22 produced a definition change. They published each correction in 2.4 days on average.

## Results and Remaining Work

The clearest result appeared in onboarding. A new analyst needed 4.5 hours for a simple permit-time report, compared with an estimated 16 hours before the dictionary. Two departments reused the parking schema for a new pilot without asking for another extract.

The feedback form received 41 submissions, with 19 requests for more history. Thirteen submissions reported a broken link or failed update, and nine questioned a definition. Every question now has an owner, a response and a recorded outcome.

We still have ownerless fields, changing geography and approval workflow to resolve. Some legacy datasets have fields with no traceable owner, so their records can't answer a question about responsibility. Geographic boundaries change annually, and the dictionary doesn't yet show the boundary version used by each historical row.

Two departments want row-level approval before every update, which conflicts with the current nightly schedule.

## Closing Notes

The dictionary made ownership visible before the project changed any code. Once fields had examples and caveats, conversations moved from guessing meanings to deciding what should change.

Starting with 18 datasets was the right decision. It gave us a safe way to test the template, generator and quality checks.

I'll write more about the boundary-version problem in another article. Subscribe to stay updated.
