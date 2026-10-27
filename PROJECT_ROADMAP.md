# AI-Powered Resume Intelligence and Job Recommendation System

## 1. Project Title

**AI-Powered Resume Intelligence and Job Recommendation System using NLP and Machine Learning**

---

# 2. Project Objective

Build an AI-based system that accepts a user's resume in PDF or DOCX format, analyzes the resume using Natural Language Processing (NLP), calculates an ATS-style resume score, compares the resume with job descriptions, predicts job suitability using Machine Learning, identifies missing skills, and recommends/ranks suitable jobs.

The system should be developed incrementally in clearly defined stages.

Do NOT attempt to build everything at once.

Complete and test each stage before moving to the next stage.

---

# 3. Main System Workflow

```text
                    USER
                      |
                      v
              Upload Resume
                PDF / DOCX
                      |
                      v
              Resume Parser
                      |
                      v
             Text Extraction
                      |
                      v
              NLP Processing
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
      Skills      Education     Experience
        |             |             |
        +-------------+-------------+
                      |
                      v
              Resume ATS Score
                      |
                      v
              Job Dataset
                      |
                      v
            Job Description NLP
                      |
          +-----------+-----------+
          |                       |
          v                       v
     TF-IDF Matching      Transformer Embeddings
          |                       |
          +-----------+-----------+
                      |
                      v
              Feature Engineering
                      |
                      v
             ML Suitability Model
                      |
                      v
          Suitable / Not Suitable
                      |
                      v
              Skill Gap Analysis
                      |
                      v
             Job Recommendation
                      |
                      v
               Ranked Jobs
                      |
                      v
             Streamlit Dashboard
```

---

# 4. Technology Stack

## Programming Language

* Python

## Frontend

* Streamlit

## Resume Parsing

* pypdf
* python-docx

## NLP

* Python regular expressions
* Text normalization
* Tokenization
* Keyword/skill extraction
* Optional spaCy
* Sentence Transformers

## Machine Learning

* scikit-learn
* Logistic Regression
* Random Forest
* Optional XGBoost if required

## Similarity

* TF-IDF
* Cosine Similarity
* Sentence Transformer embeddings

## Data Processing

* pandas
* NumPy

## Model Storage

* joblib

## Future Job API Integration

Use an appropriate legal/public job API or permitted job source.

Do not scrape websites that prohibit scraping.

---

# 5. Project Architecture

```text
resume_job_matcher/
│
├── app/
│   ├── main.py
│   │
│   ├── nlp/
│   │   ├── parser.py
│   │   ├── extractor.py
│   │   └── embeddings.py
│   │
│   ├── scoring/
│   │   └── resume_score.py
│   │
│   ├── jobs/
│   │   ├── repository.py
│   │   └── matcher.py
│   │
│   ├── ml/
│   │   ├── features.py
│   │   ├── train.py
│   │   └── predictor.py
│   │
│   └── database/
│       └── db.py
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── resumes/
│   ├── jobs/
│   └── training/
│
├── models/
│
├── scripts/
│
├── tests/
│
├── requirements.txt
├── README.md
└── PROJECT_ROADMAP.md
```

---

# 6. Development Rules

Antigravity must follow these rules:

1. Work stage-by-stage.
2. Do not skip stages.
3. Do not rewrite working components unnecessarily.
4. Preserve existing functionality when adding new features.
5. Test every stage before continuing.
6. Keep code modular.
7. Do not hard-code user-specific resume information.
8. Keep ML training code separate from prediction code.
9. Keep NLP processing separate from ML processing.
10. Explain important implementation decisions.
11. Use comments where they improve understanding.
12. Avoid unnecessary libraries.
13. Prefer simple implementations suitable for an academic mini-project.
14. The final system must be runnable locally on Windows.
15. Do not claim that rule-based ATS scoring is Machine Learning.
16. The ML contribution must include measurable model training and evaluation.

---

# 7. DEVELOPMENT STAGES

---

# STAGE 1 — Resume Upload and Text Extraction

## Objective

Allow the user to upload a PDF or DOCX resume and extract its text.

## Tasks

Implement:

* PDF upload
* DOCX upload
* PDF text extraction using pypdf
* DOCX text extraction using python-docx
* Error handling
* Raw extracted text display

## Files

```text
app/nlp/parser.py
frontend/app.py
```

## Expected Workflow

