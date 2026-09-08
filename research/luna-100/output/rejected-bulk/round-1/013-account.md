# Turning a Bootcamp into AI Engineering



I want to describe what happened, because the sequence of small decisions is more useful than a polished summary. 

One Thing I Want to Share The result Week https://maven.com/alexey-grigorev/from-rag-to-agents?promoCode=

SUBSTACK: 1. I’ve renamed the course 2. Significantly restructured it 3. Expanded the optional framework

coverage All of these changes are a result of feedback from the participants of the first cohort.

https://maven.com/alexey-grigorev/from-rag-to-agents?promoCode=SUBSTACK, which starts in 2 days. In this

newsletter, I want to explain why the name changed, how the course was redesigned, and share what’s new

in this iteration. 1. New Name: AI Engineering Buildcamp I decided to rename the course since the new

name better reflects what it is about: building AI systems with an engineering mindset through hands-on

work instead of learning theory in isolation. Each course participant will: Build real systems

trade-offs, reliability, maintainability Do a lot of hands-on work Finish with concrete, reusable

results AI Engineering Buildcamp is a project-driven course. From the first week, course participants

start working toward their final Capstone Project. In Week 1, participants define what they want to

build. As the course progresses, they gradually refine this idea, first conceptually and then through

implementation, with the final two weeks dedicated entirely to building and polishing the system.

Alongside the Capstone, course participants work on 6+ guided mini-projects through homework

assignments. These include FAQ assistants, YouTube Q&A systems, documentation agents, coding agents, and

deep research agents. These smaller projects are designed to reinforce individual topics and support

gradual material absorption, independent of the final Capstone. 2. New Structure Some of the AI

Engineering Buildcamp course participants from the first cohort shared this feedback with me: “The

content is extremely dense and valuable, but the pace felt too fast.” The new structure maintains the

same technical depth and focus of the course but makes it realistic for people with full-time jobs to

follow, complete, and apply the material. The new version is longer, less dense, and more focused: There

is now a main path built around one primary framework and a selected set of projects. Each module also

includes optional bonus material for those who want broader coverage, alternative tools, or additional

hands-on work. In other words, there’s a clearer separation between core material and optional depth, so

you can easily understand where to put your focus. And you also have more time to process concepts and

practice. https://docs.google.com/document/d/1n9DQlIOGQBtFfsxAeFtOW0AK6u3TT6n3MFz3lc0lkM/edit?usp=sharing

https://docs.google.com/document/d/1n9DQlIOGQBtFfsxAeFtOW0AK6u3TT6n3MFz3lc0lkM/edit?usp=sharing. 3.

Frameworks Philosophy and Updates The course is not framework-driven. The agents section starts without

any framework. We first build agents from scratch and implement tool calling and control loops manually.

The result makes the underlying mechanics explicit before any abstractions are introduced. The result

approach allows you to: Understand how agent frameworks actually work internally Read and reason about

framework source code Debug unexpected behavior instead of guessing Implement your own framework when

existing ones do not fit your constraints Only after this foundation is in place do we introduce

PydanticAI and use it as the primary framework throughout the main path. Focusing on a single framework

reduces context switching and allows us to go deeper into typing, validation, testing, and production

concerns. We’ll also cover other widely used frameworks as optional material: LangChain and LangGraph

OpenAI Agents SDK Google Agent Development Kit CrewAI We use OpenAI as the



That is the part I would keep from this example: connect each tool to the problem that made it necessary, and keep the limitation next to the claim. The details matter because they explain what can be reused and what was specific to this project.
