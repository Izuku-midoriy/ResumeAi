import json
from app.llm.requirement_analysis import JobRequirementExtractor

def test_extraction():
    extractor = JobRequirementExtractor()
    job_description = "We are looking for a Senior Software Engineer with 5+ years of experience in Python and Django. A Bachelor's degree is required. You will be responsible for building REST APIs and deploying to AWS."
    
    print("Testing job requirement extraction...")
    result = extractor.extract_requirements(job_description)
    
    print("Extracted Requirements:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_extraction()
