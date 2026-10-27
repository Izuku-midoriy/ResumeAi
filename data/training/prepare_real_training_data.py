import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from app.nlp.extractor import extract_resume_information, extract_skills
from app.scoring.resume_score import calculate_resume_score
from app.nlp.embeddings import SemanticEmbedder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def _clean_text(text):
    if not text or not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def calculate_tfidf(resume_text, job_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    corpus = [_clean_text(resume_text), _clean_text(job_text)]
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2]).flatten()[0]
        return float(similarity)
    except:
        return 0.0

def calculate_skill_match_ratios(resume_skills, job_skills):
    resume_skills_lower = [s.lower() for s in resume_skills]
    job_skills_lower = [s.lower() for s in job_skills]
    
    matched = sum(1 for skill in job_skills_lower if skill in resume_skills_lower)
    total_required = len(job_skills_lower)
    
    if total_required == 0:
        return 1.0, 0.0, matched, 0
        
    skill_match_ratio = matched / total_required
    missing_skill_ratio = (total_required - matched) / total_required
    missing_skill_count = total_required - matched
    
    return skill_match_ratio, missing_skill_ratio, matched, missing_skill_count

def calculate_experience_match(resume_experience, job_experience_required):
    if not job_experience_required:
        return 1
    if resume_experience and len(resume_experience.strip()) > 10:
        return 1
    return 0

def calculate_education_match(resume_education, job_education_required):
    if not job_education_required:
        return 1
    if resume_education and len(resume_education.strip()) > 10:
        return 1
    return 0

def prepare_data():
    print("Downloading / Loading dataset from Hugging Face...")
    dataset = load_dataset("cnamuangtoun/resume-job-description-fit")
    
    # Assuming the data is in 'train' split
    df = pd.DataFrame(dataset['train'])
    print(f"Initial dataset size: {len(df)}")
    
    # Clean data
    df = df.dropna(subset=['resume_text', 'job_description_text', 'label'])
    df = df.drop_duplicates(subset=['resume_text', 'job_description_text'])
    print(f"Dataset size after dropping NaNs and exact duplicates: {len(df)}")
    
    print("Label distribution:")
    print(df['label'].value_counts())
    
    # Resume-level split to prevent data leakage
    unique_resumes = df['resume_text'].unique().tolist()
    print(f"Number of unique resumes: {len(unique_resumes)}")
    
    # Split unique resumes into train (70%), val (15%), test (15%)
    resumes_train, resumes_temp = train_test_split(unique_resumes, test_size=0.30, random_state=42)
    resumes_val, resumes_test = train_test_split(resumes_temp, test_size=0.50, random_state=42)
    
    print(f"Resumes in train: {len(resumes_train)}, val: {len(resumes_val)}, test: {len(resumes_test)}")
    
    # Verify no overlap
    assert len(set(resumes_train).intersection(set(resumes_val))) == 0
    assert len(set(resumes_train).intersection(set(resumes_test))) == 0
    assert len(set(resumes_val).intersection(set(resumes_test))) == 0
    print("Verified ZERO resume overlap between train/validation/test.")
    
    df_train = df[df['resume_text'].isin(resumes_train)].copy()
    df_val = df[df['resume_text'].isin(resumes_val)].copy()
    df_test = df[df['resume_text'].isin(resumes_test)].copy()
    
    print(f"Rows in train: {len(df_train)}, val: {len(df_val)}, test: {len(df_test)}")
    
    # Initialize embedder once to save time
    # Initialize embedder once to save time
    print("Initializing SemanticEmbedder and FeatureExtractor...")
    embedder = SemanticEmbedder()
    from app.ml.features import FeatureExtractor
    feature_extractor = FeatureExtractor()
    
    def extract_features_for_df(data_split, split_name):
        print(f"Extracting features for {split_name} set ({len(data_split)} rows)...")
        features_list = []
        
        for _, row in tqdm(data_split.iterrows(), total=len(data_split)):
            resume_text = row['resume_text']
            job_text = row['job_description_text']
            label = row['label']
            
            # Extract resume information
            resume_info = extract_resume_information(resume_text)
            ats_score, _ = calculate_resume_score(resume_info, resume_text)
            
            # Extract job skills
            job_skills = extract_skills(job_text)
            
            # Prepare job_info proxy for the extractor
            job_info = {
                "required_skills": job_skills,
                "experience_required": job_text,
                "education_required": job_text
            }
            
            # Similarities
            tfidf_sim = calculate_tfidf(resume_text, job_text)
            
            try:
                res_vec = embedder.get_embedding(_clean_text(resume_text))
                job_vec = embedder.get_embedding(_clean_text(job_text))
                semantic_sim = float(embedder.calculate_similarity(res_vec, job_vec))
            except:
                semantic_sim = 0.0
                
            # Create feature vector using the unified FeatureExtractor (13 features)
            vector = feature_extractor.create_feature_vector(
                resume_info=resume_info, 
                job_info=job_info, 
                ats_score=ats_score, 
                semantic_similarity=semantic_sim, 
                tfidf_similarity=tfidf_sim
            )
            
            feature_dict = {
                "semantic_similarity": vector[0],
                "tfidf_similarity": vector[1],
                "skill_match_ratio": vector[2],
                "missing_skill_ratio": vector[3],
                "matched_skill_count": vector[4],
                "missing_skill_count": vector[5],
                "experience_match": vector[6],
                "education_match": vector[7],
                "resume_score": vector[8],
                "project_count": vector[9] if len(vector) > 9 else 0.0,
                "certification_count": vector[10] if len(vector) > 10 else 0.0,
                "resume_completeness": vector[11] if len(vector) > 11 else 0.0,
                "inferred_skill_match": vector[12] if len(vector) > 12 else 0.0,
                "label": label
            }
            features_list.append(feature_dict)
            
        return pd.DataFrame(features_list)
        
    train_features = extract_features_for_df(df_train, "Train")
    val_features = extract_features_for_df(df_val, "Validation")
    test_features = extract_features_for_df(df_test, "Test")
    
    # Save features
    output_dir = project_root / "data" / "training"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    train_features.to_csv(output_dir / "train_features.csv", index=False)
    val_features.to_csv(output_dir / "val_features.csv", index=False)
    test_features.to_csv(output_dir / "test_features.csv", index=False)
    
    print("Dataset processing complete and features saved to data/training/")

if __name__ == "__main__":
    prepare_data()
