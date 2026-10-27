# ResumeAI — Master Implementation Plan V2

## Purpose

This is the **master implementation specification for Antigravity**.

Important: this V2 plan is designed to **continue from the existing ResumeAI project**, not rebuild it from scratch.

Antigravity must first inspect the current repository and verify the status of the components marked below. Previous work is represented as **Done / Partial / Planned**, but Antigravity must confirm the actual code before modifying anything.

---

# 1. Project Goal

ResumeAI is an advanced **NLP + Machine Learning resume intelligence and job-matching system**.

The system should:

1. Accept PDF/DOCX resumes.
2. Extract resume text.
3. Extract structured resume information.
4. Extract and normalize skills.
5. Use classical NLP and semantic NLP for resume-job matching.
6. Use pretrained transformer models for semantic representations.
7. Use an LLM for contextual skill inference and job requirement analysis.
8. Engineer resume-job features.
9. Train supervised ML models.
10. Compare Logistic Regression, Random Forest, and XGBoost.
11. Optionally use an ensemble if experiments justify it.
12. Provide explainable predictions.
13. Rank relevant jobs.
14. Identify skill gaps.
15. Provide results through Streamlit.
16. Generate reproducible experiments suitable for an IEEE research paper.

---

# 2. CURRENT PROJECT STATUS

## Legend

- ✅ **DONE** — already implemented or substantially implemented in our previous development.
- 🔄 **PARTIAL / VERIFY** — concept/code exists, but Antigravity must inspect and complete it if necessary.
- ⏳ **PLANNED** — not yet implemented or requires the advanced extension.

## Status Matrix

| Stage | Component | Status | Antigravity Action |
|---|---|---|---|
| 1 | Project setup / starter structure | ✅ Done | Verify |
| 2 | Streamlit resume upload | ✅ Done | Verify |
| 3 | PDF/DOCX text extraction | ✅ Done | Verify |
| 4 | NLP information extraction | ✅ Done | Verify |
| 5 | Contact extraction | ✅ Done | Verify |
| 6 | Skill extraction | ✅ Done | Verify/improve |
| 7 | Education extraction | ✅ Done | Verify |
| 8 | Experience extraction | ✅ Done | Verify |
| 9 | Project extraction | ✅ Done | Verify |
| 10 | Certification extraction | ✅ Done | Verify |
| 11 | Raw resume text display | ✅ Done | Verify |
| 12 | TF-IDF vectorization | 🔄 Partial / Verify | Test and complete |
| 13 | Cosine similarity | 🔄 Partial / Verify | Test and complete |
| 14 | Transformer semantic embeddings | 🔄 Partial / Verify | Inspect current implementation |
| 15 | ATS scoring logic | 🔄 Partial / Verify | Refine and document |
| 16 | Job dataset / job.csv concept | 🔄 Partial / Verify | Standardize job schema |
| 17 | Job matching | 🔄 Partial / Verify | Complete pipeline |
| 18 | Job ranking | 🔄 Partial / Verify | Integrate with ML |
| 19 | Skill-gap analysis | 🔄 Partial / Verify | Complete and explain |
| 20 | Logistic Regression | 🔄 Partial / Verify | Verify actual training/evaluation |
| 21 | Random Forest | 🔄 Partial / Verify | Verify actual training/evaluation |
| 22 | Training-data pipeline | 🔄 Partial / Verify | Verify provenance and labels |
| 23 | XGBoost | ⏳ Planned | Implement |
| 24 | Advanced pretrained embedding model | ⏳ Planned | Implement/evaluate |
| 25 | LLM contextual skill inference | ⏳ Planned | Implement |
| 26 | LLM job requirement extraction | ⏳ Planned | Implement |
| 27 | Feature fusion | ⏳ Planned | Implement |
| 28 | Model comparison | ⏳ Planned | Implement |
| 29 | Ensemble | ⏳ Planned | Implement only if justified |
| 30 | SHAP explainability | ⏳ Planned | Implement |
| 31 | Advanced job reranking | ⏳ Planned | Implement/evaluate |
| 32 | Ablation experiments | ⏳ Planned | Implement |
| 33 | Final evaluation | ⏳ Planned | Implement |
| 34 | Reproducibility package | ⏳ Planned | Implement |
| 35 | IEEE research outputs | ⏳ Planned | Generate from real results |

