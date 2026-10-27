# ResumeAI V2: Intelligent Career & Job Recommendation Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Latest-F7931E.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Enabled-EB5424.svg)](https://xgboost.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/Explainability-SHAP-brightgreen.svg)](https://shap.readthedocs.io/)

**ResumeAI V2** is an end-to-end, explainable AI platform that bridges the gap between applicant resumes (PDF/DOCX) and targeted job postings. Migrated from a monolithic prototype into a production-grade decoupled architecture, ResumeAI combines deep semantic Natural Language Processing (NLP), multi-class supervised Machine Learning (XGBoost / Random Forest), and transparent eXplainable AI (XAI with SHAP) to evaluate applicant suitability and provide actionable feedback.

---

## Architecture Overview

```
+-------------------------------------------------------------------------+
|                              ResumeAI V2                                |
+-------------------------------------------------------------------------+
       |                                                 |
       v                                                 v
[ Candidate Resume ]                              [ Job Postings ]
  (PDF / DOCX)                                      (Database/API)
       |                                                 |
       +-----------------------+-------------------------+
                               |
                               v
               +-------------------------------+
               |    NLP & Extraction Layer     |
               |  - PyPDF2 / python-docx       |
               |  - Gemini 1.5 Flash (Entities)|
               |  - BGE Base v1.5 (Embeddings) |
               +-------------------------------+
                               |
                               v
               +-------------------------------+
               |    13D Feature Engineering    |
               |  - ATS Structural Scoring     |
               |  - Cosine Semantic Similarity |
               |  - Skill Gap / Jaccard Match  |
               |  - Experience & Education Gap |
               +-------------------------------+
                               |
                               v
               +-------------------------------+
               |      Supervised ML Model      |
               |  - XGBoost / Random Forest    |
               |  - 3-Class Fit Probabilities  |
               +-------------------------------+
                               |
                               v
               +-------------------------------+
               |   eXplainable AI (SHAP XAI)   |
               |  - Dynamic TreeExplainer      |
               |  - Human-Readable Insights    |
               +-------------------------------+
                               |
                +--------------+--------------+
                |                             |
                v                             v
       [ FastAPI REST API ]          [ Next.js Web UI ]
      (JSON & PDF Generator)         (Glassmorphism UI)
```

---

## Key Features

- **Document Ingestion**: High-fidelity text extraction from `.pdf` and `.docx` resumes with automated formatting cleanup.
- **Contextual Entity Extraction**: Powered by Google Gemini 1.5 Flash to accurately extract skills, degree levels, and years of experience without fragile regex rules.
- **Dense Semantic Embeddings**: Uses state-of-the-art `BAAI/bge-base-en-v1.5` embeddings via Hugging Face `sentence-transformers` for deep semantic similarity beyond keyword matching.
- **ATS Structural Scoring**: Comprehensive 0–100 rubric evaluating section completeness (Contact Info, Summary, Experience, Education, Technical Skills).
- **13-Dimensional Feature Pipeline**: Combines text metrics, semantic similarity, ATS scores, experience differentials, and skill gaps into a structured inference matrix.
- **Supervised Classification**: Predicts candidate suitability across 3 classes:
  - `Good Fit`
  - `Potential Fit`
  - `No Fit`
- **Transparent Explainability (SHAP)**: Leverages `shap.TreeExplainer` to demystify black-box predictions, translating mathematical log-odds contributions into clear, actionable bullet points.
- **Dynamic PDF Diagnostic Reports**: Automated downloadable PDF summary reports built with ReportLab.
- **Modern User Interfaces**:
  - **Next.js 15 Web Application**: Glassmorphism dark-mode UI with live file upload, ATS score breakdowns, match cards, and SHAP insight widgets.
  - **Streamlit Dashboard**: Alternate/legacy dashboard for rapid testing and experimentation.

---

## Repository Structure

