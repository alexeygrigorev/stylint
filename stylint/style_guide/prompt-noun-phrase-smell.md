# Review prompt: noun phrase doing hidden work

Review the text for concrete noun phrases that do too much explanatory work.
Be strict. This isn't the same as `abstract-subject`.

The subject may be concrete, while the sentence hides the real actor:

- the person
- the sequence
- the command
- the constraint
- the design pressure

## Target

Look for a sentence where a noun phrase acts like it decides or explains the
work.

Watch especially for these verbs:

- `defines`
- `starts`
- `becomes`
- `moves`
- `owns`
- `drives`
- `lets`
- `allows`
- `enables`
- `needs`
- `expects`
- `requires`
- `collides`
- `stays`
- `keeps`

Common subjects include:

- the frontend
- the backend
- the database
- the app
- the stack
- the setup
- the service
- the workflow
- the prompt
- the code
- the implementation
- the file
- the index
- the data
- the workshop
- the page
- the section
- the tutorial
- the reader
- the user
- the mock
- the root
- the repo
- two apps

The noun may be concrete. The smell appears when the sentence makes that noun
the actor for a decision or transformation. A person made the decision, a
command caused the change, or a design constraint forced it.

These forms usually need a rewrite:

- `The database starts as SQLite for local work, with zero setup, and becomes
  Postgres once we move into containers.`
- `We start with the frontend, because the frontend defines what the app does.`
- `The backend turns into the API contract for the frontend.`
- `The prompt becomes the source of truth for the agent.`
- `The setup moves into Docker Compose.`
- `The implementation grows into a reusable library.`
- `Add the few tools the rest of the workshop needs.`
- `The mock exists so the frontend stays usable and demoable on its own.`
- `Two apps at the root would collide.`
- `The app lets you do all of this.`
- `The frontend stays usable on its own.`
- `The workshop needs a few more tools.`
- `The root needs to make room for the backend.`
- `The service layer owns the backend choice.`

## Named tools as actors

A named tool, product, library, framework, or service is a second kind of
suspect subject. Examples: `Lovable`, `FastAPI`, `SQLAlchemy`, `Docker`,
`AWS`, `GitHub Actions`, `Claude Code`, `Postgres`.

The smell: the tool is the subject, but the sentence really describes the job
we gave it in our project. The tool didn't decide anything. We picked it and
assigned it that job. Stack overviews and "how we built it" paragraphs hide
this most often, because every clause reads like a plausible fact.

Recall comes first. Apply this decision test to every clause where a named
tool does a job or is assigned one, whether or not the tool is the grammatical
subject. Don't skip a clause because it sounds technical or correct, because
the tool name looks like an ordinary English word, or because the clause sits
inside a list, a table, or a longer sentence.

1. Role or runtime? Ask: does the sentence describe the part this tool plays in
   our project (which layer or area it covers, which job we handed it), or
   does it describe a concrete operation the tool performs when it runs?
2. Verb test: these verbs usually signal a role, not an operation: `handles`,
   `takes care of`, `drives`, `manages`, `covers`, `owns`, `is responsible
   for`, `talks to`, `runs the backend`, and `generates` or `builds` with a
   whole layer as the object (`the frontend`, `the backend`, `the API`). A
   concrete operation on a concrete input, output, file, or event usually
   signals runtime behavior: `reads <file>`, `writes <records>`, `generates
   <artifact> from <input>`, `starts <service>`, `rebuilds <output> on
   <event>`, `returns`, `serves <path>`.
3. Anyone test: would the sentence be true for every project that uses this
   tool, because the tool does it by itself as part of how it works? If yes,
   it's runtime behavior. Leave it alone. A concrete verb doesn't pass this
   test by itself. If the operation happens only because we prompted,
   configured, scripted, or deployed the tool to do it, it fails the test and
   it's a role, however concrete the verb and object are.
4. Swap test, as a tiebreaker only: replace the tool with a competitor that
   could fill the same slot (Lovable with Bolt, FastAPI with Flask, GitHub
   Actions with GitLab CI). If the sentence is a bare assignment of a slice of
   the project ("X does our frontend", "X does deployment"), it's a role
   statement. A concrete operation stays fine even if a competitor could also
   perform it.