---

# 3. IMPORTANT INSTRUCTION FOR ANTIGRAVITY

**Do NOT assume that a component is complete merely because this document says DONE or PARTIAL.**

Before changing code:

1. Inspect the repository.
2. Locate the relevant implementation.
3. Run the application/tests where possible.
4. Compare the implementation with this plan.
5. Preserve existing working functionality.
6. Only then modify missing or incomplete parts.

Do not rebuild working modules unnecessarily.

---

# 4. EXISTING FUNCTIONALITY

## 4.1 Resume Upload

Current Streamlit application supports:

- PDF upload
- DOCX upload
- Resume processing
- Error handling

Expected flow:

```text
User
 ↓
Upload Resume
 ↓
PDF/DOCX Parser
 ↓
Raw Resume Text
```

---

## 4.2 Resume Text Extraction

The existing project contains:

```python
extract_resume_text(uploaded_file)
```

This is responsible for converting PDF/DOCX files into usable text.

Antigravity must preserve the existing interface unless there is a strong technical reason to change it.

---

## 4.3 NLP Information Extraction

The current project contains:

```python
extract_resume_information(text)
```

The extracted information includes:

```text
Email
Phone
Skills
Education
Experience
Projects
Certifications
```

Current Streamlit UI displays these fields.

---

# 5. EXISTING STREAMLIT FLOW

Current high-level flow:

```text
Resume Upload
      ↓
extract_resume_text()
      ↓
Raw Text
      ↓
extract_resume_information()
      ↓
Structured Information
      ↓
Streamlit Display
```

This functionality must remain working while advanced ML features are added.

---

# 6. NLP PIPELINE

## Stage A — Parsing

Input:

```text
PDF / DOCX
```

Output:

```text
Raw resume text
```

---

## Stage B — Section Detection

Identify sections such as:

```text
Contact
Summary
Skills
Education
Experience
Projects
Certifications
```

---

## Stage C — Information Extraction

Extract structured information.

Example:

```json
{
  "email": "candidate@example.com",
  "phone": "...",
  "skills": ["Python", "React", "MongoDB"],
  "education": "...",
  "experience": "...",
  "projects": "...",
  "certifications": "..."
}
```

---

# 7. SKILL EXTRACTION

Skill extraction should identify technical skills from:

- Skills section
- Experience
- Projects
- Education
- Certifications

Skills should eventually be normalized.

Example:

```text
JS
JavaScript
ECMAScript
```

→

```text
JavaScript
```

Another example:

```text
Postgres
PostgreSQL
```

→

```text
PostgreSQL
```

The system should maintain provenance:

```text
explicit
inferred
```

Do not claim an inferred skill as explicitly stated.

---

# 8. TF-IDF MODULE

## Purpose

TF-IDF is the classical NLP baseline.

It converts text into numerical vectors based on word importance.

Resume:

```text
Python React MongoDB REST API
```

Job:

```text
Python MongoDB REST API Node.js
```

The system generates:

```text
Resume TF-IDF vector
Job TF-IDF vector
```

Then:

```text
Cosine Similarity
```

is calculated.

This gives a lexical similarity score.

---

# 9. COSINE SIMILARITY

Formula:

```text
cosine_similarity(A,B) =
(A · B) / (||A|| ||B||)
```

Interpretation:

```text
1.0 → highly similar direction
0.0 → little/no similarity
```

Use it for:

- TF-IDF similarity
- Transformer embedding similarity

Do not describe cosine similarity itself as an ML model.

---

# 10. TRANSFORMER SEMANTIC EMBEDDINGS

The project should use a pretrained sentence-transformer style model.

Candidate advanced model:

```text
BAAI/bge-base-en-v1.5
```

The exact model must be configurable.

Existing MiniLM/Sentence Transformer implementation, if present, should be retained as a baseline.

Pipeline:

```text
Resume text
    ↓
Pretrained Transformer
    ↓
Embedding vector

Job text
    ↓
Pretrained Transformer
    ↓
Embedding vector

        ↓
Cosine Similarity
        ↓
Semantic similarity
```

