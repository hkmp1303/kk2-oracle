# KK2 – Engineering Workflow Checklist

## Phase 1 – Understand the Requirements

- [x] Read the assignment completely
- [x] Identify all required endpoints
- [x] Identify required technologies:

  - FastAPI
  - Pandas
  - Pydantic
  - transformers
  - SmolLM
- [x] Identify the required Runnable architecture
- [x] Note the Pass (G) and Higher Pass (VG) requirements
- [x] Decide whether to run SmolLM locally or via the HuggingFace API

---

# Phase 2 – Project Setup

- [x] Create the project structure

```
app/
    chain/
    tests/
```

- [x] Create:

  - [x] `main.py`
  - [x] `config.py`
  - [x] `schemas.py`
  - [x] `data.py`
  - [x] `chain/runnable.py`
  - [x] `chain/steps.py`
  - [x] `chain/pipeline.py`

- [x] Configure `pyproject.toml`

- [x] Install dependencies

- [x] Create `.gitignore`

- [x] Create `.env` (if using API keys)

- [x] Verify the project starts

```
uv sync
uv run uvicorn app.main:app --reload
```

---

# Phase 3 – Design the Application

## Data Flow

Design the complete request flow.

```
Upload CSV
        ↓
Store DataFrame
        ↓
Generate Statistics
        ↓
Receive Question
        ↓
Prompt Builder
        ↓
LLM Runner
        ↓
Response Parser
        ↓
API Response
```

---

## Define Pydantic Models

Before writing logic:

- [x] Upload response model
- [x] Statistics model
- [x] Question request
- [x] AI response
- [-] PromptBuilder input/output
  - [ ] Add data to query
- [x] LLMRunner input/output
- [-] ResponseParser input/output
  - [ ] Join output

---

# Phase 4 – Build the Core Infrastructure

## Runnable Framework

Implement:

- [x] Generic Runnable class
- [x] RunnableSequence
- [x] `|` operator

Test that chaining works before adding AI

---

# Phase 5 – Implement the Chain

## PromptBuilder

- [x] Accept typed input
- [x] Add system prompt
- [ ] Add dataset statistics
- [x] Add user question
- [x] Return prompt object (GeneratedPrompt)

---

## LLMRunner

- [x] Load SmolLM
- [x] Connect through `transformers.pipeline`
- [x] Generate raw output (LLMOutput)

---

## ResponseParser

- [ ] Parse raw model output
- [-] Extract only the useful answer
- [ ] Return structured response

---

## Assemble the Chain

```
PromptBuilder
        |
LLMRunner
        |
ResponseParser
```

- [x] Verify the chain works independently of FastAPI

---

# Phase 6 – Implement Data Handling

## Dataset Storage

- [x] Store uploaded DataFrame (in memory)
- [ ] Handle replacement uploads
- [x] Make statistics accessible

---

## CSV Processing

- [x] Read CSV
- [ ] Validate extension
- [x] Validate readability (via pandas)

VG:

- [x] Empty file detection
- [ ] Encoding errors
- [ ] File size limit

---

# Phase 7 – Build the API

## GET /health

- [x] Return status
  - [x] check subsystems

---

## POST /data/upload

- [x] Upload CSV
- [x] Validate
- [x] Store dataset
- [-] Return metadata
  - [-] Add pandas stats / shape

---

## GET /data/stats

- [x] Return `describe()` output
- [x] Return 404 if no dataset exists

---

## POST /ai/ask

- [ ] Validate request
- [x] Ensure dataset exists
- [x] Execute Runnable chain
- [ ] Return structured answer

---

# Phase 8 – Error Handling

Implement proper exceptions.

- [x] Invalid file
- [x] Missing dataset
- [ ] Invalid question
- [ ] Model failure
- [ ] Unexpected exceptions

VG:

- [ ] Empty model output
- [ ] Timeout handling

---

# Phase 9 – Logging (VG)

- [ ] Log uploads
- [ ] Log questions
- [ ] Log model execution
- [ ] Log errors

---

# Phase 10 – Testing

## Runnable Tests

- [ ] PromptBuilder
- [ ] LLMRunner (mocked)
- [ ] ResponseParser

---

## Endpoint Tests

- [ ] /health
- [ ] Upload success
- [ ] Upload failure
- [ ] Stats success
- [ ] Stats without dataset
- [ ] AI ask success

---

## Mock Tests

- [ ] Mock the LLM
- [ ] Verify the complete chain

---

## VG Edge Cases

- [ ] Empty CSV
- [ ] Invalid extension
- [ ] Invalid encoding
- [ ] Strange column names
- [ ] Missing dataset
- [ ] Empty AI response
- [ ] Model exception
- [ ] Oversized upload

---

# Phase 11 – Documentation

## README

- [ ] Installation
- [ ] Dependencies
- [ ] Running the project
- [ ] API examples
- [ ] Swagger usage
- [ ] Assumptions

---

## Reflection Report

### Security

- [ ] API keys
- [ ] `.env`
- [ ] File upload risks
- [ ] Prompt injection
- [ ] Mitigation

### GDPR

- [ ] Personal data
- [ ] Production considerations

### AI

- [ ] SmolLM limitations
  - [ ] hf_token warning - fixed unknown items in config
- [ ] Bias example
- [ ] Testing strategy

### Design

- [ ] Runnable advantages
- [ ] Separation of concerns
  - [ ] Move all pandas deps to data.py
  - [ ] Move model from steps to pipeline or new file (ex. llm.py)
- [ ] Biggest challenge
  - [ ] Pipeline working
- [ ] Solution
  - [ ] trail and error, re-run it, iterative
---

# Phase 12 – Final Review

## Functional Requirements

- [ ] All endpoints work
- [ ] Runnable chain contains at least three steps
- [ ] Pydantic models are used throughout
- [ ] SmolLM is integrated
- [ ] Error handling is complete

---

## Code Quality

- [ ] Type hints everywhere
- [ ] Clear module separation
  - [ ] Move all pandas deps to data.py
- [ ] Consistent naming
- [ ] No duplicated logic
- [ ] Logging implemented

---

## Submission

- [ ] README included
- [ ] Reflection included
- [ ] Tests pass
- [ ] `.env` excluded
- [ ] Push to public GitHub
- [ ] Email repository link with correct subject
