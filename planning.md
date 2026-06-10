# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

Student reviews of professors and courses at the University of Wisconsin–Stevens Point

This domain covers student experiences with professors and courses, including teaching style, workload, exam difficulty, grading practices, and class expectations. This knowledge is valuable because official course catalogs and faculty webpages provide only formal descriptions and often do not reflect what students actually experience in the classroom. Students typically need to search multiple websites and discussion forums to find this information.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
#	Source	Type	URL or file path
1	Rate My Professors – Professor A	Review Page	https://www.ratemyprofessors.com

2	Rate My Professors – Professor B	Review Page	https://www.ratemyprofessors.com

3	Rate My Professors – Professor C	Review Page	https://www.ratemyprofessors.com

4	Reddit discussion about course registration	Reddit Thread	https://www.reddit.com

5	Reddit discussion about easiest electives	Reddit Thread	https://www.reddit.com

6	Reddit discussion about difficult CS courses	Reddit Thread	https://www.reddit.com

7	Student Discord FAQ screenshots	Community Resource	./documents/discord_faq.pdf
8	Student club advice page	Website	https://www.uwsp.edu

9	Unofficial student course guide	PDF	./documents/course_guide.pdf
10	Student forum discussion about professors	Forum Thread	https://example-forum.com/thread

11	Reddit thread on best professors for freshmen	Reddit Thread	https://www.reddit.com

12	Student blog about course experiences	Blog Post	https://example-blog.com

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 200 characters

**Overlap:** 50 characters

**Reasoning:**


I will split documents into chunks of approximately 200 characters with an overlap of 50 characters between consecutive chunks. Most of my sources consist of short student review passages that work better when chunked at a smaller granularity, so a 200-character chunk keeps each piece tightly focused on a single opinion or experience.

The 50-character overlap helps preserve context when important information appears near the boundary between two chunks. Without overlap, a review sentence could be split awkwardly and lose the connection between a professor's teaching style, workload, or grading comments.

If the chunks were too small, the retrieval system might return fragments that lack enough context to answer a question accurately. If the chunks were too large, multiple topics could be combined into a single embedding, reducing retrieval precision. The chosen chunk size and overlap provide a balance between preserving context and maintaining focused semantic search results.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via the Sentence-Transformers library

**Top-k:** 5

**Production tradeoff reflection:**


I will use the all-MiniLM-L6-v2 embedding model because it is lightweight, fast, and performs well for semantic search on short text such as student reviews, forum posts, and Reddit discussions. The model converts both documents and user queries into vector representations, allowing the system to find relevant information even when the query does not contain the exact same words as the source documents.

For each query, I will retrieve the top 5 most relevant chunks. Retrieving too few chunks could cause important information to be missed, while retrieving too many chunks could introduce irrelevant information and make it more difficult for the language model to generate a focused response. A top-k value of 5 provides a balance between coverage and precision.

If I were deploying this system for real users and cost was not a constraint, I would consider using a larger and more powerful embedding model that provides better semantic understanding and retrieval accuracy. I would evaluate tradeoffs such as context length, multilingual support, and performance on domain-specific student review data. Larger models can improve retrieval quality and handle more nuanced queries, but they require more computation, storage, and response time. The choice would depend on whether retrieval accuracy or system speed is the higher priority.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
1. What do students say about Professor Smith's grading style?	
The response should summarize common opinions from reviews, such as whether grading is fair, lenient, or strict, and reference supporting sources.
2. How difficult is the Introduction to Programming course according to students?	
The response should summarize student comments about workload, exams, projects, and overall difficulty.
3. Which professors are most frequently recommended for introductory computer science courses?	
The response should identify the professors that receive the most positive recommendations in the collected sources and explain why students recommend them.
4. What complaints do students most often have about course registration?	
The response should summarize recurring issues mentioned in Reddit threads or forums, such as limited seats, waitlists, or scheduling conflicts.
5. What advice do upperclassmen give to freshmen taking their first CS courses?	
The response should summarize common recommendations, such as attending office hours, starting assignments early, and managing course load.

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Noisy or inconsistent reviews. Student reviews are highly subjective, and different students may have very different opinions about the same professor or course. This could make it difficult for the system to provide a clear answer when retrieved documents contain conflicting information.
2. Off-topic retrieval and chunking issues. Some Reddit threads and forum discussions may contain unrelated comments that are not relevant to the user's question. In addition, important information may be split across chunk boundaries, causing the retrieval system to miss context or return incomplete answers. Using chunk overlap can help reduce this problem, but it may still occur in some cases.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

Architecture
------------------------
| Document Ingestion   |
| requests, BS4, PDFs  |
------------------------
           |
           v
------------------------
| Chunking             |
| 800-char chunks      |
| 150-char overlap     |
------------------------
           |
           v
------------------------
| Embedding +          |
| Vector Store         |
| all-MiniLM-L6-v2     |
| ChromaDB             |
------------------------
           |
           v
------------------------
| Retrieval            |
| Semantic Search      |
| Top-k = 5            |
------------------------
           |
           v
------------------------
| Generation           |
| LLM (ChatGPT)        |
| Answer + Sources     |
------------------------

Pipeline Flow:

Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation

Document Ingestion: Collect reviews, Reddit discussions, forum posts, and other sources.
Chunking: Split documents into approximately 800-character chunks with 150-character overlap.
Embedding + Vector Store: Generate embeddings using all-MiniLM-L6-v2 and store them in ChromaDB.
Retrieval: Convert the user's question into an embedding and retrieve the top 5 most relevant chunks.
Generation: Use an LLM to generate a response based on the retrieved chunks and provide source-based answers.

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->


1. Document Ingestion
AI Tool: ChatGPT
Input: Domain description, document source list, and project requirements.
Expected Output: Python code that loads documents from URLs and local files while preserving metadata such as source names and URLs.
Verification: Test the code on several documents and confirm that all text and metadata are correctly extracted and stored.
2. Chunking
AI Tool: ChatGPT
Input: Chunking Strategy section specifying 800-character chunks with 150-character overlap.
Expected Output: A Python chunk_text() function that splits documents according to the specified chunk size and overlap.
Verification: Run the function on sample documents and verify that chunk sizes are correct and overlapping text appears in adjacent chunks.
3. Embedding and Vector Store
AI Tool: GitHub Copilot
Input: Retrieval Approach section specifying the use of the all-MiniLM-L6-v2 model and ChromaDB.
Expected Output: Code that generates embeddings for each chunk and stores them in a vector database with metadata.
Verification: Confirm that every chunk has an embedding and that embeddings can be successfully stored and retrieved from the database.
4. Retrieval
AI Tool: ChatGPT
Input: Retrieval requirements, embedding model information, and top-k value of 5.
Expected Output: A retrieval function that converts a user query into an embedding and returns the five most relevant chunks.
Verification: Test the function using the evaluation questions and confirm that the returned chunks are relevant to the query.
5. Response Generation
AI Tool: ChatGPT
Input: Retrieved chunks and the Evaluation Plan questions.
Expected Output: A response-generation prompt and code that uses retrieved information to answer user questions.
Verification: Compare generated answers against the source documents to ensure the answers are accurate and supported by the retrieved evidence.
6. System Testing
AI Tool: ChatGPT
Input: Evaluation Plan and expected answers.
Expected Output: A simple testing script that runs the five evaluation questions and records the system's responses.
Verification: Compare the generated answers with the expected answers and evaluate whether the retrieved sources support the responses.

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