```text
Upload Resume
      ↓
Detect File Type
      ↓
Extract Text
      ↓
Display Text
```

## Deliverable

A working Streamlit page where a user can upload a resume and see the extracted text.

---

# STAGE 2 — NLP Resume Information Extraction

## Objective

Extract structured information from the resume.

## Information to extract

* Email
* Phone
* Skills
* Education
* Experience
* Projects
* Certifications
* Resume sections

## NLP operations

Implement:

* Text normalization
* Lowercasing
* Whitespace normalization
* Section detection
* Skill extraction
* Contact information extraction

Use a controlled technical skill dictionary initially.

Example:

```text
Python
Java
C++
SQL
Machine Learning
Deep Learning
NLP
Pandas
NumPy
TensorFlow
PyTorch
Docker
AWS
Git
React
Django
FastAPI
```

The skill dictionary can be expanded later.

## Files

```text
app/nlp/extractor.py
frontend/app.py
```

## Deliverable

Display structured resume information.

Example:

```text
Skills:
Python, SQL, Machine Learning, Pandas

Education:
B.Tech Computer Engineering

Experience:
Software Developer Intern

Projects:
AI Resume Analyzer
```

---

# STAGE 3 — ATS / Resume Scoring

## Objective

Calculate an ATS-style resume score from 0–100.

## Important

This stage is primarily RULE-BASED.

Do not describe this score itself as a trained ML model.

## Suggested scoring

```text
Contact Information     10
Skills                  25
Education               15
Experience              20
Projects                15
Certifications         10
Resume Content           5
--------------------------------
Total                  100
```

## Additional checks

Consider:

* Number of skills
* Presence of education
* Presence of experience
* Presence of projects
* Presence of certifications
* Email availability
* Phone availability
* Resume content length

## Files

```text
app/scoring/resume_score.py
frontend/app.py
```

## Deliverable

Display:

```text
Resume Score: 82/100
Category: Good
```

and a score breakdown.

---

# STAGE 4 — Job Dataset and Job Description Processing

## Objective

Introduce job descriptions into the system.

Initially use a local CSV dataset.

Do NOT depend on live APIs yet.

## Job dataset fields

```text
job_id
job_title
company
location
description
required_skills
experience_required
education_required
job_url
```

Example:

```text
1
Machine Learning Engineer
ABC Technologies
Mumbai
Develop ML models...
Python, Machine Learning, SQL, TensorFlow
2
B.Tech
```

## Tasks

* Create sample job dataset
* Load dataset using pandas
* Clean job descriptions
* Normalize job text
* Extract job skills
* Prepare jobs for matching

## Files

```text
app/jobs/repository.py
app/nlp/extractor.py
data/jobs/jobs.csv
```

## Deliverable

System can load and display available jobs.

---

# STAGE 5 — TF-IDF Resume–Job Matching

## Objective

Create the first mathematical resume-to-job matching system.

This is the BASELINE model.

## Process

```text
Resume Text
     ↓
TF-IDF Vectorization
     ↓
Resume Vector

Job Description
     ↓
TF-IDF Vectorization
     ↓
Job Vector

Resume Vector + Job Vector
     ↓
Cosine Similarity
     ↓
Similarity Score
```

## Use

```text
TfidfVectorizer
cosine_similarity
```

from scikit-learn.

## Output

Example:

```text
Machine Learning Engineer
Similarity: 0.78

Data Analyst
Similarity: 0.62

Java Developer
Similarity: 0.31
```

## Files

```text
app/jobs/matcher.py
```

## Deliverable

Rank jobs according to TF-IDF similarity.

---

# STAGE 6 — Sentence Transformer Semantic Matching

## Objective

Improve upon the TF-IDF baseline using semantic embeddings.

Use:

```text
sentence-transformers
```

Suggested initial model:

```text
all-MiniLM-L6-v2
```

## Process

```text
Resume
  ↓
Sentence Transformer
  ↓
Resume Embedding
  ↓
Compare
  ↑
Job Embedding
  ↑
Sentence Transformer
  ↑
Job Description
```

Calculate cosine similarity between embeddings.

## Why this is important

TF-IDF mainly focuses on word overlap.

Transformer embeddings can capture semantic relationships.

Example:

```text
Resume:
"Built predictive models using Python."

Job:
"Experience developing machine learning solutions."
```

Even though the exact words differ, semantic similarity may still be high.

## Files

