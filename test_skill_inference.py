from app.llm.skill_inference import SkillInferencer

def test_inference():
    inferencer = SkillInferencer()
    resume_text = "Developed a MERN application using Node.js, Express and a document-oriented database."
    explicit_skills = ["Node.js", "Express"]
    
    print("Testing skill inference...")
    inferred = inferencer.infer_skills(resume_text, explicit_skills)
    
    print("Inferred Skills:")
    for skill in inferred:
        print(skill)

if __name__ == "__main__":
    test_inference()