The purpose is to capture semantic relationships that lexical TF-IDF can miss.

---

# 11. ATS SCORING

The current ATS approach should be treated as a **feature/rule-based baseline**, not the final advanced ML system.

Potential components:

```text
Skill Match
Keyword Match
Experience Match
Education Match
Resume Completeness
Semantic Similarity
```

Example conceptual structure:

```text
ATS Score =
weighted combination of documented matching features
```

The exact weights must be documented and validated.

Do not claim that manually selected weights are learned ML weights.

---

# 12. JOB DATA

The project has previously discussed:

```text
job.csv
```

A job record should contain standardized fields such as:

```text
job_id
title
company
description
skills
education
experience
location
```

The exact fields must be adapted to the actual dataset/API.

Important:

**Training data and live job listings must remain separate.**

Do not automatically train models on live API results.

---

# 13. JOB MATCHING

Current/previous concept:

```text
Resume
  ↓
Resume features
  ↓
Compare with jobs
  ↓
Similarity
  ↓
Matching jobs
```

Advanced pipeline:

```text
Resume
   ↓
NLP extraction
   ↓
Skill extraction
   ↓
Embeddings
   ↓
Feature engineering
   ↓
ML suitability prediction
   ↓
Job ranking
```

---

# 14. JOB RANKING

The system should not simply return a list of jobs.

It should produce:

```text
Job
Prediction
Similarity
Matched Skills
Missing Skills
Explanation
```

Example:

```text
Job A
Prediction: Good Fit
Semantic Similarity: ...
Matched Skills: Python, MongoDB, REST
Missing Skills: Docker
```

Numerical values shown in examples are placeholders only.

---

# 15. SKILL-GAP ANALYSIS

For every selected job:

```text
Required Skills
        ↓
Candidate Skills
        ↓
Intersection
        ↓
Matched Skills

Required Skills
        ↓
Candidate Skills
        ↓
Difference
        ↓
Missing Skills
```

Separate:

```text
Explicit Skills
Inferred Skills
```

This distinction is important for explainability.

---

# 16. MACHINE LEARNING PART

This project becomes an advanced ML project through supervised learning over engineered resume-job features.

## Feature examples

```text
TF-IDF similarity
Transformer semantic similarity
Skill match ratio
Missing skill ratio
Required skill count
Matched skill count
Inferred skill match
Experience match
Education match
Section completeness
Project count
Certification count
```

These become the ML input:

```text
Feature Vector
      ↓
ML Model
      ↓
Suitability Prediction
```

---

# 17. LOGISTIC REGRESSION

Purpose:

**Supervised baseline classifier.**

Possible output classes:

```text
Good Fit
Potential Fit
No Fit
```

It should provide a transparent baseline against which more complex models can be compared.

Evaluate using appropriate metrics such as:

- Accuracy
- Precision
- Recall
- F1
- Confusion Matrix
- ROC-AUC where applicable

Do not invent results.

---

# 18. RANDOM FOREST

Purpose:

Capture nonlinear relationships and feature interactions.

Example:

```text
High semantic similarity
+
High skill match
+
Good experience match
```

may interact differently than individual features suggest.

Random Forest should be trained and evaluated using the same protocol as Logistic Regression.

---

# 19. XGBOOST — ADVANCED ML EXTENSION

XGBoost should be added as the advanced boosted-tree classifier.

Pipeline:

```text
Engineered Features
      ↓
XGBoost
      ↓
Suitability Prediction
```

Use controlled hyperparameter tuning and validation.

Do not assume XGBoost is better.

The research result should come from actual evaluation.

---

# 20. PRETRAINED MODEL + LLM EXTENSION

This is a major planned improvement.

## Pretrained model

Use a pretrained embedding model such as:

```text
BAAI/bge-base-en-v1.5
```

for semantic representations.

## LLM

Use a configurable LLM provider for contextual language understanding.

The LLM should help with:

```text
Skill inference
Skill normalization
Job requirement extraction
Contextual evidence extraction
```

The LLM should **not automatically replace the supervised ML classifier**.

---

