# Choosing a Portfolio Project When Everything Looks Interesting

Last month I reviewed 27 job descriptions for AI engineering roles. Sixteen mentioned retrieval, nine mentioned evaluation, and eleven asked for experience with production systems. I turned those numbers into a short selection method for portfolio projects.

I generated the projects and measurements for this piece as a synthetic style exercise. I use the fictional details to practice a concrete practitioner build-log voice.

In this post, I'll share:

- how to turn job postings into project options
- why narrow portfolio projects survive review better than broad demos
- how I score an idea before writing code
- what to put in the repository before a recruiter opens it
- how to test whether the project says what you claim

## 1. Read Postings as Problem Lists

The obvious approach is to copy a hot topic and start coding. I tried that in 2024 with a generic chatbot. It had 40 lines of prompt logic, no evaluation set, and no way to explain a failure.

So I changed the input. I collected 27 postings in one folder, highlighted every task statement, and rewrote each task as a problem in plain language. A sentence about "RAG systems" became "customers need grounded answers from 3,000 internal PDFs".

That rewriting exposed the parts recruiters actually care about. The postings talked about retrieval only after they defined the surrounding product context.

Every project idea then had to define three fields:

- the corpus or input data
- the user and their workflow
- the accuracy requirement

## 2. Choose a Narrow User and Dataset

Each candidate needs one user and one concrete dataset. "Developers who want API help" is broad, while "backend engineers who need answers from a 180-page internal API guide" is reviewable.

I wrote this filter before choosing the technology, and it removed three ideas immediately, including a support bot with no tickets. All three looked impressive and couldn't demonstrate much.

A useful portfolio project should fit on one page, and I use this template:

```text
User: junior backend engineers
Input: 180-page API guide and 50 realistic questions
Output: answer, page number, short quotation
Success: 80% accepted in human review
Out of scope: personal accounts, live API calls, mobile interface
```

The scope line matters as much as the success line. If a reviewer can see the exclusions, they can reason about the remaining claim.

## 3. Score Ideas Before Coding

I now use a six-point test that takes about 20 minutes and prevents most false starts. The categories are intentionally crude so I can compare unrelated ideas.

Here are the six categories:

- data: I have or can create a representative sample
- user: one job title and one workflow are named
- method: the project needs a relevant AI technique
- evidence: success can be measured by people or tests
- story: a one-sentence result can be shown
- maintenance: I can run it again after two months

For my fictional candidate, "internal API assistant", the total was 5 out of 6. Maintenance scored lower because the source PDF changed quarterly. I accepted that cost and added a rebuild command instead of expanding the project.

The scores also reveal trade-offs. A web-scraping agent scored 6 for method and 2 for evidence because a reviewer couldn't easily tell whether one answer was lucky.

## 4. Build the Smallest Honest Path

The first implementation was deliberately boring. I loaded the API guide, split it into sections, embedded those sections, and wrote 12 test questions. The whole pipeline lived in `app/pipeline.py` and took about two hours.

I used a spreadsheet for the first review. Each row contained the question, the answer, the cited page, and a decision. Ten of twelve answers were accepted. One omitted the page number, and one used a similar but incorrect endpoint.

Those failures set the next task. The missing citation became a schema constraint, and the wrong endpoint became a regression question in `tests/questions.jsonl`. Only after those fixes did I add a small web interface.

That order matters because a portfolio project is a claim plus evidence. The claim becomes credible when the evidence is easy to read, and the interface is only packaging.

## 5. Make the Repository Explain the Claim

A reviewer should understand the project in under two minutes, so I put five items at the top of the README:

- a one-sentence user and input description
- an install command and expected Python version
- one command that runs the pipeline
- a link to the sample output directory
- the current acceptance rate and its review date

Then I added a 40-second screen recording that opened the question set, ran three queries, and showed two answers with citations. It was plain, but it removed one step for a busy reader.

I also created `docs/decisions.md`, a short record of the section size, storage choice, and authentication boundary. It explained why sections held 700 tokens, why I used SQLite (a small embedded database), and why accounts were out of scope.

## 6. Review the Claim Before Sharing

Before sharing a project, I run one external review. I ask a peer to spend 15 minutes on the README and one output file, then to describe the project's claim and its evidence.

In the fictional exercise, the first reviewer said the system "answers API questions". That wording was broader than my claim. I changed the title to "citation-first search over one API guide", and the narrower sentence made the 83% acceptance rate meaningful.

I also removed a benchmark table. It compared my small set with a public benchmark on four unrelated documents. The comparison wasn't defensible, and keeping it would have invited a question I couldn't answer.

## Selection Changes

Interesting is a weak selection criterion. A job posting, one user, and a measurable input are stronger. The method gives you a project you can defend after the first question.

I now keep a one-page idea file with scores and rejected options. It turns career anxiety into a backlog, and it makes it easier to stop a project when the evidence doesn't appear.

The next step in my own process is to add refresh instructions to every portfolio repository. I plan to write about that in a future article. Subscribe to stay updated.
