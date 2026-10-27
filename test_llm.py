from app.llm.client import get_llm_client

def test_client():
    client = get_llm_client("gemini")
    print(f"Client model: {client.model_name}")
    print(f"Client instance: {client}")
    # Run in mock mode
    print("Mock response:", client.generate_text("Hello"))

if __name__ == "__main__":
    test_client()
