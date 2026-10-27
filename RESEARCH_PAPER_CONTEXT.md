# ResumeAI V2: An End-to-End NLP & Explainable Machine Learning Job Matching System
## Research Paper Context Document

This document outlines the entire architecture, machine learning pipelines, and software engineering methodologies used to build ResumeAI V2. You can feed this entire document to ChatGPT (or any LLM) to generate an academic research paper, thesis, or technical article.

---

### 1. Abstract & System Overview
ResumeAI V2 is an advanced, full-stack intelligence platform that bridges the gap between raw applicant resumes (PDF/DOCX) and specific job descriptions using deep semantic Natural Language Processing (NLP) and supervised Machine Learning (ML). Unlike legacy rule-based Applicant Tracking Systems (ATS), ResumeAI leverages high-dimensional feature engineering, state-of-the-art embedding models, and tree-based classification to rank candidates. Crucially, the system utilizes SHAP (SHapley Additive exPlanations) to ensure the AI's decisions are 100% transparent and explainable to human users.

---

### 2. Core Architecture & Tech Stack
The project was migrated from a legacy monolithic Streamlit prototype to a highly scalable, decoupled microservice architecture.
*   **Backend Interface:** Python 3.10+, FastAPI (ASGI), Uvicorn.
*   **Frontend UI:** Next.js 15 (React), CSS Modules (Glassmorphism design, native dark-mode).
*   **Machine Learning/NLP Engine:** Scikit-Learn, XGBoost, SHAP, HuggingFace (`sentence-transformers`), Google Gemini API.
*   **Utility/Processing:** PyPDF2 (PDF parsing), python-docx, ReportLab (dynamic PDF generation).

---

### 3. NLP & Feature Engineering Pipeline
The system parses unstructured resume text and converts it into a rigid 13-dimensional feature matrix for ML inference.

1.  **Contextual LLM Extraction:** Replaced fragile Regex parsers with an LLM Factory Pattern (`LLMClient`). The system queries Google Gemini 1.5 Flash to intelligently extract structured JSON entities (skills, education levels, experience years) from both the candidate's resume and target job descriptions.
2.  **Dense Semantic Embeddings:** Dropped legacy `all-MiniLM-L6-v2` in favor of `BAAI/bge-base-en-v1.5`, a state-of-the-art embedding model. This computes the cosine similarity between the resume text and the job description, capturing deep semantic meaning rather than just keyword matching.
3.  **13-Dimensional Feature Matrix:** The system generates a fixed-length vector for every Resume-Job pair. Features include:
    *   `ats_score`: Structural score (0-100) based on section completeness.
    *   `semantic_similarity`: BGE-based cosine similarity.
    *   `skill_match_percent`: Jaccard similarity of extracted skills.
    *   `experience_diff`: Target years of experience minus candidate's years of experience.
    *   `missing_skills_count`: Absolute count of skill gaps.
    *   `has_degree`, `education_match`, `is_manager`, etc.

---

### 4. Advanced Machine Learning (XGBoost & Random Forest)
ResumeAI treats job matching as a Multi-Class Supervised Learning problem. The model predicts the probability that a candidate is a `Good Fit`, `Potential Fit`, or `No Fit`.

1.  **Model Selection & Ablation:** We implemented a rigorous training loop (`train.py`) that executes Grid Search and Stratified K-Fold cross-validation across three architectures:
    *   *Logistic Regression*: Used as a high-bias baseline.
    *   *Random Forest*: Captures non-linear feature interactions.
    *   *XGBoost (Extreme Gradient Boosting)*: The final production model, chosen for its superior handling of tabular feature interactions and speed.
2.  **Standardization:** Continuous features (like `semantic_similarity`) are normalized using `StandardScaler` to stabilize gradient descent and tree splitting criteria.
3.  **Confidence Calibration:** The backend returns raw class probabilities rather than binary outputs, allowing the frontend to rank candidates precisely by their `Good Fit` confidence score.

---

### 5. eXplainable AI (XAI) using SHAP
A critical novelty of ResumeAI is its commitment to transparent AI. Job seekers and recruiters deserve to know *why* an AI made a decision.
1.  **Dynamic Explainer Factory:** The `SuitabilityPredictor` dynamically loads `shap.TreeExplainer` for XGBoost/Random Forest models, or `shap.LinearExplainer` if defaulting to Logistic Regression.
2.  **Log-Odds Translation:** SHAP calculates the marginal contribution of every single feature (e.g., `skill_match_percent: +0.45`, `experience_diff: -0.21`).
3.  **Human-Readable Insights:** The backend parses the absolute maximum SHAP values and converts them into natural language. For example, instead of outputting raw matrices, the API returns: *"Your semantic similarity significantly influenced the AI towards 'Good Fit', but your missing skills count pulled the score down."*

---

### 6. Decoupled Frontend & UI Engineering
The presentation layer was entirely rebuilt in Next.js to provide a premium user experience.
1.  **Glassmorphism & Micro-animations:** The dashboard features responsive CSS grids, backdrop-blur aesthetics, and smooth React state transitions.
2.  **Interactive Diagnostics:** Features an `AtsBreakdown` component that renders a checklist of the user's structural resume scores.
3.  **Skill Gaps & Upskilling:** The frontend computes the exact delta between candidate skills and job requirements, dynamically rendering "Upskill" links that redirect the user to Coursera search queries for missing skills.
4.  **In-Browser Report Generation:** The React client can trigger a `POST /api/v1/report` request to the FastAPI backend, which uses `ReportLab` to stitch together the ML probabilities, SHAP insights, and ATS breakdown into a downloadable PDF report.

---

### 7. Future Directions (V3 Architecture)
*   **Auto-Resume Optimization:** Using Gemini to actively rewrite weak bullet points to maximize the ATS score.
*   **Live Web Scraping:** Injecting real-time job requisitions from LinkedIn/Indeed to replace the mock database.
*   **RLHF (Reinforcement Learning from Human Feedback):** Adding 👍/👎 buttons to the Next.js UI to incrementally retrain the XGBoost model based on user matching preferences.
