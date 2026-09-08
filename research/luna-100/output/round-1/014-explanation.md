# How the AI Engineering Buildcamp Was Structured

The AI Engineering Buildcamp was designed around a simple idea: participants learn AI engineering by building systems. The course name reflected that emphasis. It was project-driven, concerned with trade-offs and reliability, and organized so that the main path stayed focused while optional material provided breadth.

The central project was a Capstone. During the first week, each participant defined what they wanted to build. The idea was refined conceptually and then through implementation. The final two weeks were reserved for building and polishing the result, so the course had a destination from the beginning rather than a collection of disconnected exercises.

The Capstone was supported by more than six guided mini-projects. The examples included FAQ assistants, YouTube Q&A systems, documentation agents, coding agents, and deep research agents. Each smaller project reinforced a particular topic. Participants could therefore practice individual parts of an AI system before bringing those ideas into the larger project.

The projects also gave the course a sequence. A participant could encounter one mechanism in a small assignment, understand its purpose, and later meet the same concern inside the Capstone. This made the larger system a place to apply ideas rather than the first place to discover all of them.

The structure changed after the first cohort reported that the material was valuable but moved too quickly. The redesigned version kept the technical depth while making the workload more realistic for people with full-time jobs. It was longer and less dense. A main route centered on one framework and a selected group of projects gave participants a clear place to focus. Bonus material in each module covered alternative tools and additional hands-on work for those who wanted more breadth.

The framework strategy followed the same separation. The agents section started without a framework. Tool calling and control loops were implemented manually so that participants could see the mechanics before learning an abstraction. That foundation made it easier to understand how frameworks work internally, read their source, debug unexpected behavior, and decide when an existing framework did not fit.

After the manual foundation, PydanticAI became the primary framework for the main path. Concentrating on one framework reduced context switching and left more room for typing, validation, testing, and production concerns. Other frameworks were included as optional material: LangChain, LangGraph, OpenAI Agents SDK, Google Agent Development Kit, and CrewAI.

The same principle applied to model providers. OpenAI was used as the main provider, but the course also covered Groq, Anthropic, Gemini, and Z.ai. This gave participants enough exposure to navigate the wider ecosystem without making every week a comparison exercise.

The resulting design had two levels. The core path taught engineering fundamentals through one sequence of projects and one primary framework. The optional layer let participants explore alternatives after they understood the underlying mechanics. That division addressed the original pacing problem while preserving the course’s hands-on character.
