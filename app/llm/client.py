import os
import json
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()

class LLMClient(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate_text(self, prompt: str, system_instruction: str = None) -> str:
        pass

    @abstractmethod
    def generate_json(self, prompt: str, system_instruction: str = None) -> dict:
        pass

class GeminiClient(LLMClient):
    """Gemini API client using google.genai (if installed) or fallback mock."""
    
    def __init__(self, model_name=None, api_key=None):
        self.model_name = model_name or os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        
        try:
            from google import genai
            if self.api_key:
                self.client = genai.Client(api_key=self.api_key)
            else:
                self.client = None
                print("Info: GEMINI_API_KEY not set. GeminiClient will run in mock mode.")
        except ImportError:
            self.client = None
            print("Warning: google-genai package not found. GeminiClient will run in mock mode.")

    def generate_text(self, prompt: str, system_instruction: str = None) -> str:
        if not self.client:
            return "Mock response: LLM client is missing API key or package."
            
        from google import genai
        config = genai.types.GenerateContentConfig(
            temperature=0.2
        )
        if system_instruction:
            config.system_instruction = system_instruction
            
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config,
        )
        return response.text

    def generate_json(self, prompt: str, system_instruction: str = None) -> dict:
        if not self.client:
            return {"mock": True, "message": "LLM client not configured properly."}
            
        from google import genai
        config = genai.types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json"
        )
        if system_instruction:
            config.system_instruction = system_instruction
            
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config,
        )
        try:
            raw_text = (response.text or "").strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            return json.loads(raw_text.strip())
        except Exception as e:
            print(f"Failed to parse JSON response: {e}")
            return {}

def get_llm_client(provider="gemini", **kwargs) -> LLMClient:
    """Factory function to get the configured LLM client."""
    if provider.lower() == "gemini":
        return GeminiClient(**kwargs)
    
    raise ValueError(f"Unsupported LLM provider: {provider}")