Generating, running, or handling something doesn't make it runtime behavior.
What matters is whether the object is a mechanism the tool always performs or
a slice of our project that we assigned to it.

A setting we chose turns runtime behavior into a role. If the clause places the
tool's normal behavior in our pipeline, infrastructure, environment, or
audience (`in CI`, `on AWS`, `in production`, `on our server`, `for our
users`), we put it there, so flag it and name us as the actor: `In <setting>,
we <do the job> with <Tool>.` A trigger or condition that belongs to the
tool's own mechanism isn't a setting we chose: `when a file changes`, `on each
request`, `from the routes`, `at startup`.

AI coding agents, assistants, chatbots, subagents, and our own commands and
skills that drive an agent count as tools, named or not (`the assistant`, `the
agent`, `the /deploy command`). Our own ordinary code (a bot, a class, a
function, a script) doing what we wrote it to do is literal component behavior,
so it's `runtime`. An agent does whatever we prompt it to do, so every piece of
project work it performs is work we directed, including concrete steps:
`<Agent> reads <our file> and produces <our artifact>`, `<Agent> installs
<packages> and creates <module>`, `it watches <source> and responds to
<events>`, `<our command> reads <N> files and edits <M>`. Flag these and name
who directs the agent: `We ask <Agent> to <step>`, `We use <Agent> to <job>`,
`When I run <command>, I have the agent <step>`. Only a built-in mechanism of
the product, which happens for every user without a task-specific prompt, stays
fine: `<Agent> reads <its config file> at startup`, `<Agent> asks for
permission before running a command`, `<Agent> compacts the context when the
window fills up`. A clause that reports a mistake or default the agent made on
its own (`the agent assumed <default>`) is also fine, because nobody assigned
it.

Configured behavior is a role too. When a tool does something only because of
configuration, code, or infrastructure we wrote (proxy rules, build stages,
pipeline rules, IAM or RBAC permissions we granted, resources our template
created, the routes our app serves), we are the actor: `<Tool> proxies <path>
to <service>` becomes `We configure <Tool> to proxy <path> to <service>`, and
`its role can read <resources>` becomes `we let it read <resources>`. When the
tool serves, builds, or deploys our app, that's configured behavior too.

Don't stretch this rule to a tool's standard function. A tool doing the thing
it exists to do, stated with a concrete verb and object, stays fine even though
we chose the tool, it works on our data, or we switched on a standard mode or
flag: a compiler emitting a binary, a linter reporting an unused import, a
queue redelivering an unacknowledged message, a search index ranking results.
What turns it into a role is a role verb (`handles`, `takes care of`, `talks
to`), a whole layer or area as the object, a setting we chose (`in CI`), or
behavior whose details come from our own configuration (which paths, which
stages, which permissions, what gets served).

Contrasted division of labor is a role too. When the text explicitly
contrasts what each tool is responsible for in a design (`<Tool A> does X,
while <Tool B> does Y`, `<Tool A> covers X. <Tool B>, in contrast, does Y`),
each clause states the part that someone assigned to that tool, even if the
verb names its standard function. Flag every clause in the contrast and name
who designed it. A plain list of what each tool does, with no contrast between
them, falls back to the rules above.

This applies to other teams' projects in case studies too. If a company or a
student built the setup, their tool choices are roles they assigned, and the
rewrite names them: `<Team> runs <agent> in <setting>`.

### Three labels

Label every entry `role`, `borderline`, or `runtime`:

- `role`: the decision test says it's a job we assigned. Rewrite it.
- `borderline`: the rules point both ways. Report it with a one-line reason
  and a suggested rewrite, but don't apply the rewrite. The author decides.
- `runtime`: the tool's own behavior, or not this smell. Leave it.

Use `borderline` in these cases, and only when nothing else in the clause
makes it a clear `role`:

- A standard function placed in a phase or environment that may or may not be
  our choice, such as a development phase or a local machine. (`in CI`, `on
  AWS`, `in production`, and `for our users` are clear settings, so they stay
  `role`.)
- A requirement or limit stated about a tool (`<Tool> needs <N> variables`,
  `<Tool> requires <X>`), where the hidden actor is only the person who
  supplies it.
- An explicit request already names us in the same sentence or in the lead-in
  right before it, and the clause only reports the tool carrying out that same
  task: `We ask <Agent> for <artifact>. <Agent> reads <file> and produces
  <artifact>.`, or a list whose lead-in says `We assign these roles to
  agents:`. Only request verbs count here: ask, tell, prompt, have <Agent> do,
  give <Agent> the job. Picking, switching to, or moving to a tool is a choice,
  not a request, so a later clause where the tool does the work stays `role`.
- A behavior that could be the tool's built-in default or our configuration,
  and the text doesn't say which.

### What to skip

Some text isn't the author's to reword, and some text has no tool acting.
Don't rewrite these:

- Verbatim prompts, quoted speech, quotations, code blocks, command output,
  and diagram source code (such as Mermaid). If the enumeration meets one,
  list it as `quoted - skip` with no rewrite. Image alt text, captions, and
  illustration descriptions are the author's own prose, so check them.
- Imperative instructions to the reader (`Run the tests with <Tool>`, `Deploy
  with <Tool>`, `Set up <Tool> for <job>`). The reader is the implied subject
  and the tool is the instrument. List them as `imperative - skip`.
- Clauses whose subject is a policy level, a rule, a file, a step, or a test
  suite, and no tool is named or clearly referred to. They may have other
  smells from the general pass, but they aren't entries here.
- General claims about what a category of tools does everywhere, not in a
  specific project, ours or a case study's (`<Tool category> speeds up
  <task>`, `Chat assistants answer in many languages`). Label them `runtime`, or
  `borderline` if they use a role verb such as `handles`.

Stack lists and tables without verbs: a list or table that pairs jobs with
tools in noun phrases (`- a <Framework> backend in <Language>`, `- <Tool> for
<job>`, `| <job> | <Tool> |`) is one entry for the whole list, not one per
item. If the lead-in names who chose (`We use:`, `We picked:`), label it
`runtime`. If nothing names an actor (`The stack is:`, a table with only
`Area | Tool` headers), label it `role` and rewrite the lead-in to name us
(`We picked an ordinary stack:`). When there's no lead-in to fix, rewrite the
items themselves.

Grouping keeps one problem from being counted many times:

- Several verbs that share one tool as subject in the same sentence form one
  entry (`It <does A>, <does B>, and <does C>`). Different tools in the same
  sentence stay separate entries, even when they share one verb.
- An item that names our agent or command and its job, together with the
  bullets under it that list that agent's steps, forms one entry, labelled by
  the strongest part.
- A tool used as the instrument inside another tool's or agent's step
  (`<Agent> fetches <X> via <Tool>`, `<Agent> used <Tool> to <step>`) belongs
  to that step's entry. It doesn't get its own entry.

### Forms that hide the smell

The tool doesn't have to be the grammatical subject. Check each of these forms
and treat every hit like a sentence with the tool as subject:

- Passive voice with the tool as agent: `<job> is handled/done/generated/run
  by <Tool>.`
- The layer or job as subject, with the tool after the verb: `<layer> comes
  from <Tool>`, `<layer> runs on <Tool>`, `<layer> lives in <Tool>`, `<layer>
  is <Tool>`, `<job> is <Tool>'s job`, `<job> goes through <Tool>`.
- Possessives: `<Tool>'s job/role/part is <job>`.
- Our own component, project, platform, skill, or command as the subject of a
  tool choice: `<component> uses <Tool> to <job>`, `<component> is built on
  <Tool>`, `<component> does <job> through/via/with <Tool>`. We chose the tool,
  so name us: `We use <Tool> in <component> to <job>`. This includes
  architecture descriptions in image comments, alt text, and diagram notes.