```text
app/nlp/embeddings.py
app/jobs/matcher.py
```

## Deliverable

Compare:

```text
TF-IDF similarity
vs
Transformer semantic similarity
```

---

# STAGE 7 — Feature Engineering

## Objective

Create meaningful ML features from resume-job pairs.

Each resume/job pair becomes one training example.

## Features

At minimum include:

```text
semantic_similarity
tfidf_similarity
skill_match_ratio
missing_skill_ratio
experience_match
education_match
resume_score
```

Additional possible features:

```text
number_of_resume_skills
number_of_required_skills
keyword_overlap
resume_length
project_presence
certification_presence
```

## Example

```text
semantic_similarity = 0.82
tfidf_similarity = 0.71
skill_match_ratio = 0.75
missing_skill_ratio = 0.25
experience_match = 1
education_match = 1
resume_score = 84
```

These features become input to the ML model.

## Files

```text
app/ml/features.py
```

## Deliverable

Generate a structured training dataset.

---

# STAGE 8 — Train Machine Learning Suitability Model

## Objective

Train an actual supervised ML model to predict whether a job is suitable for a candidate.

## Target

Binary classification:

```text
1 = Suitable
0 = Not Suitable
```

## Candidate models

Start with:

### Model 1

Logistic Regression

Then compare with:

### Model 2

Random Forest

Optional:

### Model 3

XGBoost

Only add XGBoost if necessary.

## Training pipeline

```text
Training Dataset
       ↓
Feature Selection
       ↓
Train/Test Split
       ↓
Feature Scaling if required
       ↓
Train Model
       ↓
Save Model
```

## Model files

```text
models/
    suitability_model.pkl
```

## Training code

```text
app/ml/train.py
```

## Prediction code

```text
app/ml/predictor.py
```

## Deliverable

Given a resume-job pair:

```text
Suitability Probability: 87%
Prediction: Suitable
```

---

# STAGE 9 — Model Evaluation and Comparison

## Objective

Evaluate the trained ML models.

## Metrics

Use:

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix
* ROC-AUC if applicable

## Compare

At minimum:

```text
Logistic Regression
vs
Random Forest
```

Also compare the baseline:

```text
TF-IDF similarity
```

with:

```text
Transformer semantic similarity
```

## Example evaluation table

```text
Model                  Accuracy    Precision    Recall    F1
--------------------------------------------------------------
Logistic Regression      0.84        0.82       0.85    0.83
Random Forest            0.88        0.87       0.89    0.88
```

## Deliverable

Select the best model based on evaluation results.

---

# STAGE 10 — Skill Gap Analysis

## Objective

Identify skills that the candidate has and skills required by the job that are missing.

## Process

```text
Resume Skills
      +
Job Required Skills
      ↓
Compare
      ↓
Matched Skills
Missing Skills
```

Example:

```text
Resume Skills:
Python
SQL
Pandas
Machine Learning

Job Requirements:
Python
SQL
Machine Learning
AWS
Docker

Matched:
Python
SQL
Machine Learning

Missing:
AWS
Docker
```

## Deliverable

Display:

```text
✅ Matched Skills
❌ Missing Skills
```

This makes the system more useful than a simple ATS scorer.

---

# STAGE 11 — Job Recommendation and Ranking

## Objective

Combine all matching signals into a final job recommendation system.

Possible ranking signals:

```text
ML suitability probability
Semantic similarity
TF-IDF similarity
Skill match
Experience match
Education match
```

Recommended approach:

Use ML suitability probability as the primary ranking signal and use other scores as supporting information.

Example:

```text
Job                         Match
--------------------------------------
ML Engineer                 91%
Data Scientist              87%
Data Analyst                79%
Backend Developer           63%
```

For each job display:

```text
Job Title
Company
Location
Match %
Matched Skills
Missing Skills
Why it matches
```

## Files

```text
app/jobs/matcher.py
```

---

# STAGE 12 — Final Streamlit Dashboard

## Objective

Create the final user-friendly interface.

## Dashboard structure

### Section 1

Resume Upload

### Section 2

Resume Overview

```text
ATS Score
Skills
Education
Experience
Projects
Certifications
```

### Section 3

Resume Analysis

```text
Resume Score
Skill Count
Experience
Education
```

### Section 4

Job Recommendations

```text
Rank
Job
Company
Location
Match %
```

### Section 5

Job Details

Display:

```text
Matched Skills
Missing Skills
Semantic Similarity
Suitability Probability
```

### Section 6

Raw Data

Optional expandable sections for:

```text
Extracted Resume Text
Processed Job Description
```

---

# STAGE 13 — Live Job Fetching

## Objective

Replace or supplement the local job dataset with live job data.

Only implement this after the local recommendation system works correctly.

## Requirements

Use:

* Legal/public APIs
* Official APIs
* Permitted job feeds

Do not depend on prohibited scraping.

## Pipeline

```text
Live Job API
      ↓
Fetch Jobs
      ↓
Normalize Data
      ↓
NLP Processing
      ↓
Resume Matching
      ↓
ML Prediction
      ↓
Ranking
      ↓
Recommendations
```

## Important

The system should still work using the local dataset if the API is unavailable.

---

# STAGE 14 — Testing

## Objective

Test every major component.

## Unit tests

Test:

```text
PDF extraction
DOCX extraction
Email extraction
Phone extraction
Skill extraction
Section extraction
ATS scoring
TF-IDF matching
Embedding similarity
Feature generation
ML prediction
Skill gap analysis
Job ranking
```

## Example tests

```text
test_parser.py
test_extractor.py
test_scoring.py
test_matcher.py
test_features.py
test_predictor.py
```

## Error cases

Test:

* Empty resume
* Resume without email
* Resume without phone
* Resume without skills
* Resume with unusual formatting
* Invalid file
* Empty job description
* Job with no required skills

---

# STAGE 15 — Final Documentation, Report and Presentation

## Objective

Prepare the complete academic project documentation.

## Documentation should include

### 1. Introduction

Problem and motivation.

### 2. Problem Statement

Current resume screening challenges.

### 3. Objectives

What the system solves.

### 4. Literature / Existing System

Traditional ATS and resume screening.

### 5. Proposed System

Our NLP + ML architecture.

### 6. System Architecture

Complete pipeline diagram.

### 7. Technologies Used

Python, NLP, scikit-learn, Sentence Transformers, Streamlit, etc.

### 8. Methodology

Explain:

* Resume parsing
* NLP
* ATS scoring
* TF-IDF
* Cosine similarity
* Transformer embeddings
* Feature engineering
* Classification
* Evaluation
* Recommendation

### 9. Dataset

Explain job dataset and ML training dataset.

### 10. Model Training

Explain selected algorithms.

### 11. Evaluation

Include:

* Accuracy
* Precision
* Recall
* F1
* Confusion matrix

### 12. Results

Show sample resume analysis and job recommendations.

### 13. Limitations

Examples:

* Skill dictionary limitations
* Resume formatting differences
* Job dataset limitations
* API availability
* Synthetic training data if used

### 14. Future Scope

Examples:

* Better NER
* More advanced resume understanding
* Larger real-world dataset
* Personalized recommendations
* Multi-language resumes
* Explainable AI
* Better job APIs

### 15. Conclusion

Summarize the system.

---

# 8. MACHINE LEARNING COMPONENT

The project must clearly demonstrate Machine Learning.

The main ML pipeline should be:

```text
Resume + Job
       ↓
NLP Processing
       ↓
TF-IDF Similarity
       +
Transformer Similarity
       +
Skill Match
       +
Experience Match
       +
Education Match
       +
Resume Score
       ↓
Feature Vector
       ↓
ML Classifier
       ↓
Suitability Prediction
```

Example feature vector:

```text
[
    0.82,   # semantic similarity
    0.71,   # TF-IDF similarity
    0.75,   # skill match
    0.25,   # missing skill ratio
    1,      # experience match
    1,      # education match
    84      # resume score
]
```

Output:

```text
Suitable = 1
Probability = 0.87
```

---

# 9. NLP COMPONENT

NLP should be used for:

```text
Resume text extraction
       ↓
Text normalization
       ↓
Section detection
       ↓
Skill extraction
       ↓
Job description processing
       ↓
TF-IDF representation
       ↓
Transformer embeddings
       ↓
Semantic similarity
```

NLP is responsible for processing and representing text.

Machine Learning is responsible for learning suitability patterns from features.

---

# 10. ATS SCORE VS ML SCORE

Keep these separate.

## ATS Score

Rule-based:

```text
Resume completeness
Skills
Education
Experience
Projects
Certifications
Contact
```

Output:

```text
82/100
```

## ML Suitability Score