# 21. LLM CONTEXTUAL SKILL INFERENCE

Example resume:

```text
Developed a MERN application using Node.js,
Express and a document-oriented database.
```

Explicitly stated:

```text
MERN
Node.js
Express
```

The LLM may infer:

```text
MongoDB
```

if the evidence genuinely supports that inference.

The system must store:

```json
{
  "name": "MongoDB",
  "source": "inferred",
  "confidence": "...",
  "evidence": "..."
}
```

The example confidence is illustrative only.

---

# 22. JOB REQUIREMENT EXTRACTION

The LLM can convert unstructured job descriptions into structured requirements:

```text
Required skills
Preferred skills
Experience
Education
Responsibilities
Technologies
```

This makes job matching more structured.

---

# 23. FEATURE FUSION

Advanced feature vector:

```text
[
TF-IDF similarity,
Transformer similarity,
Skill match,
Missing skill ratio,
Inferred skill match,
Experience match,
Education match,
Resume completeness,
Project count,
Certification count,
...
]
```

This combined feature representation is used for ML.

---

# 24. MODEL COMPARISON

Models:

```text
Logistic Regression
Random Forest
XGBoost
```

Compare using the same test protocol.

Example report:

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | Actual result | Actual result | Actual result | Actual result |
| Random Forest | Actual result | Actual result | Actual result | Actual result |
| XGBoost | Actual result | Actual result | Actual result | Actual result |

Never put invented numbers into the report.

---

# 25. ENSEMBLE

Only after evaluating individual models:

```text
Logistic Regression
Random Forest
XGBoost
       ↓
Soft / Weighted Voting
       ↓
Final prediction
```

The ensemble should only be adopted if experiments provide evidence that it is useful.

---

# 26. EXPLAINABILITY

Use SHAP where technically appropriate.

The explanation should answer:

```text
Why did the model give this prediction?
```

Example feature contributions:

```text
Semantic similarity
Skill match
Experience match
Missing skills
Education match
```

Do not fabricate explanations.

---

# 27. ADVANCED JOB RERANKING

Optional advanced stage:

```text
Initial retrieval
      ↓
Top-K jobs
      ↓
Pretrained reranker / cross encoder
      ↓
Final ranking
```

Evaluate whether reranking improves:

```text
Precision@K
Recall@K
MRR
NDCG@K
```

Only adopt it if supported by experiments.

---

# 28. RESEARCH EXPERIMENTS

The project should eventually support:

### Experiment 1

```text
TF-IDF
```

### Experiment 2

```text
Transformer embeddings
```

### Experiment 3

```text
TF-IDF + Transformer
```

### Experiment 4

```text
Explicit skills only
```

### Experiment 5

```text
Explicit + LLM inferred skills
```

### Experiment 6

```text
Logistic Regression vs Random Forest vs XGBoost
```

### Experiment 7

```text
Individual models vs Ensemble
```

### Experiment 8

```text
Retrieval vs Retrieval + Reranking
```

### Experiment 9

Feature ablation:

```text
All features
- semantic features
- skill features
- experience features
- LLM features
```

This provides stronger evidence for the IEEE research paper.

---

# 29. DATA LEAKAGE RULES

Antigravity must prevent:

- Same resume appearing in train and test.
- Same candidate appearing across splits.
- Test labels influencing feature engineering.
- Hyperparameter tuning on the final test set.
- Live job data accidentally entering training.
- LLM-generated labels being treated as ground truth without documented validation.

---

# 30. DATASET RULES

The project previously specified that **synthetic data should not be used as the primary training dataset**.

Therefore:

1. Use documented real/available datasets.
2. Record source and license.
3. Record preprocessing.
4. Record labeling methodology.
5. Do not fabricate labels.
6. Do not silently replace a real dataset with synthetic data.
7. If the available dataset does not contain the required target labels, report the limitation before proceeding.

---

# 31. LIVE JOB API RULES

The live job API is for:

```text
Current job retrieval
```

not automatically:

```text
ML training
```

The architecture should be:

```text
Research Dataset
       ↓
Training / Evaluation

Live Job API
       ↓
Inference / Job Retrieval
```

