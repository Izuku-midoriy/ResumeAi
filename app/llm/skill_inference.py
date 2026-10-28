from typing import List, Dict
from app.llm.client import get_llm_client
from app.llm.prompts import SKILL_INFERENCE_SYSTEM_PROMPT, SKILL_INFERENCE_USER_PROMPT

class SkillInferencer:
    """Uses LLM to infer contextual skills from resume text."""
    
    def __init__(self, provider: str = "gemini"):
        self.llm = get_llm_client(provider)
        
    def infer_skills(self, resume_text: str, explicit_skills: List[str]) -> List[Dict]:
        """
        Analyze resume text and explicitly found skills to infer missing implicit skills.
        
        Returns:
            A list of dictionaries, each containing:
            - name: (str)
            - source: "inferred"
            - confidence: (float)
            - evidence: (str)
        """
        if not resume_text or not str(resume_text).strip():
            return []
            
        explicit_skills_str = ", ".join(explicit_skills) if explicit_skills else "None"
        
        prompt = SKILL_INFERENCE_USER_PROMPT.format(
            explicit_skills=explicit_skills_str,
            resume_text=resume_text
        )
        
        # We expect a JSON array from the LLM based on the system instruction.
        response_json = self.llm.generate_json(
            prompt=prompt,
            system_instruction=SKILL_INFERENCE_SYSTEM_PROMPT
        )
        
        # Validate structure
        inferred_skills = []
        if isinstance(response_json, dict):
            for key in ["inferred_skills", "skills", "results", "data"]:
                if key in response_json and isinstance(response_json[key], list):
                    response_json = response_json[key]
                    break

        if isinstance(response_json, list):
            for item in response_json:
                if isinstance(item, dict) and "name" in item:
                    item["source"] = "inferred"  # Ensure source is correct
                    item.setdefault("confidence", 0.8)
                    item.setdefault("evidence", "")
                    inferred_skills.append(item)
                elif isinstance(item, str) and item.strip():
                    inferred_skills.append({
                        "name": item.strip(),
                        "source": "inferred",
                        "confidence": 0.8,
                        "evidence": "Inferred from resume context"
                    })
                    
        return inferred_skills
