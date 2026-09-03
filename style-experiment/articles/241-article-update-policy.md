# Deciding When to Update an Old Article

I wrote this synthetic style exercise as an analysis piece. The blog, dates and traffic numbers are fictional. In March 2026 I opened the stats for my 62-post blog and found that 9 posts took about 70% of all views.

Several of those posts were written in 2024 and described library versions that no longer exist. I counted 27 posts older than 18 months, and 11 of them mentioned at least one tool version. I spent one weekend deciding which posts to refresh and which to leave alone. Then I wrote the decision rules down, so I wouldn't re-argue the same choice every month.

In this post, I'll share:

- what the traffic numbers said about the 62 posts
- why correctness forces updates regardless of traffic
- how an effort budget keeps refreshes small
- what goes into the changelog line
- which limits the policy hit in one quarter
- how the policy works in daily practice

## 1. Traffic Decides Most Cases

The blog uses Plausible, a privacy-friendly analytics service, and I export the per-page numbers once a quarter with a small Python script. The median post got 12 views in the last quarter of 2025. The top post, a piece about FastAPI dependency injection, got 340 views per month, and it was 20 months old.

That gap drove the first rule: any post above 100 views per month goes on the refresh list. Nine posts qualified in March 2026, and eight of them were older than a year. Traffic favors posts that already rank well, so it can't be the only input.

The export has its own caveat, and I state it here the way I state it in the data posts. My blog is small, and the sample comes from one analytics tool with ad-blocker visitors undercounted. Real traffic is probably 10 to 20% higher across the board, which moves no post across the 100-view line.

## 2. Correctness Decides the Rest

A post can be invisible and still wrong, and wrong posts damage a blog quietly. One post from 2024 recommended uvicorn startup flags that changed in late 2025. Two readers tried the old flags, and one sent me a short, polite note with the error message.

That note produced the second rule: a post with a factual error gets fixed, or it gets a dated warning at the top. The fix comes first, and traffic plays no role in that decision. Since March I have added two warning banners and fixed four factual errors across the 62 posts.

Version drift caused three of the four fixes. The fourth was a code sample that no longer ran, because a library had moved a function to another module. No reader had reported that one in eight months.

## 3. Effort Sets the Budget

Refresh work expands to fill a free afternoon, so I capped it. A refresh gets about 60 to 90 minutes, and the timer starts after I reread the post. If a fix needs more time, I write a new post and link the two in both directions.

The budget killed two planned refreshes in March. One post about dataset scraping needed a new methodology section, so it moved to the idea list as a fresh post. The other was a rewrite of a piece about cron, and the diff had already reached 400 changed words when I stopped.

Ninety minutes covers more than I expected. A typical refresh replaces two or three version numbers, reruns the code samples, and adds a paragraph about what changed since publication. That fits the budget in about six of ten cases, and the rest become new posts.

## 4. A Changelog Keeps the Record

Every updated post gets a dated line at the bottom, in plain text and in the git history. A line from March reads: "2026-03-14: replaced the uvicorn flags, added a note about worker counts". A second line from April marks a post with a banner: "2026-04-02: added a warning about the deprecated API, rewrite planned".

The line settles disputes with myself about what changed and when. It also shows readers that the post has maintenance behind it. Nine updated posts hold 14 changelog lines so far, and no line ran longer than one sentence.

## 5. Limits of the Policy

Traffic numbers lag by weeks, so a post can sit wrong for months before the views return and expose it. Small numbers are also noisy, and a move from 12 to 15 views per month means nothing. My quarterly export smooths some of that noise, and it can't remove it.

The policy also says nothing about merging two overlapping posts. Two of my posts cover nearly the same FastAPI topic from 2024, and the traffic split between them hides both. Merging has no rule yet, so I handle those cases by hand for now.

Tone is the third blind spot, and it resists measurement. A post can be accurate, current and poorly written, and none of my three rules notices. I reread the nine refreshed posts during the March pass, and two of them needed rewording that no rule had asked for.

## The Policy in Practice

The pass sorted 62 posts into 9 refreshes, 2 warning banners, and 51 untouched posts. The sorting took one weekend, and the editing took about 4 hours spread over two weeks. The refreshed posts kept their URLs, so nothing moved in the search index.

What still doesn't work is the merge decision, and the policy stays silent on tone. The quarterly rerun in June will tell me whether the refreshes hold their traffic. I'll write about the merge cases in a future post. If you want to follow along, don't forget to subscribe.