Both should produce the same standardized job schema.

---

# 32. STREAMLIT FINAL UI

Planned sections:

```text
Dashboard
Resume Analysis
Extracted Information
Skill Intelligence
ATS Analysis
Job Matching
Skill Gap
Prediction Explanation
Model Performance
```

---

# 33. FINAL SYSTEM PIPELINE

The final intended architecture is:

```text
                    ┌──────────────────┐
                    │  Resume PDF/DOCX │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Resume Parser    │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ NLP Extraction   │
                    └────────┬─────────┘
                             ↓
              ┌──────────────┴──────────────┐
              ↓                             ↓
       Explicit Skills                Resume Text
              ↓                             ↓
       Normalization                Transformer Model
              ↓                             ↓
       LLM Inference                 Embeddings
              ↓                             ↓
       Inferred Skills               Semantic Similarity
              └──────────────┬──────────────┘
                             ↓
                    Feature Engineering
                             ↓
                  ┌──────────┼──────────┐
                  ↓          ↓          ↓
                 LR         RF       XGBoost
                  └──────────┼──────────┘
                             ↓
                         Comparison
                             ↓
                    Optional Ensemble
                             ↓
                    Explainability
                             ↓
                    Job Ranking
                             ↓
                     Skill Gap
                             ↓
                    Streamlit Results
```

---

# 34. TARGET PROJECT STRUCTURE

```text
ResumeAI/
├── app/
│   ├── nlp/
│   │   ├── parser.py
│   │   ├── extractor.py
│   │   ├── skill_extractor.py
│   │   ├── skill_normalizer.py
│   │   └── section_detector.py
│   ├── embeddings/
│   │   ├── embedding_model.py
│   │   ├── similarity.py
│   │   └── reranker.py
│   ├── llm/
│   │   ├── client.py
│   │   ├── skill_inference.py
│   │   ├── requirement_analysis.py
│   │   └── prompts.py
│   ├── features/
│   │   ├── tfidf_features.py
│   │   ├── skill_features.py
│   │   ├── experience_features.py
│   │   ├── education_features.py
│   │   └── feature_pipeline.py
│   ├── ml/
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   ├── predict.py
│   │   ├── logistic_model.py
│   │   ├── random_forest.py
│   │   ├── xgboost_model.py
│   │   └── ensemble.py
│   ├── explainability/
│   │   └── shap_explainer.py
│   ├── jobs/
│   │   ├── job_loader.py
│   │   ├── job_api.py
│   │   └── job_ranker.py
│   └── utils/
│       ├── config.py
│       └── logger.py
├── data/
│   ├── raw/
│   ├── processed/
│   ├── jobs/
│   └── external/
├── models/
│   ├── embeddings/
│   ├── classifiers/
│   └── vectorizers/
├── experiments/
│   ├── baseline/
│   ├── transformer/
│   ├── ml_comparison/
│   └── ablation/
├── frontend/
│   └── app.py
├── tests/
├── notebooks/
├── reports/
│   ├── figures/
│   ├── metrics/
│   └── experiments/
├── requirements.txt
├── README.md
└── .env.example
```

Antigravity should adapt this structure to the existing repository instead of blindly recreating it.

---

# 35. STAGE EXECUTION PLAN

## Phase 1 — Verify Existing Work

### Stage 1
Inspect repository and run current application.

### Stage 2
Verify resume parsing.

### Stage 3
Verify NLP information extraction.

### Stage 4
Verify skill extraction and normalization.

### Stage 5
Verify TF-IDF and cosine similarity.

### Stage 6
Verify existing transformer embeddings.

### Stage 7
Verify ATS scoring.

### Stage 8
Verify job dataset/job schema.

### Stage 9
Verify job matching, ranking, and skill-gap analysis.

### Stage 10
Verify existing Logistic Regression and Random Forest implementation.

---

# 36. Phase 2 — Advanced ML/NLP

### Stage 11
Implement BGE pretrained embeddings.

### Stage 12
Implement LLM client.

### Stage 13
Implement contextual skill inference.

### Stage 14
Implement LLM job requirement extraction.

### Stage 15
Implement advanced feature engineering.

