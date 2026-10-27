from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import uvicorn
import io
import os
import tempfile

from app.nlp.parser import extract_pdf_text, extract_docx_text
from app.nlp.extractor import extract_resume_information
from app.scoring.resume_score import calculate_resume_score
from app.jobs.matcher import JobMatcher
from app.reporting.pdf_generator import PDFGenerator
from app.scoring.resume_score import get_score_category
from pydantic import BaseModel
from fastapi.responses import Response

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ResumeAI Advanced API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock database of jobs for matching
MOCK_JOBS = [
    {
        "id": "J101",
        "title": "Senior Python Engineer",
        "description": "Looking for an experienced backend developer with strong Python and ML skills.",
        "required_skills": "Python, Django, Machine Learning, AWS, PostgreSQL",
        "experience_required": "5+ years",
        "education_required": "Bachelor's Degree in Computer Science"
    },
    {
        "id": "J102",
        "title": "Frontend React Developer",
        "description": "We need a UI expert who can build dynamic, beautiful interfaces.",
        "required_skills": "JavaScript, React, CSS, HTML, TypeScript",
        "experience_required": "3+ years",
        "education_required": "Any"
    },
    {
        "id": "J103",
        "title": "Data Scientist",
        "description": "Role focused on predictive modeling, NLP, and unstructured data extraction.",
        "required_skills": "Python, Pandas, Scikit-Learn, PyTorch, SQL",
        "experience_required": "2+ years",
        "education_required": "Master's Degree preferred"
    },
    {
        "id": "J104",
        "title": "DevOps Engineer",
        "description": "Manage infrastructure and deployment pipelines.",
        "required_skills": "AWS, Docker, Kubernetes, CI/CD, Terraform",
        "experience_required": "4+ years",
        "education_required": "Bachelor's Degree"
    },
    {
        "id": "J105",
        "title": "Full Stack Developer",
        "description": "Build end-to-end applications using modern web technologies.",
        "required_skills": "JavaScript, Node.js, React, Express, MongoDB",
        "experience_required": "3+ years",
        "education_required": "Bachelor's Degree"
    },
    {
        "id": "J106",
        "title": "Machine Learning Engineer",
        "description": "Deploy machine learning models at scale.",
        "required_skills": "Python, TensorFlow, AWS, C++, Docker",
        "experience_required": "4+ years",
        "education_required": "Master's Degree"
    },
    {
        "id": "J107",
        "title": "Backend Go Developer",
        "description": "High performance microservices architecture.",
        "required_skills": "Go, gRPC, PostgreSQL, Redis, Docker",
        "experience_required": "3+ years",
        "education_required": "Bachelor's Degree"
    },
    {
        "id": "J108",
        "title": "Cloud Architect",
        "description": "Design scalable cloud infrastructure.",
        "required_skills": "AWS, Azure, System Design, Terraform, Networking",
        "experience_required": "8+ years",
        "education_required": "Bachelor's Degree"
    },
    {
        "id": "J109",
        "title": "Mobile App Developer",
        "description": "Build cross-platform mobile apps.",
        "required_skills": "React Native, Swift, Kotlin, Firebase",
        "experience_required": "2+ years",
        "education_required": "Any"
    },
    {
        "id": "J110",
        "title": "AI Researcher",
        "description": "Research cutting edge foundational models.",
        "required_skills": "Python, PyTorch, Deep Learning, NLP, Mathematics",
        "experience_required": "5+ years",
        "education_required": "Ph.D. preferred"
    }
]

@app.post("/api/v1/match")
async def match_resume(file: UploadFile = File(...), top_n: int = 3):
    """
    Endpoint that takes a PDF or DOCX resume, parses it, extracts ML features,
    and returns ranked job matches with SHAP explainability insights.
    """
    filename = file.filename.lower()
    if not (filename.endswith('.pdf') or filename.endswith('.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
        
    try:
        content = await file.read()
        
        # Parse text based on format
        if filename.endswith('.pdf'):
            # Save to temporary file since PyPDF2 requires file path/stream
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
                temp.write(content)
                temp_path = temp.name
            try:
                resume_text = extract_pdf_text(temp_path)
            finally:
                os.unlink(temp_path)
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp:
                temp.write(content)
                temp_path = temp.name
            try:
                resume_text = extract_docx_text(temp_path)
            finally:
                os.unlink(temp_path)
                
        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(status_code=400, detail="Could not extract sufficient text from the document.")
            
        # Standard Pipeline
        resume_info = extract_resume_information(resume_text)
        ats_score, missing = calculate_resume_score(resume_info, resume_text)
        
        # Rank Jobs
        matcher = JobMatcher()
        ranked_jobs = matcher.rank_jobs_with_ml(
            resume_text=resume_text,
            resume_info=resume_info,
            ats_score=ats_score,
            jobs=MOCK_JOBS
        )
        
        # Extract top N and compute missing skills
        top_jobs = ranked_jobs[:top_n]
        resume_skills_lower = [s.lower() for s in resume_info.get("skills", [])]
        
        for job in top_jobs:
            req_skills = [s.strip() for s in job.get("required_skills", "").split(",")]
            missing_skills = [s for s in req_skills if s.lower() not in resume_skills_lower]
            job["missing_skills"] = missing_skills
        
        return {
            "status": "success",
            "ats_score": ats_score,
            "ats_breakdown": missing,
            "resume_extracted_data": resume_info,
            "matches": top_jobs
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ReportRequest(BaseModel):
    resume_info: dict
    ats_score: int
    ats_breakdown: dict
    matches: list

@app.post("/api/v1/report")
async def generate_pdf_report(req: ReportRequest):
    try:
        generator = PDFGenerator()
        
        pdf_bytes = generator.generate_report(
            req.resume_info,
            req.ats_score,
            req.matches
        )
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=ResumeAI_Report.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
