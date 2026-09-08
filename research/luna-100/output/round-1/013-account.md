# Why I Renamed My AI Agents Course

The first cohort of my AI agents course gave me a lot of feedback. Three changes followed from it: I renamed the course, restructured the material, and expanded the optional framework coverage. I was re-recording around 90 percent of the content for the second cohort, which was due to start in two days.

The new name was AI Engineering Buildcamp. “AI agents” described the topic, but it did not describe how I wanted participants to work. The course was about building AI systems with an engineering mindset, through practical projects rather than theory in isolation. Participants would make real systems, deal with trade-offs, reliability, and maintainability, and finish with results they could reuse.

The course was project-driven from the first week. Participants defined a Capstone Project immediately, then refined it first as an idea and later through implementation. The final two weeks were reserved for building and polishing that system. Alongside the Capstone, homework included more than six smaller projects: FAQ assistants, YouTube question-and-answer systems, documentation agents, coding agents, and deep research agents. Those projects covered individual topics and gave people a gradual way to absorb the material.

This sequence also made the expected result concrete. Participants were not only collecting explanations about agents; they were accumulating working pieces and a larger system that could be revisited throughout the course. The mini-projects gave the Capstone a practical context.

The first cohort also gave me a clear problem with the pace. One piece of feedback said the content was dense and valuable, but moved too quickly. The technical depth would stay, but the schedule had to become realistic for people with full-time jobs. I made the new version longer and less dense, with a clearer main path.

The main path used one primary framework and a selected set of projects. Each module also had optional material for participants who wanted alternative tools, wider framework coverage, or more practice. Separating the core from the optional depth made it easier to see where to focus and gave participants more time to process concepts.

I kept the framework philosophy deliberately narrow at first. The agents section starts without a framework. We implement tool calling and control loops ourselves, so the underlying mechanics are visible before an abstraction is introduced. Only after that foundation do we use PydanticAI as the primary framework, where the course can go deeper into typing, validation, testing, and production concerns.

Other frameworks remained available as optional material: LangChain and LangGraph, OpenAI Agents SDK, Google Agent Development Kit, and CrewAI. The same applied to model providers. OpenAI was the main provider, but the course also covered Groq, Anthropic, Gemini, and Z.ai.

The changes were a response to participants rather than a change of subject. The Buildcamp kept its focus on reliable, hands-on systems, but made the path easier to follow and the surrounding ecosystem easier to explore.
