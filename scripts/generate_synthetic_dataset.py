import os
import sys
import pandas as pd
import random
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from app.ml.features import FeatureExtractor

def generate_synthetic_dataset(num_samples=200):
    """
    Generates a synthetic dataset of resume-job feature vectors and labels 
    to train the ML model in Stage 8.
    """
    extractor = FeatureExtractor()
    
    dataset = []
    
    # 1. Generate "Suitable" matches (Label = 1)
    for _ in range(num_samples // 2):
        # Strong candidates typically have high scores
        semantic_sim = random.uniform(0.65, 0.95)
        tfidf_sim = random.uniform(0.50, 0.85)
        skill_match = random.uniform(0.70, 1.0)
        missing_skill = 1.0 - skill_match
        exp_match = random.choices([1.0, 0.0], weights=[0.9, 0.1])[0]
        edu_match = random.choices([1.0, 0.0], weights=[0.95, 0.05])[0]
        ats_score = random.uniform(70.0, 98.0)
        
        feature_vector = [
            semantic_sim, tfidf_sim, skill_match, missing_skill, 
            exp_match, edu_match, ats_score
        ]
        
        # Add label
        feature_vector.append(1)
        dataset.append(feature_vector)
        
    # 2. Generate "Not Suitable" matches (Label = 0)
    for _ in range(num_samples // 2):
        # Weak candidates typically have lower scores
        semantic_sim = random.uniform(0.10, 0.55)
        tfidf_sim = random.uniform(0.05, 0.45)
        skill_match = random.uniform(0.0, 0.50)
        missing_skill = 1.0 - skill_match
        exp_match = random.choices([1.0, 0.0], weights=[0.4, 0.6])[0]
        edu_match = random.choices([1.0, 0.0], weights=[0.7, 0.3])[0]
        ats_score = random.uniform(30.0, 65.0)
        
        feature_vector = [
            semantic_sim, tfidf_sim, skill_match, missing_skill, 
            exp_match, edu_match, ats_score
        ]
        
        # Add label
        feature_vector.append(0)
        dataset.append(feature_vector)
        
    # Shuffle the dataset
    random.shuffle(dataset)
    
    # Create DataFrame
    columns = [
        "semantic_similarity", "tfidf_similarity", "skill_match_ratio", 
        "missing_skill_ratio", "experience_match", "education_match", 
        "resume_score", "label"
    ]
    df = pd.DataFrame(dataset, columns=columns)
    
    # Save to CSV
    output_dir = project_root / "data" / "training"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / "dataset.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✅ Successfully generated {num_samples} synthetic training samples at {output_path}")

if __name__ == "__main__":
    generate_synthetic_dataset(300)
