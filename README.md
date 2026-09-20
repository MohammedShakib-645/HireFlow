# HireFlow

## AI-Powered Recruitment Intelligence Agent

> **Smarter Hiring. Better Decisions.**  
> **Not just resumes. Real evidence.**

HireFlow is an AI-powered recruitment intelligence system designed to help recruiters move from resume-heavy screening toward evidence-based candidate evaluation.

Instead of treating a resume as the complete story, HireFlow connects:

**Job Requirements → Candidate Evidence → AI Analysis → Interview Intelligence → Recruiter Insights → Human Decision**

> **AI supports the decision. The human decides.**

## Problem

Recruiters often need to process large amounts of candidate information across job descriptions, resumes, projects, interviews, and notes. This creates several challenges:

- Time-consuming manual screening
- Scattered candidate information
- Difficult requirement-to-candidate matching
- Interview preparation takes time
- Important evidence can be missed
- Recruiters need clearer, traceable evidence

## Proposed Solution

HireFlow creates an agentic recruitment workflow that:

1. Extracts structured requirements from a job description.
2. Analyzes candidate resumes and documents.
3. Maps requirements to candidate evidence.
4. Detects missing, weak, or unclear evidence.
5. Generates adaptive interview questions.
6. Captures interview responses and notes.
7. Analyzes interview evidence and gaps.
8. Produces a traceable recruiter report.
9. Keeps the recruiter in control of the final decision.

## Core Intelligence

- JD Requirement Extraction
- Resume Intelligence
- Evidence-Based Analysis
- Requirement Mapping
- Gap Detection
- Adaptive Interview
- Interview Analysis
- Candidate Comparison
- Evidence Graph
- Natural Language Recruiter Search

## Evidence-First Principle

HireFlow distinguishes between evidence states instead of presenting every candidate claim as fact:

- **VERIFIED** — supported by available candidate evidence
- **PARTIAL EVIDENCE** — some supporting information exists
- **NEEDS VALIDATION** — a claim requires further verification

## Agentic Workflow

`01 Upload Job Description`  
→ `02 JD Analyzer Agent`  
→ `03 Upload Resumes`  
→ `04 Resume Analyzer`  
→ `05 Evidence Mapping`  
→ `06 Gap Detection`  
→ `07 AI Interview Agent`  
→ `08 Response Capture`  
→ `09 Interview Analysis`  
→ `10 Evaluation Agent`  
→ `11 Recruiter Report`  
→ **Human Recruiter Makes the Final Decision**

## Technology Direction

| Layer | Technology |
|---|---|
| Frontend | Next.js + TypeScript + Tailwind |
| Backend | Python + FastAPI |
| Database | SQLite |
| Documents | PyMuPDF + python-docx |
| AI | LLM API / Ollama |
| Search | SQLite FTS5 / Optional Vector Search |

### Architecture

**Agentic Orchestrator**  
↓  
**Specialized AI Agents**  
↓  
**Evidence Store**  
↓  
**Recruiter Dashboard**

## Day 1 Progress

- [x] Problem understood
- [x] Recruitment workflow analyzed
- [x] Solution architecture designed
- [x] Agentic workflow defined
- [x] Core features identified
- [x] Evidence-first approach designed
- [x] Interview intelligence planned
- [x] Human-in-the-loop workflow defined
- [x] MVP roadmap prepared

### Day 1 Complete

**Next:** Build the core agent, data pipeline and working MVP.

## Documentation

- [Problem Statement](docs/PROBLEM_STATEMENT.md)
- [Solution Overview](docs/SOLUTION.md)
- [System Architecture](docs/ARCHITECTURE.md)
- [Day 1 Progress](docs/DAY_1_PROGRESS.md)

## Project Status

**Phase:** Day 1 — Product and Architecture Definition  
**Project:** HireFlow  
**Track:** AI Agent Hackathon 2026

## Principle

> Recruitment intelligence should make evidence clearer, not replace human judgment.
