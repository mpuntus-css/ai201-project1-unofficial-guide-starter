# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

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
| 1 | Rate My Professors – Professor A | Review text file for Sinan Kanbir | ./documents/professor_a_reviews.txt |
| 2 | Rate My Professors – Professor B | Review text file for Saemyi Park | ./documents/professor_b_reviews.txt |
| 3 | Rate My Professors – Professor C | Review text file for Cortney Chaffin | ./documents/professor_c_reviews.txt |
| 4 | Rate My Professors – Professor D | Review text file for Elena Novak | ./documents/professor_d_reviews.txt |
| 5 | Rate My Professors – Professor E | Review text file for Marcus Lee | ./documents/professor_e_reviews.txt |
| 6 | Rate My Professors – Professor F | Review text file for Nadia Ortiz | ./documents/professor_f_reviews.txt |
| 7 | Rate My Professors – Professor G | Review text file for Tanya Brooks | ./documents/professor_g_reviews.txt |
| 8 | Rate My Professors – Professor H | Review text file for Priya Shah | ./documents/professor_h_reviews.txt |
| 9 | Rate My Professors – Professor I | Review text file for Dylan Reed | ./documents/professor_i_reviews.txt |
| 10 | Rate My Professors – Professor J | Review text file for Olivia Bennett | ./documents/professor_j_reviews.txt |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 200 characters

**Overlap:** 50 characters

**Why these choices fit your documents:**

I used 200-character chunks because the corpus is made up of short professor and course review snippets rather than long articles. Smaller chunks keep each embedding focused on a single opinion or experience, which improves retrieval precision for review-style questions.

The 50-character overlap preserves context when a review sentence spills across a chunk boundary. That matters for this corpus because reviews often combine a professor's teaching style, workload, and grading behavior in only a few sentences.

**Final chunk count:** 220

Before chunking, I removed HTML tags, decoded HTML entities, and collapsed repeated whitespace. I also filtered out empty chunks so the vector store would only contain usable review text.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

all-MiniLM-L6-v2 via SentenceTransformer

**Production tradeoff reflection:**

I chose all-MiniLM-L6-v2 because it is small, fast, and works well for short review text. It runs locally with no API key, which makes it practical for iterative debugging and classroom-scale evaluation.

If cost were not a constraint in production, I would compare larger embedding models with better semantic understanding and longer context windows. The main tradeoffs would be retrieval accuracy versus latency, storage cost, and whether the model handles subtle domain language better than the lightweight default.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The system prompt tells the model to answer only from the retrieved context, not from outside knowledge, and to return exactly "I don't have enough information on that." when the context is insufficient. The user prompt repeats the same rule and passes the retrieved chunks as explicit context.

I also keep source attribution out of the model's control. The app builds the source list programmatically from the retrieved chunk metadata, so the filenames and chunk positions come from Chroma rather than from whatever the model decides to invent.

**How source attribution is surfaced in the response:**

The Gradio UI shows the answer in one field and the retrieved sources in a separate field. Each source line is generated from metadata returned by retrieval and includes the filename, chunk index, and distance score.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about Professor Smith's grading style? | The response should summarize common opinions from reviews, such as whether grading is fair, lenient, or strict, and reference supporting sources. | The system responded that it did not have enough information on that and returned weakly related professor review chunks. | Partially relevant | Accurate |
| 2 | How difficult is the Introduction to Programming course according to students? | The response should summarize student comments about workload, exams, projects, and overall difficulty. | The system mixed unrelated CS review snippets and answered that the course is a 4.0 difficulty with a lot of work, then cited Professor Lee and other unrelated chunks. | Off-target | Inaccurate |
| 3 | Which professors are most frequently recommended for introductory computer science courses? | The response should identify the professors that receive the most positive recommendations in the collected sources and explain why students recommend them. | The system said Marcus Lee is the only CS professor mentioned and summarized his rating and student praise, but it did not really compare multiple professors. | Partially relevant | Partially accurate |
| 4 | What complaints do students most often have about course registration? | The response should summarize recurring issues mentioned in Reddit threads or forums, such as limited seats, waitlists, or scheduling conflicts. | The system said it did not have enough information on that and returned only weakly related professor chunks. | Partially relevant | Accurate |
| 5 | What advice do upperclassmen give to freshmen taking their first CS courses? | The response should summarize common recommendations, such as attending office hours, starting assignments early, and managing course load. | The system said it did not have enough information on that and returned weakly related chunks. | Partially relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

How difficult is the Introduction to Programming course according to students?

**What the system returned:**

The model answered that the course has a difficulty of 4.0 and is a lot of work, then blended in snippets about Professor Lee explaining programming concepts clearly. The answer sounded plausible, but it was stitched together from loosely related chunks rather than from a real Introduction to Programming source.

**Root cause (tied to a specific pipeline stage):**

The failure starts in retrieval. The corpus does not contain a direct Introduction to Programming review, so Chroma returned nearby CS-related chunks with high distance scores around 1.0. Because those chunks still contained words like "programming" and "difficulty," the generator treated them as evidence and composed a confident answer anyway.

**What you would change to fix it:**

I would add actual Introduction to Programming sources or relax the question set so it matches the available documents. If I kept this corpus, I would also add a stricter retrieval filter that refuses to answer when the best distances are too high, so the model cannot turn weak matches into confident summaries.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The spec kept the pipeline focused on small, testable stages. Because the chunking, retrieval, and grounding requirements were spelled out separately, I could validate each stage before moving on and catch weak retrieval results early instead of debugging them after generation was added.

It also helped me choose the output shape for the UI and evaluation report. The planning document made it clear that I needed source attribution, top-k retrieval, and a failure analysis, so I built those into the interface and the README from the start.

**One way your implementation diverged from the spec, and why:**

I started with the planned 800-character chunk size, but I reduced it to 200 characters with 50-character overlap because the review text is short and the larger chunks were merging multiple opinions into one embedding. I also switched the splitter to sentence-aware chunking so chunks read more like complete thoughts instead of mid-sentence fragments.

Another divergence is that the evaluation questions in planning.md cover some topics that are not actually present in the current document set. That mismatch exposed retrieval failures during testing, which is useful diagnostically but means the evaluation report includes several intentional no-answer cases.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*

I gave the AI my planning.md chunking section, the review text files, and the requirement to load plain .txt documents, clean them, and split them into chunks with overlap.
- *What it produced:*

It produced the initial ingestion and chunking script with document loading, cleaning, metadata, and a character-based chunker.
- *What I changed or overrode:*

I replaced the raw character slicing with a sentence-aware splitter and reduced the chunk size from 800 characters to 200 because the original chunks were too large for these short review documents.

**Instance 2**

- *What I gave the AI:*

I gave the AI the Retrieval Approach section and the architecture diagram, along with the requirement to embed chunks with all-MiniLM-L6-v2, store them in ChromaDB, and expose a grounding-first query interface.
- *What it produced:*

It produced the embedding and retrieval module plus the grounded generation/query layer using Groq and a Gradio UI skeleton.
- *What I changed or overrode:*

I made source attribution programmatic instead of trusting the model to cite sources on its own, and I enforced an explicit "I don't have enough information on that." fallback when retrieval is weak or the corpus does not cover the question.
