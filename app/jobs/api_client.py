import requests

class RemotiveClient:
    """Client for fetching live remote software dev jobs from the Remotive API."""
    
    def __init__(self):
        self.base_url = "https://remotive.com/api/remote-jobs"

    def fetch_jobs(self, limit=15):
        """Fetches jobs and formats them to match our system's expected schema."""
        url = f"{self.base_url}?category=software-dev&limit={limit}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            api_jobs = data.get("jobs", [])
            
            formatted_jobs = []
            for job in api_jobs:
                # Format to exactly match the dictionary structure from jobs.csv
                formatted_job = {
                    "job_id": str(job.get("id")),
                    "job_title": job.get("title", "Software Engineer"),
                    "company": job.get("company_name", "Unknown Company"),
                    "location": job.get("candidate_required_location", "Remote"),
                    "description": job.get("description", ""),
                    # Convert list of tags to a comma-separated string
                    "required_skills": ",".join(job.get("tags", [])), 
                    "experience_required": "",
                    "education_required": "",
                    "job_url": job.get("url", "")
                }
                formatted_jobs.append(formatted_job)
                
            return formatted_jobs
            
        except Exception as e:
            print(f"Error fetching live jobs: {e}")
            return []

import os

class IndianApiClient:
    """Client for fetching live local Indian jobs from the IndianAPI."""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("INDIAN_API_KEY")
        if not self.api_key or self.api_key == "your_api_key_here":
            raise ValueError("INDIAN_API_KEY is not set. Please update your .env file.")
        self.base_url = "https://jobs.indianapi.in/jobs"
        
    def fetch_jobs(self, what="software", limit=15):
        """Fetches jobs and extracts skills on-the-fly using NLP."""
        url = f"{self.base_url}?q={what}"
        
        try:
            headers = {"X-Api-Key": self.api_key}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            # Handle potential dict wrappers (usually a list or wrapped in 'jobs'/'results')
            api_jobs = data if isinstance(data, list) else data.get("jobs", data.get("results", []))
            
            from app.nlp.extractor import extract_skills
            
            formatted_jobs = []
            for idx, job in enumerate(api_jobs[:limit]):
                description = job.get("description", "")
                title = job.get("title", job.get("job_title", "Software Engineer"))
                
                # Extract skills dynamically from description/title
                skills_list = extract_skills(description) if description else extract_skills(title)
                
                formatted_job = {
                    "job_id": str(job.get("id", idx)),
                    "job_title": title,
                    "company": job.get("company_name", job.get("company", "Unknown Company")),
                    "location": job.get("location", "India"),
                    "description": description,
                    "required_skills": ",".join(skills_list), 
                    "experience_required": "",
                    "education_required": "",
                    "job_url": job.get("url", job.get("job_link", ""))
                }
                formatted_jobs.append(formatted_job)
                
            return formatted_jobs
            
        except Exception as e:
            print(f"Error fetching live Indian jobs: {e}")
            return []