- A pronoun or short noun that refers back to a tool: `We picked <Tool>. It
  <does the job>.` Resolve `it`, `they`, `this`, `the tool`, `the service`, and
  `the platform` to the tool they name, then test that clause.
- Relative and appositive clauses: `<Tool>, which <does the job>, ...`,
  `<Tool>, our <job> layer, ...`, `..., with <Tool> doing <job>.`
- Gerund and `with` absolutes: `With <Tool> <doing the job>, we ...`,
  `<Tool> <doing the job>, we ...`.
- A tool in the middle of a sentence, after an intro clause or a conjunction:
  `Once <condition>, <Tool> <does the job>.`
- Tool lists split across clauses or sentences: give each tool its own entry,
  even when one verb covers several tools.
- Bullet items, table cells, image captions, alt text, diagram descriptions,
  and headings: treat each one as its own clause. A caption that describes what
  a tool did in a screenshot of our run counts. A cell like
  `| Hosting | <Tool> takes care of it |` or a bullet like
  `- <Tool> does <job>` counts.
- Product names that look like ordinary words or verbs, such as `Lovable`,
  `Cursor`, `Bolt`, `Linear`, `Render`, `Railway`, `Vite`, `Next`. When a
  capitalized word names a product, treat it as a tool.

Flag (role in our project):

- `Lovable generates the React frontend, FastAPI runs the backend, and
  SQLAlchemy talks to SQLite or Postgres.`
- `Docker, AWS, and GitHub Actions handle deployment.`

Rewrite with `we` as the actor and the tool as the instrument:

- `We generate the React frontend with Lovable, write the backend in FastAPI,
  and use SQLAlchemy with SQLite or Postgres.`
- `For deployment, we use Docker, AWS, and GitHub Actions.`

Leave alone (runtime behavior, true for anyone who uses the tool):

- `FastAPI generates live documentation at /docs from the routes.`
- `Claude Code reads CLAUDE.md.`
- `Docker Compose starts Postgres.`

## Search checklist

Don't rely on intuition alone.

Make a deliberate pass for these surface patterns:

- `The <component> defines...`
- `The <component> starts as...`
- `The <component> becomes...`
- `The <component> turns into...`
- `The <component> moves into...`
- `The <component> owns/drives/controls...`
- `The <component> lets/allows/enables you...`
- `The <component> needs/requires/expects...`
- `The <component> stays/remains usable/demoable/clean/simple...`
- `The <component> exists so...`
- `<component> and <component> would collide...`
- `two apps at the root...`
- `the rest of the workshop needs...`
- `the app lets you do all of this...`
- `you can do all of this...`
- `this keeps the frontend/backend/app...`
- `this makes replacing/switching/moving... easier`
- `so replacing it later is easier`

Treat these as suspect subjects whenever they appear before one of those verbs:

- `app`
- `frontend`
- `backend`
- `database`
- `mock`
- `repo`
- `root`
- `stack`
- `setup`
- `service layer`
- `OpenAPI spec`
- `Docker Compose`

## The Test

Start with a required enumeration step. Before you judge anything, read the
text line by line, including lists, tables, captions, and headings, and list
every clause where a named tool, product, library, framework, service, AI
agent, or our own command or script does a job or is assigned one. Include
all the forms from "Forms that hide the smell", not only clauses with the tool
as grammatical subject. Split compound sentences into one entry per tool,
so `X does A, Y does B, and Z does C` gives three entries, and a list of tools
sharing one verb gives one entry per tool. Follow the grouping rules in "What
to skip" for verbs that share one subject and for an agent's list of steps.
Mark the skips from "What to skip" as `quoted - skip` or `imperative - skip`.
Label every other entry `role`, `borderline`, or `runtime` with the decision
test from "Named tools as actors". Give a one-line reason for each. Don't drop
an entry because it looks harmless.

Then, for each sentence, ask:

1. Find the grammatical subject.
2. Check whether that subject is a component, document, file, process, setup
   noun, or summary noun.
3. Check whether the verb does design, decision, sequencing, ownership, or
   explanation work.
