from app.ml.features import FeatureExtractor

def test_advanced_features():
    extractor = FeatureExtractor()
    resume_info = {
        "skills": ["python", "django"],
        "inferred_skills": [{"name": "aws", "confidence": 0.9}],
        "projects": "- built an API\n- deployed to cloud",
        "certifications": "- AWS Certified",
        "email": "test@test.com"
    }
    job_info = {
        "required_skills": "python, aws, react"
    }
    
    print("Testing advanced feature extraction...")
    vector = extractor.create_feature_vector(resume_info, job_info, 80, 0.85, 0.6)
    
    print(f"Generated Vector Length: {len(vector)}")
    print(f"Vector values: {vector}")

if __name__ == "__main__":
    test_advanced_features()
