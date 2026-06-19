# Persona Adaptive Support Agent

A Streamlit-based AI customer support system that combines **Persona Classification**, **Retrieval-Augmented Generation (RAG)**, and **Human Escalation** workflows to provide adaptive customer support responses.

---

## Features

### Persona Classification

Classifies incoming customer messages into personas such as:

* Technical Expert
* Frustrated User
* Business Executive

The response style is adapted based on the detected persona.

---

### Retrieval-Augmented Generation (RAG)

Uses:

* Gemini Embeddings (`gemini-embedding-001`)
* ChromaDB Vector Database
* Markdown, TXT, and PDF knowledge sources

The system retrieves the most relevant support documentation before generating a response.

---

### Human Escalation

Sensitive issues such as:

* Refund requests
* Billing disputes
* Duplicate charges
* Escalation requests

are automatically routed to human support with a structured handoff summary.

---

### Streamlit Dashboard

Interactive web interface displaying:

* Customer Query
* Detected Persona
* Retrieved Sources
* Similarity Scores
* Generated Response
* Escalation Details

---

## Project Architecture

```text
Customer Query
       │
       ▼
Persona Classifier
       │
       ▼
RAG Retriever
(ChromaDB + Gemini Embeddings)
       │
       ▼
Adaptive Response Generator
       │
       ├── Normal Response
       │
       └── Escalation Engine
                 │
                 ▼
          Human Handoff JSON
```

---

## Tech Stack

### Frontend

* Streamlit

### LLM & Embeddings

* Google Gemini API
* Gemini Embedding 001
* Gemini 2.5 Flash

### Vector Database

* ChromaDB

### Document Processing

* PyPDF
* LangChain Text Splitters

### Environment Management

* Python 3.11+
* python-dotenv

---

## Knowledge Base

The system indexes the following support documents:

```text
data/
├── account_management.txt
├── api_troubleshooting.md
├── authentication_guide.md
├── billing_policy.txt
├── database_integration.md
├── password_reset_guide.md
├── password_reset_guide.pdf
├── payment_failures.md
├── refund_policy.md
└── ui_troubleshooting.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/persona-support-agent.git

cd persona-support-agent
```

---

### Create Virtual Environment

```bash
python -m venv myenv
```

Activate:

Windows:

```bash
myenv\Scripts\activate
```

Mac/Linux:

```bash
source myenv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Build Knowledge Base

Run once to create vector embeddings:

```python
from src.rag_pipeline import LocalRAGPipeline

rag = LocalRAGPipeline()
rag.ingest_all("data")
```

Verify:

```python
print(rag.collection.count())
```

Expected:

```text
12
```

or higher.

---

## Run Application

```bash
streamlit run app.py
```

Application launches at:

```text
http://localhost:8501
```

---

## Example Queries

### Technical Expert

```text
What headers are required for bearer token authentication?
```

Expected:

* Persona: Technical Expert
* Retrieves authentication documentation

---

### Password Reset

```text
I forgot my password.
```

Expected:

* Retrieves password reset instructions

---

### Payment Failure

```text
My payment failed.
```

Expected:

* Retrieves troubleshooting steps

---

### Escalation Scenario

```text
I was charged twice and need a refund immediately.
```

Expected:

* Persona: Frustrated User
* Human escalation triggered
* Handoff summary generated

---

## Sample Output

### Persona

```json
{
  "persona": "Technical Expert",
  "confidence": 0.95
}
```

### Retrieved Sources

```text
authentication_guide.md
api_troubleshooting.md
database_integration.md
```

### Response

```text
Authorization: Bearer YOUR_API_TOKEN
```

---

## Screenshots

### Main Dashboard

Add screenshot here:

```text
docs/dashboard.png
```

### Technical Expert Query

Add screenshot here:

```text
docs/technical_query.png
```

### Escalation Workflow

Add screenshot here:

```text
docs/escalation_workflow.png
```

---

## Future Improvements

* Conversation memory
* Multi-turn support
* Ticketing system integration
* CRM integration
* Real-time analytics dashboard
* Role-based support routing

---

## Author

Ramas

AI/ML Engineer

---


## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```
