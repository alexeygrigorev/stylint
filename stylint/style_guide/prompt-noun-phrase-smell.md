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

For each sentence, ask:

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

For each change, give the original line and your rewrite, then apply it. If a
page has no offenders, say so plainly and change nothing.
