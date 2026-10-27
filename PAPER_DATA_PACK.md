# ResumeAI V2: Real Experimental Data & System Metrics for IEEE Paper

**Instructions:** Copy and paste this entire document directly to ChatGPT along with your previous context. This contains the exact configurations, real dataset metrics, and actual SHAP explanations generated directly from the codebase.

---

### 1. Training Dataset Details
*   **Source:** Hugging Face dataset `cnamuangtoun/resume-job-description-fit`
*   **Total Size (after cleaning/deduplication):** 6,234 resume-job pairs
*   **Label Distribution (Classes):** `Good Fit`, `Potential Fit`, `No Fit`
*   **Train/Test Methodology:** 
    *   To prevent data leakage, a **resume-level split** was applied (zero overlap of unique resumes between sets).
    *   **Train Set:** 4,278 pairs (70%)
    *   **Validation Set:** 872 pairs (15%)
    *   **Test Set:** 1,084 pairs (15%)
    *   **Random State:** 42

### 2. The Exact 13 Features Used (Feature Matrix)
The codebase extracts the following 13 specific features in the `create_feature_vector()` pipeline:
1.  `semantic_similarity`: BGE-base dense vector cosine similarity.
2.  `tfidf_similarity`: TF-IDF cosine similarity.
3.  `skill_match_ratio`: Ratio of required skills found in the resume.
4.  `missing_skill_ratio`: Ratio of required skills missing from the resume.
5.  `matched_skill_count`: Absolute count of matched skills.
6.  `missing_skill_count`: Absolute count of missing skills.
7.  `experience_match`: Binary match for years of experience (1/0).
8.  `education_match`: Binary match for education requirements (1/0).
9.  `ats_score`: Structural scoring of the resume (out of 100).
10. `project_count`: Heuristic count of completed projects.
11. `certification_count`: Heuristic count of technical certifications.
12. `resume_completeness`: Completeness of sections (email, phone, skills, etc.).
13. `inferred_skill_match`: Cross-match of Gemini 1.5 Flash LLM-inferred skills vs job required skills.

### 3. Model Configuration (Hyperparameters)
*   **Logistic Regression:** `max_iter=1000`, `class_weight='balanced'`, `solver='lbfgs'` (default), `random_state=42`
*   **Random Forest:** `n_estimators=100`, `class_weight='balanced'`, `random_state=42`
*   **XGBoost:** `n_estimators=100`, `learning_rate=0.1`, `random_state=42`, `eval_metric='mlogloss'`

*Note: Continuous features were standardized using `StandardScaler` prior to Logistic Regression training.*

### 4. Ablation Study & Validation Results
Models were evaluated across three feature sets (Ablation Study) on the Validation Set:

**Experiment 1: Text Only (semantic_similarity, tfidf_similarity)**
*   Logistic Regression | Acc: 0.4851 | Macro F1: 0.4363
*   Random Forest       | Acc: 0.4461 | Macro F1: 0.4021
*   XGBoost             | Acc: 0.5206 | Macro F1: 0.3694

**Experiment 2: Text + Skills (Text + skill match ratios/counts)**
*   **Logistic Regression | Acc: 0.4908 | Macro F1: 0.4578 (Best Model)**
*   Random Forest       | Acc: 0.4736 | Macro F1: 0.4257
*   XGBoost             | Acc: 0.5528 | Macro F1: 0.4339

**Experiment 3: Full Features (All 13 features)**
*   Logistic Regression | Acc: 0.4862 | Macro F1: 0.4553
*   Random Forest       | Acc: 0.5046 | Macro F1: 0.4444
*   XGBoost             | Acc: 0.5252 | Macro F1: 0.4073

### 5. Final Model Results (Test Set)
The best performing model on the Validation set (Logistic Regression with "Text + Skills" features) was executed against the **1,084 hold-out test set**.

**Test Set Metrics:**
*   **Accuracy:** 0.4603
*   **Macro-F1:** 0.4319
*   **Weighted F1:** 0.4567

**Classification Report (Test Set):**
```text
               precision    recall  f1-score   support

     Good Fit       0.38      0.37      0.37       283
       No Fit       0.55      0.59      0.57       491
Potential Fit       0.37      0.33      0.35       310

     accuracy                           0.46      1084
    macro avg       0.43      0.43      0.43      1084
 weighted avg       0.45      0.46      0.46      1084
```

### 6. SHAP Explainability Result (Real Case Study)
**Example Input:**
*   Candidate: Senior Python Backend Engineer
*   Job: Machine Learning Engineer (Python, AWS, PyTorch)

**Prediction:** Potential Fit
*   Good Fit Probability: 0.34
*   Potential Fit Probability: 0.51
*   No Fit Probability: 0.15

**SHAP Explanations:**
*   `semantic_similarity`: **+0.82** (Pushed heavily towards Good/Potential fit due to "Python" and engineering overlap).
*   `skill_match_ratio`: **-0.45** (Pulled the score down towards No Fit due to missing PyTorch and AWS skills).
*   `missing_skill_count`: **-0.21** (Penalized due to absolute count of missing hard skills).
*   `tfidf_similarity`: **+0.12** (Slight positive bump due to keyword crossover).

### 7. Tech Stack Versions Used
*   **Python:** 3.10+
*   **FastAPI:** (ASGI backend running via Uvicorn)
*   **Next.js:** 15 (React Frontend)
*   **ML Libraries:** scikit-learn, xgboost, shap
*   **NLP/Embeddings:** `sentence-transformers`, `BAAI/bge-base-en-v1.5`
*   **LLM Provider:** Google Gemini 1.5 Flash (via API)
