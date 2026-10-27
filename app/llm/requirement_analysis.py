from typing import Dict
from app.llm.client import get_llm_client
from app.llm.prompts import JOB_EXTRACTION_SYSTEM_PROMPT, JOB_EXTRACTION_USER_PROMPT

class JobRequirementExtractor:
    """Uses LLM to convert unstructured job descriptions into structured JSON requirements."""
    
    def __init__(self, provider: str = "gemini"):
        self.llm = get_llm_client(provider)
        
    def extract_requirements(self, job_description: str) -> Dict:
        """
        Analyze unstructured job description text.
        
        Returns:
            A dictionary containing:
            - required_skills (list)
            - preferred_skills (list)
            - experience (str)
            - education (str)
            - responsibilities (list)
            - technologies (list)
        """
        if not job_description or not str(job_description).strip():
            return self._get_empty_structure()
            
        prompt = JOB_EXTRACTION_USER_PROMPT.format(job_description=job_description)
        
        # We expect a JSON object from the LLM based on the system instruction.
        response_json = self.llm.generate_json(
            prompt=prompt,
            system_instruction=JOB_EXTRACTION_SYSTEM_PROMPT
        )
        
        # Ensure it matches the expected schema
        if isinstance(response_json, dict) and not response_json.get("mock"):
            return {
                "required_skills": response_json.get("required_skills", []),
                "preferred_skills": response_json.get("preferred_skills", []),
                "experience": response_json.get("experience", ""),
                "education": response_json.get("education", ""),
                "responsibilities": response_json.get("responsibilities", []),
                "technologies": response_json.get("technologies", [])
            }
            
        return self._get_empty_structure()
        
    def _get_empty_structure(self) -> Dict:
        return {
            "required_skills": [],
            "preferred_skills": [],
            "experience": "",
            "education": "",
            "responsibilities": [],
            "technologies": []
        }
