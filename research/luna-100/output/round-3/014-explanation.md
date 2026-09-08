# Following the AI Engineering Buildcamp curriculum

In AI Engineering Buildcamp, you start with something you want to build. During the first week, you define your Capstone Project, then refine it as you work through the material and begin implementing the system. The final two weeks are devoted to building and polishing it.

I renamed the course to reflect that work. You practice AI engineering through projects, including the decisions needed to make a system reliable and maintainable. You should finish with results you can reuse after the course.

There are also six or more guided mini-projects in the homework. You build FAQ assistants and YouTube question-and-answer systems, then work on projects such as documentation agents. Coding agents and deep research agents are included too.

These smaller assignments reinforce individual topics independently of the Capstone. You can practice what you've just learned without having to make every exercise part of the same final system.

The first cohort helped me see that the schedule needed changing. Participants valued the content but told me it was too dense and moved too quickly. I wanted the course to remain technically detailed while becoming realistic for people with full-time jobs.

The redesigned version is longer and gives you more time to process concepts and practice. A main path takes you through a selected set of projects using one primary framework. Each module has optional material if you want broader coverage or more hands-on work.

When we reach agents, we begin without a framework. We build tool calling and the control loop manually, so you can see the mechanics before using abstractions.

This helps you understand how an agent framework works internally. You can read its source and reason about what it's doing when something unexpected happens. If the existing frameworks don't fit your constraints, you also have a basis for implementing your own.

We introduce PydanticAI after that foundation and use it throughout the main path. Staying with one framework reduces context switching. It leaves more time for typing and validation, as well as testing and the concerns that appear in production.

You can explore other frameworks through the optional material:

- LangChain and LangGraph
- OpenAI Agents SDK
- Google Agent Development Kit
- CrewAI

We use OpenAI as the main model provider without tying the course exclusively to it. You also work with alternatives such as Groq and Anthropic, along with Gemini and Z.ai.
