# Turning Workshop Feedback into a Public Recap

I wrote this synthetic style exercise as a build log, and the workshop, people and quotes below are fictional. On 5 March 2026 I ran a free three-hour online workshop about data pipelines for 41 attendees. The feedback form collected 23 responses within two days.

The session went the way my workshops usually go. The public recap was the part I kept getting wrong, because I summarized 23 free-text answers from memory and published whatever sounded representative. This post describes the pipeline that replaced that habit.

In this post, I'll share:

- the five-question form I send after each workshop
- a recap draft that leaked identifying details
- an anonymization step that runs before I read anything
- how I count themes from the answers
- what the public recap and the follow-up note contain
- where the pipeline stands after two runs

## The Survey After Each Workshop

The form has five questions and takes about three minutes. Two questions collect pace and difficulty scores from 1 to 5. Two more collect free text about the best and the least useful part. The last question asks whether I may quote answers in a public recap.

That quote question matters more than any score. In March, 19 of 23 participants answered it with a clear yes, two said no, and two left it blank. I treat blank as a no, which costs me two quotes per run and keeps the trust of the people who prefer to stay out. The form lives in the same tool as the registration page, so the export takes one click. The response rate came out at 56 percent in March.

## The Draft That Leaked Details

The first recap went out on 12 March and stayed up for about two hours. One quoted answer began with "in our fraud team we always", and a participant wrote minutes later that the phrase identified her employer. I replaced the quote with a paraphrase and apologized the same morning.

Nobody else wrote in, and the recap had 40 views at that point. Still, the episode changed how I handle every answer. My mistake was quoting exact sentences with their surrounding context attached. The rule I took from it: anonymize every response before it reaches any draft.

## Anonymizing Before Reading

In April I automated that step with `anonymize-recap`, a 40-line Python script that runs before I open anything.

The feedback form exports answers as a CSV file, and the script replaces emails, employer names, and product vendor names with participant codes:

```bash
python anonymize_recap.py feedback-2026-03.csv > responses-anon.csv
```

The script reads a list of known names from `names.txt` in the same folder, and it also catches sequences that look like email addresses. When I re-ran it on the March export as a test, it found 5 email addresses and 9 employer names. I had read all 14 with my own eyes and missed every one.

Three lines from the anonymized March file look like this:

```text
P04: the section on retries finally made sense
P11: more live coding, fewer slides
P19: the pace got too fast in the second hour
```

Codes preserve the wording while removing the origin, and the mapping file never leaves my laptop.

## Counting Themes From 23 Answers

Reading 23 short answers takes about 15 minutes, so I count themes by hand instead of automating the step.

Each answer gets one label from a fixed set of four:

- content, for anything about the material
- pace, for speed and difficulty comments
- recordings, for requests about replays and slides
- other, for everything I can't classify

The March counts came out as 12 content answers, 7 recording requests, and 4 others, with the last two answers containing only scores. The counts decide the recap structure. A theme with 12 mentions earns a paragraph, a theme with 5 earns a sentence, and single mentions wait for the next run. The labels have stayed stable across both runs, and anything that resists a label twice becomes an agenda item for the next session.

## The Recap And The Follow-Up Note

The recap post has kept one structure since April. It opens with the attendance numbers, gives one paragraph per theme, and closes with dated changes I committed to. Each theme paragraph quotes at most two coded answers, always from participants who consented to public quotes. The scored questions go in as plain sentences, for example an average pace score of 4.1 out of 5 from 21 answers.

That 4.1 reads better than it deserves. The two lowest scores came from the same fast second hour that P19 described, and the recap says so in the same paragraph.

A follow-up email goes to all 64 registered people two days after the recap, with a link and the two changes with dates. The May follow-up brought 9 replies and one unsubscribe, and two recipients asked for the slides from the fast hour.

## The Pipeline After Two Runs

The whole pipeline is one form, one script, and a fixed recap structure, and the May run took about 90 minutes from export to email. In March the same work consumed an afternoon and produced a leaked employer name.

The theme counting happens in my head, and the consent check stays manual before any quote goes public. At 50 or more responses I would want a clustering step, but 23 answers don't justify building one yet.

I'll write about the workshop material in a future post. If you want to follow along, don't forget to subscribe.
