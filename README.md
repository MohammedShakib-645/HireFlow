# HireFlow

---

## 🚀 Live Demo + 🎥 Video Demo

### 🌐 Live Hosted Demo — GitHub Pages

[👉 Open HireFlow Live Demo](https://mohammedshakib-645.github.io/HireFlow/)

### 🎥 Latest Video Demo — Day 2

[▶️ Watch the HireFlow Day 2 Demo](https://drive.google.com/file/d/10nynm8WP6PoCmGmvHoKyvZ1PM7AobP5O/view?usp=sharing)

---

### AI-Powered Recruitment Intelligence Agent

> **Smarter Hiring. Better Decisions.**  
> **Not just resumes. Real evidence.**

HireFlow is a recruitment intelligence MVP built around an **evidence-first, agentic workflow**. It is designed to help recruiters analyze job requirements, candidate resumes, evidence gaps and interview responses in one traceable workflow.

The core principle is simple:

**AI analyzes the evidence. The human makes the final decision.**

---

## What HireFlow Actually Does

HireFlow takes a job description and a pool of candidate resumes, extracts relevant information, maps candidate evidence against job requirements, identifies gaps, prepares targeted interview questions and produces recruiter-facing insights.

### Current end-to-end concept

```
Job Description
      ↓
JD Requirement Extraction
      ↓
Candidate Resume Analysis
      ↓
Requirement ↔ Evidence Mapping
      ↓
Evidence / Gap Detection
      ↓
Targeted Interview Questions
      ↓
Interview Evidence Update
      ↓
Candidate / Cohort Insights
      ↓
Recruiter Report
      ↓
Human Decision
```

The repository contains both a working lightweight Streamlit MVP and a more structured FastAPI backend foundation for the agentic architecture.

---

# The Problem

Recruitment information is fragmented.

A recruiter may need to compare:

- Job requirements
- Candidate skills
- Work experience
- Projects
- Technical claims
- Interview responses
- Missing or unclear evidence

A resume keyword match alone cannot explain whether a candidate actually demonstrated the required capability.

This creates a practical problem:

> **More candidates. More data. Less clarity.**

HireFlow is designed to turn that scattered information into a structured evidence trail.

---

# The HireFlow Approach

Instead of producing only a generic candidate score, HireFlow focuses on:

### 1. Requirements

Understand what the role actually requires.

### 2. Candidate Profile

Extract skills, experience, projects and other relevant facts from candidate documents.

### 3. Evidence Mapping

Connect each requirement to supporting candidate evidence.

### 4. Gap Detection

Identify requirements that are missing, weakly supported or need validation.

### 5. Targeted Interview

Generate questions around candidate claims and evidence gaps.

### 6. Evidence Update

Use interview outcomes to update the evidence state.

### 7. Recruiter Report

Present coverage, verified evidence, gaps and interview information without replacing the recruiter's judgment.

---

# Agentic Architecture

The backend currently defines **7 separable agent stages**:

| Stage | Agent | Responsibility |
|---|---|---|
| 1 | JD Analyzer | Extract structured requirements |
| 2 | Resume Analyzer | Build a candidate profile and facts |
| 3 | Evidence Mapper | Map requirements to candidate evidence |
| 4 | Question Agent | Generate targeted validation questions |
| 5 | Evidence Updater | Update evidence after interview outcomes |
| 6 | Grouper | Organize candidate/cohort information |
| 7 | Reporter | Produce an evidence-based report |

### Agent Flow

```
                ┌─────────────────────┐
                │   Job Description   │
                └──────────┬──────────┘
                           ↓
                 ┌──────────────────┐
                 │   JD Analyzer    │
                 └────────┬─────────┘
                          ↓
       ┌──────────────────────────────────┐
       │        Candidate Resumes          │
       └────────────────┬─────────────────┘
                        ↓
                ┌──────────────────┐
                │ Resume Analyzer  │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │ Evidence Mapper  │
                └────────┬─────────┘
                         ↓
                 ┌─────────────────┐
                 │  Gap Detection  │
                 └────────┬────────┘
                          ↓
                ┌──────────────────┐
                │ Question Agent   │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │ Interview Input  │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │ Evidence Updater │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │ Cohort / Report  │
                └────────┬─────────┘
                         ↓
                ┌──────────────────┐
                │ Human Recruiter  │
                └──────────────────┘
```

---

# Evidence-First Intelligence

HireFlow does not treat every resume statement as equally reliable.

Evidence can move through different states:

| Status | Meaning |
|---|---|
| **Verified** | Evidence is sufficiently supported |
| **Needs Validation** | A claim exists but requires further checking |
| **Missing** | No direct supporting evidence was found |

The backend also records:

- Source
- Source reference
- Confidence
- Evidence score
- Evidence status
- Evidence history
- Agent responsible for the update

This creates a foundation for traceable recruitment intelligence rather than an unexplained black-box result.

---

# Interview Intelligence

The interview layer is designed around **evidence gaps**, not generic interview templates.

For example:

**Requirement:** FastAPI  
**Candidate evidence:** Mentioned in resume  
**Detected issue:** Depth is unclear

HireFlow can generate a validation question such as:

> Explain what you personally built with FastAPI and how you handled a production problem.

The interview outcome can then update the evidence state.

This creates a loop:

**Resume Claim → Evidence Check → Interview Question → Interview Evidence → Updated Evidence**

---

# Current MVP

The repository currently contains a lightweight Streamlit MVP in `app.py`.

It supports:

- Job description upload
- PDF / text document reading
- Resume upload
- Multiple candidate processing
- Skill extraction
- Experience extraction
- Requirement matching
- Candidate summaries
- Gap identification
- Interview question generation
- Optional live LLM generation
- Natural-language candidate search
- Recruiter-style evaluation report
- Downloadable Markdown report

### MVP input flow

```
Upload JD
   +
Upload Resumes
   ↓
Requirement Extraction
   ↓
Candidate Analysis
   ↓
Matching + Gaps
   ↓
Interview Kit
   ↓
Ask / Report
```

The MVP also includes sample recruitment data under `sample_data/` so the workflow can be demonstrated without preparing documents first.

---

# Structured Backend

The `backend/` directory contains the FastAPI-based architecture for expanding the MVP into a structured multi-agent application.

### Backend components include

- FastAPI application
- SQLAlchemy models
- Authentication utilities
- Organization and user models
- Job and requirement models
- Candidate and candidate-fact models
- Evidence and evidence-history models
- Interview question / response models
- Recruiter report model
- Audit log model
- LLM provider abstraction
- Mock LLM provider
- Anthropic provider
- Document-processing dependencies
- Redis / Celery infrastructure dependencies
- Docker configuration

---

# Data Model

The backend models the recruitment process around connected entities:

```
Organization
     │
     ├── Users
     │
     └── Jobs
           │
           ├── Requirements
           │
           └── Candidates
                  │
                  ├── Candidate Facts
                  │
                  ├── Evidence
                  │      ↓
                  │   Evidence History
                  │
                  └── Interview
                         ├── Questions
                         └── Responses

Candidate + Job + Evidence
            ↓
          Report
```

This structure allows recruitment insights to remain connected to their underlying evidence.

---

# LLM Layer

The project separates LLM access from the agent logic.

The repository includes an `LLMProvider` abstraction with support for provider-based generation and a mock implementation for development.

The lightweight MVP can use:

- Gemini API
- OpenAI API

The structured backend includes provider abstractions for:

- OpenAI
- Anthropic
- Mock / development mode

The application is therefore designed so the intelligence layer can evolve without rewriting the entire recruitment workflow.

---

# Technology Stack

## Current MVP

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Language | Python |
| Data processing | Python / Pandas |
| PDF parsing | pypdf |
| AI | Gemini / OpenAI optional |
| Reports | Markdown |

## Structured Backend

| Layer | Technology |
|---|---|
| API | FastAPI |
| ORM | SQLAlchemy |
| Development DB | SQLite-compatible setup |
| Production direction | PostgreSQL + pgvector |
| Cache / Queue | Redis + Celery |
| Documents | pypdf / pdfplumber / python-docx |
| AI providers | OpenAI / Anthropic / Mock |
| Authentication | JWT |
| Containers | Docker Compose |

---

# Repository Structure

```
HireFlow/
│
├── index.html
├── app.py
├── run_all.bat
├── requirements.txt
├── docker-compose.yml
│
├── backend/
│   ├── app/
│   │   ├── agents.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   │
│   │   ├── core/
│   │   ├── llm/
│   │   ├── models/
│   │   ├── parsers/
│   │   └── schemas/
│   │
│   ├── requirements.txt
│   └── storage/
│
├── sample_data/
│   ├── job_description.txt
│   ├── resume_01_aarav.txt
│   ├── resume_02_sneha.txt
│   ├── resume_03_rahul.txt
│   └── resume_04_ishita.txt
│
├── docs/
│   ├── PROBLEM_STATEMENT.md
│   ├── SOLUTION.md
│   ├── ARCHITECTURE.md
│   └── DAY_1_PROGRESS.md
│
└── linkedin_day1.png
```

---

# Sample Evaluation Scenario

The repository includes a sample **Senior Backend Engineer (Python)** job description.

The sample requirements include areas such as:

- Python
- FastAPI / Django
- REST APIs
- PostgreSQL / SQL
- Docker
- Git / CI/CD
- LLM / AI API integration
- System design

Four sample candidate profiles are included to exercise different evidence and gap patterns.

This makes the repository useful for demonstrating:

**Requirement → Candidate Evidence → Gap → Interview Validation**

rather than only showing a static UI.

---

# Human-in-the-Loop

HireFlow is explicitly designed as a **decision-support system**.

It does not claim that the AI should autonomously hire or reject candidates.

```
AI analyzes evidence
        ↓
AI identifies gaps
        ↓
AI prepares questions
        ↓
AI organizes insights
        ↓
      HUMAN
        ↓
Final recruitment decision
```

> **AI supports the decision. The human decides.**

---

# Day 1 — AI Agent Hackathon 2026

### Completed

- [x] Recruitment problem analyzed
- [x] Solution direction defined
- [x] Agentic workflow designed
- [x] Seven backend agent stages defined
- [x] Evidence-first model designed
- [x] Interview intelligence flow defined
- [x] Human-in-the-loop principle defined
- [x] MVP workflow implemented
- [x] Structured backend foundation created
- [x] Sample JD and candidate data added
- [x] Architecture documentation added

### Next Engineering Phase

- Connect the structured backend flow end-to-end
- Strengthen document parsing
- Improve evidence extraction and source spans
- Connect interview responses to persistent evidence updates
- Complete provider integrations
- Add robust semantic / vector search
- Expand recruiter dashboard workflows
- Add automated tests and deployment validation

---

# Project Status

**Project:** HireFlow  
**Category:** AI Recruitment Intelligence  
**Event:** AI Agent Hackathon 2026  
**Current Phase:** Day 1 → MVP / Architecture Foundation

---

## Core Vision

> **Build a trusted AI recruitment intelligence partner that makes candidate evidence easier to understand, gaps easier to investigate, interviews more targeted, and recruiter decisions better informed — without removing the human from the decision.**

---

## License

This project is being developed as a hackathon project.
