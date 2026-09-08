# Renaming and rebuilding my AI agents course

I've renamed my AI agents course to AI Engineering Buildcamp. After the first cohort, I also changed the structure and expanded the optional material on other frameworks. I'm re-recording around 90% of the content for the second cohort, which starts in two days.

I wanted the name to describe how we work in the course. Participants build AI systems and deal with engineering questions about reliability and maintainability. They practice making trade-offs while working on projects, so they finish with something they can reuse.

The Capstone starts in the first week, when participants decide what they want to build. They refine the idea as they go through the course and begin implementing it. The final two weeks are reserved for building and polishing that system.

Alongside the Capstone, participants complete six or more guided mini-projects through homework. We build FAQ assistants and systems for asking questions about YouTube videos. Other assignments include documentation agents, coding agents, and deep research agents.

Those smaller projects reinforce individual topics and give participants time to absorb the material. They don't depend on the final Capstone, so there's also practice outside the larger project.

Some first-cohort participants told me they valued the technical depth but found the pace too fast. I wanted people with full-time jobs to be able to follow the course and apply what they learned. I kept the depth, but made the new version longer and less dense.

There's now a main path with one primary framework and a selected set of projects. Each module also has optional material for people who want to try other tools or do more exercises. That separates the work needed to follow the course from the additional topics people can explore.

We still start the agents section without a framework. We implement tool calling and control loops ourselves before introducing abstractions. I want participants to understand what the frameworks are doing, so they can read the code and debug unexpected behavior.

That foundation also helps when an existing framework doesn't fit a project's constraints and you need to implement something yourself.

After that, we use PydanticAI throughout the main path. Focusing on one framework reduces context switching and gives us time to work on typing and validation, as well as testing and production concerns.

The optional material covers other frameworks:

- LangChain and LangGraph
- OpenAI Agents SDK
- Google Agent Development Kit
- CrewAI

OpenAI is our main model provider, but we also cover alternatives such as Groq and Anthropic. Gemini and Z.ai are included in that coverage too.
