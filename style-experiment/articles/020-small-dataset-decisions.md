# Making Product Decisions with a Small, Biased Dataset

I wrote this analysis as a synthetic style exercise. Although the survey and measurements are fictional, the argument reflects how I treat directional evidence.

In April 2026, our five-person product team had to decide whether to build offline access for a field-inspection app. We had 47 user interviews, 218 support tickets, and usage logs from 1,190 active accounts. The evidence all pointed the same way, and every source had a clear bias.

In this post, I'll share:

- how we stated the sampling frame before analysis

- why we separated direction from size

- the checks that weakened our confidence

- how we chose a reversible first release

- what evidence would change the decision

## State the sampling frame first

The first rule is to write down where each row came from before drawing any conclusion. A sampling frame describes the population you can actually observe and the mechanism that put people into the dataset.

Our interviews came from 14 customers who had renewed in the previous 12 months. Customer success chose them because they were responsive. Support tickets came from users who cared enough to write to us, and about 38% came from two enterprise accounts.

The usage logs had a different boundary. They included only accounts with telemetry enabled, which covered 71% of active users. Three enterprise customers disabled telemetry because of internal policy, so their workflows were invisible to us.

Those constraints didn't make the data useless. They defined the population about which we could speak: engaged, reachable, mostly enterprise users who had already paid. That group mattered, but it wasn't the whole market.

## Separate direction from size

Small datasets often support a direction more reliably than a precise estimate. We therefore asked whether offline access appeared to matter. We asked separately how large the effect was.

The direction was consistent:

- 31 of 47 interviews mentioned poor connectivity

- 64 of 218 tickets described failed synchronization

- 18 users described paper forms as their current fallback

That evidence made offline access a serious candidate. It didn't tell us that 68% of all users needed offline mode, even though 31 of 47 interviews produced that raw percentage. The renewal-biased interview frame made such precision unjustified.

We wrote the distinction into the decision memo. The direction was "connectivity failures interfere with field work", while the size estimate was "unknown among accounts without telemetry and among non-renewing customers".

## Test the obvious explanation

The strongest competing explanation was simple: poor connectivity could correlate with poor onboarding. Users who didn't understand synchronization might report a network problem when the real issue was configuration.

We checked that explanation with three checks. First, we read a random sample of 40 synchronization tickets and classified each description. Second, we compared ticket rates across account ages. Third, we examined offline events recorded by the app.

The ticket review found 29 reports with explicit network errors, nine with ambiguous descriptions, and two with clear configuration mistakes. Account age didn't show the onboarding structure: tickets were highest between months 7 and 12, after initial setup.

The application logs added the most useful detail. Among telemetry-enabled users, 41% had at least one 10-minute interval with no network connection during field hours. The median offline interval lasted 34 minutes. That evidence didn't depend on user vocabulary or support-channel access.

## Choose a reversible first release

Even with consistent evidence, we avoided a large commitment. Instead of building full offline storage and conflict resolution, we scoped a narrow release that could test the behavior in real work.

The first release had four limits:

- forms cache locally for up to 24 hours

- photos queue separately from form data

- only inspections created after installation can run offline

- synchronized records remain locked for one hour

This version solved the shortest common outage but deliberately didn't handle multi-day trips. It also avoided legacy records, where permissions and data migration made the first version risky. We could remove the feature with less damage if usage didn't justify further work.

We set a review after eight weeks. Success required 100 field users to submit at least one offline-created inspection. The synchronization failure rate also had to stay below 3%. Support logged whether users understood the 24-hour cache limit.

## Define what would change the decision

A small dataset needs an exit condition. Before the release, we wrote down observations that would make us stop or redirect the work.

These results would count against expansion:

- fewer than 25 users create offline inspections in eight weeks

- synchronization failures remain above 8% after cache fixes

- support receives repeated reports about lost older inspections

Low synchronization failure would support expansion. So would evidence that users deliberately save offline inspections for areas with no coverage. We treated the latter as behavioral evidence, stronger than another round of agreement from the same interview panel.

We also named the groups whose evidence was missing. Non-renewing accounts, telemetry-disabled enterprises, and users in regions without support coverage could have different needs. Their absence kept our conclusion provisional.

## Lessons from the decision

The useful issue wasn't whether the dataset was big enough. The issue was whether the data could support the specific decision, at the risk level we were prepared to accept.

Stating the sampling frame made hidden exclusions visible. Separating direction from size prevented an impressive percentage from masquerading as a market measurement. A reversible release let the next evidence come from behavior.

I plan to write next about logging field-product experiments without collecting unnecessary personal data. Subscribe if you want that follow-up.
