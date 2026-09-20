# System Architecture

## High-Level Architecture

```
┌───────────────────────────────┐
│        Recruiter UI           │
│     Next.js + TypeScript      │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Agentic Orchestrator     │
│          FastAPI              │
└───────────────┬───────────────┘
                │
      ┌─────────┼─────────┐
      ▼         ▼         ▼
   JD Agent  Resume     Interview
             Agent        Agent
      │         │         │
      └─────────┼─────────┘
                ▼
┌───────────────────────────────┐
│        Evidence Engine        │
│ Requirement → Evidence → Gap  │
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│         Evidence Store        │
│            SQLite             │
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│       Recruiter Dashboard     │
│ Reports • Search • Insights   │
└───────────────────────────────┘
```

## Technology Stack

### Frontend

- Next.js
- TypeScript
- Tailwind CSS

### Backend

- Python
- FastAPI

### Data

- SQLite
- SQLite FTS5
- Optional vector search

### Document Processing

- PyMuPDF
- python-docx

### AI Layer

- LLM API
- Ollama-compatible local models where appropriate

## Agent Responsibilities

| Agent | Responsibility |
|---|---|
| JD Analyzer | Extract structured job requirements |
| Resume Analyzer | Extract candidate information |
| Evidence Mapper | Connect requirements to evidence |
| Gap Detector | Identify missing or weak evidence |
| Interview Agent | Generate adaptive questions |
| Interview Analyzer | Analyze interview responses |
| Evaluation Agent | Produce structured evidence insights |
| Recruiter Report Agent | Generate traceable recruiter reports |

## Evidence Model

Each important candidate claim should be represented with:

- Requirement
- Evidence
- Source
- Evidence status
- Confidence/uncertainty
- Supporting context

## Evidence States

**VERIFIED**  
Available evidence supports the claim.

**PARTIAL EVIDENCE**  
Some supporting evidence exists, but additional information may be useful.

**NEEDS VALIDATION**  
The claim requires additional verification.

## Data Flow

```
Job Description
      ↓
Requirement Extraction
      ↓
Candidate Documents
      ↓
Candidate Evidence Extraction
      ↓
Requirement ↔ Evidence Mapping
      ↓
Gap Detection
      ↓
Adaptive Interview
      ↓
Interview Evidence
      ↓
Evaluation
      ↓
Recruiter Report
      ↓
Human Decision
```

## Architecture Principle

The system is designed around **traceability**.

Every important insight should be connected to the evidence that produced it whenever possible.
