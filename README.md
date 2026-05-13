# Telecom Fraud Detection Platform
> End-to-End ML + GenAI System for Telecom Fraud Detection

## Overview
A production-grade telecom fraud detection system that analyzes Call Detail Records (CDR) to identify fraudulent callers. The system combines a trained Random Forest ML model with a GenAI layer — LLM-powered explanations, LLM-as-Judge quality evaluation, and a RAG pipeline grounded in TRAI regulations.

---

## Project Status
| Phase | Description | Status |
|---|---|---|
| EDA | Exploratory data analysis, class distribution, visualizations | ✅ Complete |
| Feature Engineering | 15 raw CDR fields → 29 engineered features | ✅ Complete |
| ML Modelling | Random Forest, SHAP analysis, model comparison | ✅ Complete |
| GenAI — Explainer | LLM explanation for flagged numbers via Ollama/LLaMA3 | ✅ Complete |
| GenAI — Judge | LLM-as-Judge explanation quality evaluation | ✅ Complete |
| GenAI — RAG | ChromaDB + TRAI knowledge base + RAG query pipeline | ✅ Complete |
| FastAPI Backend | /score, /explain, /query endpoints | ✅ Complete |
| Streamlit Dashboard | Visual UI for analysts | 🔄 In Progress |
| Docker Compose | Containerized deployment | 🔄 In Progress |

---

## Tech Stack
| Layer | Tools |
|---|---|
| ML | Scikit-learn, Random Forest, SHAP |
| GenAI | Ollama, LLaMA3, ChromaDB, Sentence Transformers |
| Backend | FastAPI, Uvicorn, Pydantic |
| Frontend | Streamlit (in progress) |
| DevOps | Docker Compose (in progress) |

---

## Project Structure
telecom-spam-detection/
│
├── notebooks/
│   ├── 01_eda.ipynb                 # Exploratory Data Analysis
│   ├── 02_feature_engineering.ipynb # Feature Engineering (29 features)
│   └── 03_model_cdr.ipynb           # Model Training + SHAP
│
├── genai/
│   ├── explainer.py                 # Fraud score + LLM explanation
│   ├── judge.py                     # LLM-as-Judge quality check
│   └── rag/
│       ├── pipeline.py              # ChromaDB + RAG query pipeline
│       ├── knowledge_base.py        # TRAI regulation documents
│       └── scraper.py               # Document scraper
│
├── api/
│   ├── main.py                      # FastAPI app entry point
│   ├── models.py                    # Pydantic input/output schemas
│   └── routes/
│       ├── scoring.py               # POST /score
│       ├── explain.py               # POST /explain
│       └── rag.py                   # POST /query
│
├── models/artifacts/
│   ├── fraud_model.pkl              # Trained Random Forest
│   ├── features_names.pkl           # 29 feature names
│   └── scaler.pkl                   # Feature scaler
│
├── data/
│   ├── chromadb/                    # Vector store (15 TRAI docs)
│   ├── processed/                   # Processed CSVs + plots
│   └── raw/                         # Raw CDR data
│
└── docker-compose.yml               # Container orchestration

---

## API Endpoints

### `POST /score`
CDR data lo, fraud probability return karo.
```json
// Request
{
  "Account_Length": 82,
  "VMail_Message": 0,
  "Day_Mins": 300.3,
  "Day_Calls": 109,
  "Day_Charge": 51.05,
  "Eve_Mins": 181.0,
  "Eve_Calls": 100,
  "Eve_Charge": 15.39,
  "Night_Mins": 270.1,
  "Night_Calls": 73,
  "Night_Charge": 12.15,
  "Intl_Mins": 11.7,
  "Intl_Calls": 4,
  "Intl_Charge": 3.16,
  "CustServ_Calls": 0
}

// Response
{
  "fraud_probability": 0.98,
  "fraud_percentage": 98.0,
  "is_fraud": true,
  "risk_level": "CRITICAL",
  "top_features": {
    "Day Mins": 300.3,
    "Day Calls": 109
  },
  "message": "Fraud indicators detected. Risk level: CRITICAL. Manual review recommended."
}
```

### `POST /explain`
Fraud score + LLM plain English explanation + Judge verdict.
```json
// Response
{
  "fraud_probability": 0.98,
  "fraud_percentage": 98.0,
  "is_fraud": true,
  "risk_level": "CRITICAL",
  "top_features": {...},
  "explanation": "This number was flagged due to unusually high daytime usage...",
  "judge_score": "SCORE: 4/5 — ACCURACY: Good — CLARITY: Good..."
}
```

### `POST /query`
TRAI knowledge base se RAG-grounded answer lo.
```json
// Request
{
  "question": "What happens after third TRAI violation?",
  "n_results": 3
}

// Response
{
  "question": "What happens after third TRAI violation?",
  "answer": "After a third TRAI violation, the telemarketer is subject to permanent blacklisting.",
  "sources": [
    "TRAI Regulations — Penalty Framework",
    "TRAI DND Registry — How It Works",
    "TRAI UCC Regulations — Definition"
  ]
}
```

---

## How to Run

### Prerequisites
```bash
pip install -r requirements.txt
ollama pull llama3
```

### Start the System
```bash
# Terminal 1 — LLM server
ollama serve

# Terminal 2 — FastAPI server (project root se)
uvicorn api.main:app --reload
```

### Swagger UI
http://127.0.0.1:8000/docs

---

## Risk Level Logic
| Fraud Probability | Risk Level |
|---|---|
| 0.0 — 0.3 | LOW |
| 0.3 — 0.5 | MEDIUM |
| 0.5 — 0.7 | HIGH |
| 0.7 — 1.0 | CRITICAL |

---

## Key Results
| Metric | Value |
|---|---|
| Model | Random Forest |
| Features | 29 engineered from 15 raw CDR fields |
| Fraud threshold | 0.3 probability |
| Knowledge base | 15 TRAI regulation documents |
| API endpoints | 3 (/score, /explain, /query) |
| Swagger UI | http://127.0.0.1:8000/docs |