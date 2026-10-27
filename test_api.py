import json
import os
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def create_dummy_pdf():
    # Create a basic PDF using reportlab to simulate an upload
    from reportlab.pdfgen import canvas
    pdf_path = "dummy_resume.pdf"
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 750, "John Doe")
    c.drawString(100, 730, "Email: john.doe@example.com")
    c.drawString(100, 710, "Skills: Python, Django, AWS, React")
    c.drawString(100, 690, "Experience: 5 years software engineer building scalable backend systems.")
    c.drawString(100, 670, "Education: Bachelor of Science in Computer Science.")
    c.save()
    return pdf_path

def test_match_endpoint():
    print("Generating dummy PDF...")
    pdf_path = create_dummy_pdf()
    
    print("Testing /api/v1/match endpoint...")
    try:
        with open(pdf_path, "rb") as f:
            response = client.post("/api/v1/match", files={"file": ("dummy_resume.pdf", f, "application/pdf")})
            
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"ATS Score: {data.get('ats_score')}")
            matches = data.get('matches', [])
            print(f"Number of Matches: {len(matches)}")
            
            if matches:
                top_match = matches[0]
                print("\nTop Match Details:")
                print(f"- Job Title: {top_match.get('title')}")
                print(f"- ML Prediction: {top_match.get('ml_prediction')}")
                print(f"- Explanation: {top_match.get('explanation')}")
                
            print("\nFull JSON Response Snippet (First 500 chars):")
            print(json.dumps(data, indent=2)[:500] + "...")
        else:
            print(f"Error: {response.text}")
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

if __name__ == "__main__":
    test_match_endpoint()
