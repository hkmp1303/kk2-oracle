# kk2-oracle
FastAPI SmolLLM interface
# KK2 – AI-Powered Data Analysis API

## Overview

This project is a REST API built with **FastAPI*- that allows users to upload a CSV dataset, retrieve descriptive statistics, and ask natural language questions about the dataset using a Large Language Model (LLM).

The application uses a custom **Runnable pipeline*- consisting of three processing steps:

- PromptBuilder
- LLMRunner
- ResponseParser

The language model used is **HuggingFaceTB/SmolLM2-135M-Instruct**, accessed through the Hugging Face `transformers` library.

---

## Features

- Upload CSV datasets
- Store datasets in memory
- Generate descriptive statistics using Pandas
- Ask questions about uploaded datasets
- AI-powered responses using SmolLM
- Runnable pipeline architecture
- REST API with automatic Swagger documentation

---

## Technologies

- Python 3.13
- FastAPI
- Pydantic
- Pandas
- Transformers
- Hugging Face
- Uvicorn

---

## Project Structure

```text
app/
├── chain/
│   ├── pipeline.py
│   ├── runnable.py
│   └── steps.py
├── config.py
├── data.py
├── main.py
└── schemas.py

tests/
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd kk2-oracle
```

Install dependencies:

```bash
uv sync
```

---

## Configuration

If using Hugging Face authentication, create a `.env` file:

```text
HF_TOKEN=your_token_here
```

---

## Running the Application

Start the API:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### GET /health

Checks that the API is running.

---

### POST /data/upload

Uploads a CSV dataset.

Example:

```text
multipart/form-data

file = dataset.csv
```

---

### GET /data/stats

Returns descriptive statistics generated using `pandas.DataFrame.describe()`.

---

### POST /ai/ask

Accepts a natural language question about the uploaded dataset.

Example request:

```json
{
  "q": "How many columns are in the dataset?"
}
```

Example response:

```json
{
  "status": "ok",
  "a": "There are 5 columns."
}
```

---

## Runnable Pipeline

The AI workflow is implemented using a custom Runnable pipeline.

```text
Question
    │
    ▼
PromptBuilder
    │
    ▼
LLMRunner
    │
    ▼
ResponseParser
    │
    ▼
API Response
```

### PromptBuilder

Creates the prompt by combining:

- system instructions
- dataset statistics
- user question

### LLMRunner

Executes the prompt using the Hugging Face `transformers` pipeline and SmolLM.

### ResponseParser

Extracts the generated answer before returning it to the API.

---

## Assumptions

- Only one dataset is stored in memory at a time.
- Uploaded datasets are not persisted after the application stops.
- The quality of AI responses depends on the capabilities of the SmolLM model.
- Dataset statistics are used as context instead of the full dataset to reduce prompt size.

---

## Testing

Tests are located in the `tests/` directory.

Run all tests:

```bash
pytest
```

---

## Known Limitations

- Only one dataset is stored in memory at a time.
- Uploaded datasets are not persisted after the application shuts down.
- AI responses depend on the capabilities of the SmolLM2-135M-Instruct model and may occasionally be inaccurate.
- The model is provided with dataset statistics rather than the full dataset, so some questions cannot be answered accurately.

---

## Future Improvements

- Support multiple uploaded datasets.
- Persist datasets using a database.
- Improve prompt engineering and response parsing.
- Add more comprehensive validation and error handling.
- Increase automated test coverage.
- Add structured logging and monitoring.