```text
AML/
├── app/
│   ├── api/
│   │   └── main.py                 # FastAPI application endpoints
│   ├── jobs/
│   │   ├── api_client.py           # External job search API client
│   │   ├── matcher.py              # ML-powered job ranking logic
│   │   └── repository.py           # Job storage & dataset management
│   ├── llm/
│   │   ├── client.py               # Gemini LLM client factory
│   │   ├── prompts.py              # System prompts & few-shot templates
│   │   └── skill_inference.py      # LLM-based skill inference
│   ├── ml/
│   │   ├── explainer.py            # SHAP model explainability engine
│   │   ├── features.py             # 13D feature extraction pipeline
│   │   ├── predictor.py            # Model inference & calibration
│   │   └── train.py                # Model training, cross-validation & ablation
│   ├── nlp/
│   │   ├── embeddings.py           # BGE sentence embeddings
│   │   ├── extractor.py            # Resume entity extraction
│   │   └── parser.py               # PDF and DOCX parsers
│   ├── reporting/
│   │   └── pdf_generator.py        # ReportLab PDF diagnostic generator
│   └── scoring/
│       ├── explainability.py       # ATS feedback rules
│       └── resume_score.py         # Structural ATS scoring engine
├── data/
│   ├── jobs/                       # Sample jobs CSV & template
│   ├── resumes/                    # Test resumes
│   └── training/                   # Model dataset & preparation scripts
├── frontend/
│   ├── app.py                      # Streamlit application
│   └── web/                        # Modern Next.js 15 web application
│       ├── src/
│       │   ├── app/                # Next.js App Router (pages & styles)
│       │   └── components/         # React components (Upload, JobCard, etc.)
│       └── package.json
├── models/                         # Model metadata & evaluation metrics
├── .env.example                    # Environment variable template
├── .gitignore                      # Git exclusion rules
├── requirements.txt                # Python backend dependencies
└── README.md                       # Project documentation
```

---

## Getting Started

### 1. Prerequisites

- **Python**: Version 3.10 or higher
- **Node.js**: Version 18.x or higher
- **Package Managers**: `pip` and `npm`

### 2. Environment Configuration

Create a `.env` file in the project root directory:

```env
# Google Gemini API key (for LLM extraction)
GEMINI_API_KEY="your-google-gemini-api-key"

# Optional: RapidAPI / Job Search Provider Key
RAPIDAPI_KEY="your-rapidapi-key"
```

### 3. Backend Setup

```bash
# 1. Clone repository
git clone https://github.com/Izuku-midoriy/ResumeAi.git
cd ResumeAi

# 2. Create and activate a virtual environment
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Start the FastAPI backend
uvicorn app.api.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. You can explore interactive Swagger documentation at `http://localhost:8000/docs`.

---

## Frontend Setup

### Option A: Modern Next.js UI (Recommended)

Open a new terminal window:

```bash
cd frontend/web

# Install dependencies
npm install

# Run development server
npm run dev
```

Open your browser at `http://localhost:3000`.

### Option B: Streamlit Dashboard (Alternate / Testing)

With the virtual environment active:

```bash
streamlit run frontend/app.py
```

The Streamlit dashboard will open at `http://localhost:8501`.

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/match` | Upload a resume (`.pdf` / `.docx`). Returns ATS score, extracted profile, ranked job matches, and SHAP explainability insights. |
| `POST` | `/api/v1/report` | Generates and downloads a branded PDF audit report summarizing scores, matches, and recommendations. |
| `GET` | `/docs` | Interactive OpenAPI / Swagger UI documentation. |

---

## Model Training & Evaluation

To retrain the supervised models or perform ablation studies:

```bash
# Prepare dataset
python data/training/prepare_real_training_data.py

# Train models and generate evaluation metrics
python -m app.ml.train
```

Outputs and metrics are saved to `models/evaluation_results.json` and `models/model_meta.json`.

---

## Research & Documentation

For in-depth theoretical formulations, feature matrices, and ablation benchmark summaries, please refer to:
- [`RESEARCH_PAPER_CONTEXT.md`](RESEARCH_PAPER_CONTEXT.md)
- [`PAPER_DATA_PACK.md`](PAPER_DATA_PACK.md)
- [`PROJECT_ROADMAP.md`](PROJECT_ROADMAP.md)

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

