import requests

url = "https://jobs.indianapi.in/jobs?q=software"
headers = {"X-Api-Key": "dummy"}
try:
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(response.text[:500])
except Exception as e:
    print(f"Error: {e}")