Learned from training data:

```text
Resume + Job Features
        ↓
ML Model
        ↓
87% suitable
```

The final dashboard may show both:

```text
Resume ATS Score: 82/100

Job Match:
Machine Learning Engineer — 91%

ML Suitability:
87%
```

---

# 11. DATASET STRATEGY

Initially use a local job dataset.

Example:

```text
data/jobs/jobs.csv
```

For supervised ML training, create a labeled resume-job pair dataset.

Example:

```text
semantic_similarity
tfidf_similarity
skill_match_ratio
missing_skill_ratio
experience_match
education_match
resume_score
label
```

Where:

```text
label = 1 → suitable
label = 0 → not suitable
```

The dataset should eventually be replaced or supplemented with a real, properly licensed dataset if available.

Do not present synthetic/generated data as real-world collected data.

---

# 12. MODEL COMPARISON

The project should demonstrate progression:

```text
Baseline
   ↓
TF-IDF + Cosine Similarity
   ↓
Improved NLP
   ↓
Sentence Transformer
   ↓
Feature Engineering
   ↓
Supervised ML
   ↓
Logistic Regression / Random Forest
```

This progression should be documented in the final report.

---

# 13. EXPECTED FINAL OUTPUT

The final application should allow a user to:

1. Upload a resume.
2. Extract resume text.
3. Analyze the resume.
4. Extract skills and other information.
5. Calculate ATS score.
6. Load/fetch jobs.
7. Compare resume with jobs.
8. Calculate semantic similarity.
9. Predict job suitability.
10. Identify missing skills.
11. Rank jobs.
12. Display recommended jobs.

Example final output:

```text
=========================================
RESUME ANALYSIS
=========================================

ATS SCORE
84 / 100

Skills:
Python
SQL
Machine Learning
Pandas
NumPy
Git

Education:
B.Tech Computer Engineering

Experience:
2 years

=========================================
JOB RECOMMENDATIONS
=========================================

1. Machine Learning Engineer
   Company: ABC Technologies
   Match: 91%

   Matched Skills:
   Python
   SQL
   Machine Learning
   Pandas

   Missing Skills:
   AWS
   Docker


2. Data Scientist
   Company: XYZ Analytics
   Match: 87%

   Matched Skills:
   Python
   Machine Learning
   SQL

   Missing Skills:
   TensorFlow
```

---

# 14. CURRENT DEVELOPMENT STATUS

The project must track development status.

```text
[✓] Stage 1 — Resume Upload + Text Extraction
[✓] Stage 2 — NLP Information Extraction
[✓] Stage 3 — ATS Resume Scoring

[ ] Stage 4 — Job Dataset
[ ] Stage 5 — TF-IDF Matching
[ ] Stage 6 — Transformer Semantic Matching
[ ] Stage 7 — Feature Engineering
[ ] Stage 8 — ML Suitability Model
[ ] Stage 9 — Model Evaluation
[ ] Stage 10 — Skill Gap Analysis
[ ] Stage 11 — Job Recommendation
[ ] Stage 12 — Final Dashboard
[ ] Stage 13 — Live Job API
[ ] Stage 14 — Testing
[ ] Stage 15 — Final Documentation
```

Update this section as development progresses.

---

# 15. IMPORTANT INSTRUCTION FOR ANTIGRAVITY

This file is the master project roadmap.

When instructed to work on a stage:

1. Read this roadmap.
2. Inspect the existing project files.
3. Identify what has already been implemented.
4. Implement ONLY the requested stage.
5. Preserve previous stages.
6. Run/test the implementation.
7. Fix errors before declaring the stage complete.
8. Explain:

   * What was implemented
   * Which files changed
   * How it works
   * How to run/test it
   * What the expected output is
9. Do not automatically implement future stages unless explicitly requested.
10. Keep the architecture compatible with all future stages.

---

# 16. FINAL PROJECT GOAL

The final project should demonstrate the integration of:

```text
NLP
 +
Information Extraction
 +
ATS Scoring
 +
TF-IDF
 +
Semantic Embeddings
 +
Feature Engineering
 +
Supervised Machine Learning
 +
Skill Gap Analysis
 +
Job Recommendation
```

The key academic contribution is:

**Using NLP and semantic representations to convert unstructured resumes and job descriptions into meaningful features, followed by supervised Machine Learning to predict job suitability and rank relevant opportunities.**