4. Treat these verbs and phrases as common offenders:
   - `defines`
   - `decides`
   - `starts`
   - `becomes`
   - `turns into`
   - `moves into`
   - `switches to`
   - `forces`
   - `owns`
   - `drives`
   - `grows into`
   - `ends up as`
   - `lets you`
   - `allows you`
   - `enables`
   - `needs`
   - `requires`
   - `stays`
   - `keeps`
   - `exists so`
   - `would collide`
5. Name the person, command, dependency, constraint, or sequence that actually
   causes the change.

When that hidden actor exists, rewrite the sentence, but leave literal
component behavior alone. `The function returns a list`, `The frontend calls
the backend`, and `The database stores scores` are fine.

## Fix

Rewrite with the hidden actor, decision, or constraint made explicit.

Use these transformations.

- For tool choice over time, split the stages:
  `We use SQLite locally because it needs no setup. In containers, we switch
  to Postgres so the app uses the same database engine it will use in
  production.`
- For "X defines Y", name what X forces you to decide:
  `We start with the frontend because the screens force us to name the game
  states, API calls, and data the backend must support.`
- For "X becomes Y", name the action:
  `We copy the settings into Docker Compose` or `we use the prompt as the
  source of truth for the agent`.
- For "X moves into Y", name who moves it and where:
  `We move the database config into Docker Compose`.
- For "X grows into Y", name the repeated action:
  `After we reuse the helper in three places, we extract it into a library`.
- For "The app lets you do X", address the reader:
  `You can play both modes, submit a score, open the leaderboard, sign up, and
  watch the spectate page`.
- For "X stays usable", name the design choice:
  `We keep the mock backend so we can play and test the frontend before the
  real API exists`.
- For "the workshop needs X", name who needs it:
  `We need these tools for the rest of the workshop`.
- For "the mock exists so X", name why we ask for it:
  `We ask Lovable for a mock backend so we can keep testing the frontend before
  the real API exists`.
- For "X would collide", name the filesystem constraint:
  `If React and FastAPI both live at the repo root, their package files and
  commands compete for the same directory. We move the React app to
  frontend/ before adding backend/`.

Prefer `we` or `you` when the workshop author or reader is doing the work.
Name a tool or command only when it's the real actor. `Docker Compose starts
Postgres` is fine.

If the rewrite says only that something is "easier", name why.

Concrete reasons include:

- fewer files changed
- one service layer swapped
- one command run
- no local install
- no CORS error
- no root-level package collision

The rewrite must pass this quality gate:

- Don't keep `all of this`, `this`, `that`, or `it` as the main object when the
  original hid concrete actions.
- Name the concrete actions, files, commands, screens, endpoints, or constraint.
- If the original says `The app lets you do all of this`, the rewrite must list
  what the reader can do.

## Leave Alone

Leave these cases alone:

- Compatibility or availability claims where the tool is only the place
  something runs and gets no job: `The prompts work the same way in <Tool A>
  or <Tool B>`, `<Tool> supports <feature>`.

- Literal component behavior: `The database stores scores.`
- Literal API behavior: `The function returns a list.`
- Concrete UI behavior: `The frontend calls the scores endpoint.`
- Specific measured changes: `The latency drops from 800ms to 120ms.`
- Sentences where the noun is the topic but the actor is still clear:
  `In Docker Compose, we run Postgres next to the app.`

When the source doesn't say why the decision happened, make the action explicit
and keep the reason out.

## Output

Use this reporting format:

First, give the named-tool enumeration: each clause where a named tool does
or is assigned a job, its label (`role`, `borderline`, `runtime`, `quoted -
skip`, or `imperative - skip`), and the one-line reason. End it with the count
for each label.

Then list the `role` rewrites. For each one, give the original line and your
rewrite, then apply it. Include rewrites from the general noun-phrase pass
here too.

Then give a separate list headed "Borderline - author decides". For each
entry, give the original line, the one-line reason, and a suggested rewrite.
Don't apply these.

If a page has no offenders, say so plainly and change nothing.
