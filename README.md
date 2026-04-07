# Pharma Compliance RAG Assistant (V1)

A retrieval-augmented generation (RAG) system that answers compliance and regulatory questions from pharmaceutical documents using grounded evidence and citations.

---

## Overview

This project implements a simple but complete RAG pipeline for the pharma/compliance domain.

Given a user question, the system:
1. retrieves relevant sections from regulatory documents  
2. generates an answer using only retrieved context  
3. cites sources (document + page)  
4. abstains when the answer is not supported  

The focus of this project is **correctness, grounding, and explainability**, not complexity.

---

## Motivation

In regulated environments like pharmaceuticals, correctness and traceability are critical.

Traditional LLMs:
- may hallucinate  
- cannot cite specific internal policies  
- are not grounded in authoritative documents  

This system demonstrates how to:
> **constrain LLMs to trusted sources and enforce evidence-based answers**

---

## Architecture

PDF Documents
    ↓
Parsing + Chunking
    ↓
Local Embeddings (nomic-embed-text)
    ↓
Vector Similarity Search (cosine similarity)
    ↓
Top-K Relevant Chunks
    ↓
LLM (API) Answer Generation
    ↓
Grounded Answer + Citations / Abstention

---

## Tech Stack

- Python  
- Local embeddings via Ollama (`nomic-embed-text`)  
- OpenAI API (generation)  
- NumPy (cosine similarity)  
- Pandas (evaluation)  

---

## Key Features

### 1. Grounded Answer Generation
- Answers are generated **only from retrieved context**
- No external knowledge allowed

### 2. Source Attribution
- Every answer includes citations:

### 3. Abstention Behavior
- If the system cannot find sufficient evidence:
"I don't know based on the provided documents."

### 4. Local Embeddings
- Embeddings are computed locally for:
  - privacy awareness  
  - realistic compliance use case  

### 5. Lightweight Evaluation Pipeline
- Structured JSON outputs:
```json
{
  "retrieved": true,
  "answered": true,
  "answer": "...",
  "citations": [...]
}

Automated evaluation across:
- answerable questions
- weak/dataset-dependent questions
- unanswerable questions

## Evaluation (V1)

### Dataset

- ~8–12 public FDA / GMP / compliance documents  
- ~15–20 evaluation questions  

### Question Types

| Type           | Description                                  |
|----------------|----------------------------------------------|
| Answerable     | Clearly supported by documents               |
| Weak           | Depends on dataset coverage                  |
| Unanswerable   | Requires internal/company knowledge          |

### Results Summary

- Strong performance on answerable regulatory questions  
- Correct abstention on most unanswerable questions  
- Mixed results on dataset-dependent (“weak”) questions  

---

## Key Findings (V1)

### 1. Chunking Quality is Critical

**Initial failures were caused by:**

- Retrieving headings instead of full content  
- Incomplete context  

**Fix:**

- Normalized chunk sizes (merge small, split large)  

**Result:**

- Significant improvement in answer quality  

---

### 2. Retrieval Threshold Helps but Is Not Sufficient

**Similarity thresholding:**

- Reduces noise  
- Filters weak matches  

**However:**

- Thresholding alone does not prevent hallucinations  

**Observed failure mode:**

- Semantically similar but irrelevant chunks pass threshold  
- LLM attempts to answer anyway  

---

### 3. Dataset Coverage Matters

Some questions (e.g., CAPA) failed because:

- Content was not present in the dataset  

**Correct behavior:**

- Abstain rather than hallucinate  

---

### 4. Two Types of Failure Identified

**A. Retrieval Failure**

- Correct answer exists  
- Not retrieved properly  

**B. Sufficiency Failure**

- Retrieved chunks are related  
- But do not fully answer the question  

---

### 5. Organization-Specific Questions Are High Risk

**Examples:**

- “Who approves SOP changes internally?”  
- “What is the company’s internal deviation policy?”  

**Result:**

- Sometimes incorrectly answered despite retrieval filtering  

**Insight:**

> RAG systems need a notion of **answer sufficiency**, not just similarity  

---

## Limitations (V1)

- No reranking of retrieved chunks  
- No semantic relevance validation beyond similarity  
- No structured evaluation of answer correctness (beyond answered/not answered)  
- Chunking is heuristic (character-based)  
- No UI (CLI-based interaction only)  

---

## Future Improvements

- Add lightweight reranking (cross-encoder or scoring step)  
- Improve chunking with sentence-aware splitting  
- Add answer sufficiency scoring  
- Expand dataset coverage  
- Build simple UI (Streamlit)  

---

## Example

**Question:** What are requirements for electronic signatures?

**Answer:**
> Electronic signatures may replace handwritten signatures if properly controlled and securely linked to records *(Source: Data Integrity and Compliance With Drug CGMP.pdf, Page 12)*
>
> Firms must ensure identity verification and document controls *(Page 13)*

---

## How to Run
```bash
python generation.py
```

For evaluation:
```bash
python evaluate.py
```

---

## Key Takeaway

> A simple, well-designed RAG system with strong grounding and evaluation can outperform more complex architectures that lack discipline.

---

## Author's Note

This is V1, built with a focus on simplicity, correctness, and fast iteration. The goal was not to build the most complex system, but to build a **complete, explainable, and improvable RAG pipeline**.