### Stage 16
Implement reproducible training-data pipeline.

### Stage 17
Implement XGBoost.

### Stage 18
Run model comparison.

---

# 37. Phase 3 — Advanced Intelligence

### Stage 19
Implement ensemble if justified.

### Stage 20
Implement SHAP explainability.

### Stage 21
Implement advanced job ranking.

### Stage 22
Implement optional pretrained reranker.

### Stage 23
Implement skill-gap improvements.

---

# 38. Phase 4 — Research

### Stage 24
Run baseline experiments.

### Stage 25
Run pretrained-model experiments.

### Stage 26
Run LLM-inference experiments.

### Stage 27
Run ML model comparison.

### Stage 28
Run feature ablation.

### Stage 29
Run ranking/reranking experiments.

### Stage 30
Generate final evaluation.

---

# 39. Phase 5 — Product + IEEE

### Stage 31
Finalize Streamlit interface.

### Stage 32
Finalize reproducibility.

### Stage 33
Generate graphs and tables.

### Stage 34
Generate experiment artifacts.

### Stage 35
Prepare IEEE Results and Discussion evidence.

---

# 40. ANTIGRAVITY RULES

At every stage:

1. Inspect before editing.
2. Preserve working code.
3. Make the smallest necessary change.
4. Write tests where appropriate.
5. Run tests.
6. Run the application where appropriate.
7. Report files changed.
8. Report commands executed.
9. Report failures honestly.
10. Never fabricate results.
11. Never fabricate datasets.
12. Never fabricate metrics.
13. Never claim an improvement without an experiment.
14. Never silently implement future stages.
15. Stop after the requested stage.

---

# 41. ACCEPTANCE REPORT FORMAT

After every stage, Antigravity must respond using:

```text
STAGE:
<stage number and name>

STATUS:
PASS / PARTIAL / BLOCKED

FILES CHANGED:
- ...

IMPLEMENTATION:
- ...

TESTS RUN:
- ...

TEST RESULTS:
- ...

APPLICATION RESULT:
- ...

ISSUES/BLOCKERS:
- ...

NEXT STAGE:
<next stage>

STOP HERE.
```

---

# 42. MASTER ANTIGRAVITY PROMPT

Use this prompt with the file:

> Read `ResumeAI_Master_Implementation_Plan_V2.md` completely.
>
> This is an existing ResumeAI project. Do NOT rebuild it from scratch.
>
> First inspect the repository and determine which components from the CURRENT PROJECT STATUS section actually exist and work.
>
> Preserve working functionality.
>
> Start with **Phase 1 / Stage 1 only**.
>
> Do not implement future stages.
>
> Run the existing application and tests where possible.
>
> Compare the repository against this specification.
>
> At the end, provide the required ACCEPTANCE REPORT FORMAT and stop.
>
> Do not fabricate datasets, labels, metrics, citations, or results.

---

# 43. RESEARCH QUESTIONS

The completed project should allow investigation of:

1. Does transformer semantic similarity provide useful information beyond TF-IDF?
2. Does BGE provide better semantic matching than the existing sentence-transformer baseline?
3. Which of Logistic Regression, Random Forest, and XGBoost performs best on the engineered resume-job features?
4. Does adding LLM-inferred skills improve suitability prediction?
5. Does feature fusion improve prediction?
6. Does an ensemble improve over individual models?
7. Does reranking improve job retrieval/ranking metrics?
8. Which feature groups contribute most to prediction performance?

These are **research questions**, not predetermined conclusions.

---

# 44. FINAL IMPORTANT NOTE

The purpose of V2 is to prevent Antigravity from starting the project over.

The existing resume parsing, NLP extraction, Streamlit interface, and previously developed matching/ML components should be **verified first**.

Only after verification should missing advanced functionality be implemented.

The final project should be evidence-driven:

```text
Existing System
      ↓
Verification
      ↓
Advanced NLP
      ↓
Pretrained Models
      ↓
LLM Intelligence
      ↓
Feature Engineering
      ↓
Advanced ML
      ↓
Evaluation
      ↓
Explainability
      ↓
Job Ranking
      ↓
Research Experiments
      ↓
IEEE Paper Evidence
```
