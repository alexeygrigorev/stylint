# Building Search with SQLite



The useful part of this example is the workflow. I will walk through the problem, the decisions, and the limits so the idea stays connected to what actually happened. 

Recently, I was looking for a compact Python search library that provides reliable search functionality

without requiring a full-scale infrastructure. https://github.com/alexeygrigorev/minsearch/, which met

the first two requirements but stored everything in memory and lacked persistence. After reviewing the

available options, I realized no solution fully matched my requirements.

https://github.com/alexeygrigorev/sqlitesearch, a lightweight, pure-Python search library that supports

both text and vector search. It stores all data in a single file using SQLite, an open-source relational

database included with the Python standard library. In this post, I’ll explain the building process, how

I came up with the final configuration of the system and evaluated existing solutions with ChatGPT, why

they were insufficient, how SQLiteSearch is structured internally, its benefits, and what my workflow

looked like for publishing it as a PyPI package. Background The concept for the SQLiteSearch library

emerged from the need for a persistent, lightweight search library that AI Engineering Buildcamp course

participants can use in one of their projects. https://github.com/alexeygrigorev/minsearch that supports

text and vector search with an easy-to-use API. But, it only works in memory. The result means that when

I close the Python process running it, all the indexed data disappears. I have to rebuild the index each

time I restart the application. The result works in some cases, but I wanted to show how to build a data

ingestion pipeline that operates independently of the RAG agent. So I needed a lightweight and

persistent search engine. My Requirements I wanted a search library that meets these criteria: Available

in Python Easy to set up and interact with allowing use in environments like Google Colab Support both

regular text search and vector search Existing solutions, such as running Elasticsearch, are not always

a good fit for small-scale problems. They cost $200+ per month and are designed for large-scale

production systems. There are cheaper options like Qdrant or PostgreSQL, but if I were to use them, I’d

need to rely on an external service or run them in Docker. So I decided to do my own research with

ChatGPT. In cases like that, when I want to find something but it’s not yet very clear in my head

exactly what I need, and I’m not sure whether a solution to my problem already exists, I turn to ChatGPT

to brainstorm ideas and interact with it in dictation mode. Research Phase I shared my requirements with

ChatGPT and asked it to find a solution. Eventually, it suggested using SQLite’s text search. I like

SQLite since it’s embedded in Python and satisfies most of my requirements. But I also wanted to have

vector search, which it didn’t support out of the box. So I started looking for vector search options

that work with SQLite. Here’s what ChatGPT found: ChatGPT research results showing existing libraries

Results were: lshashing: Pure Python LSH library, but keeps hash tables in memory, not SQLite Redis,

LevelDB, BerkeleyDB but not SQLite narrow-down: Supports SQLite backend but uses a native Rust

extension, not pure Python None of the existing solutions met all requirements, so I decided to create a

new library. Implementation I continued my conversation with ChatGPT to brainstorm solutions and iterate

on



That is the part I would keep from this example: connect each tool to the problem that made it necessary, and keep the limitation next to the claim. The details matter because they explain what can be reused and what was specific to this project.
