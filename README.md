# Resume Intelligence & Job Recommendation System

Starter project for an Advanced Machine Learning mini-project.

## Current stage
Stage 8 (Supervised ML) is completed!
- Real training data loaded from Hugging Face (`cnamuangtoun/resume-job-description-fit`)
- 9-dimensional ML feature extraction (including ATS score, Semantic embeddings, and TF-IDF)
- Strict resume-level Train/Validation/Test split to prevent data leakage
- 3-class classification ("Good Fit", "Potential Fit", "No Fit") using Logistic Regression and Random Forest
- Comprehensive Ablation Study (Text Only vs Text+Skills vs Full Features)
- Job recommendations ranked by `P(Good Fit) + 0.5 * P(Potential Fit)`
- Streamlit Dashboard displaying prediction classes and AI-generated explanations

## Planned stages
1. Resume parsing (Done)
2. NLP skill/entity extraction (Done)
3. ATS/resume scoring (Done)
4. Job dataset (Done)
5. Sentence Transformer semantic matching (Done)
6. Feature Engineering (Done)
7. Supervised ML job suitability model (Done)
8. Live job API integration (Done)
9. Final dashboard (Done)

## Run

Create and activate a virtual environment, then install:

```bash
pip install -r requirements.txt
```
.\venv\Scripts\Activate.ps1
uvicorn app.api.main:app --reload --port 8000

Run Streamlit:

```bash
streamlit run frontend/app.py
```
cd "frontend\web"
npm run dev

The app should open in your browser.

## Project structure

```text
resume-job-matcher/
├── app/
│   ├── main.py
│   ├── nlp/
│   │   ├── parser.py
│   │   ├── extractor.py
│   │   └── embeddings.py
│   ├── ml/
│   │   ├── features.py
│   │   ├── train.py
│   │   └── predictor.py
│   ├── scoring/
│   │   └── resume_score.py
│   ├── jobs/
│   │   └── matcher.py
│   └── database/
│       └── db.py
├── data/
│   ├── resumes/
│   └── jobs/
├── models/
├── frontend/
│   └── app.py
├── requirements.txt
└── README.md
```
