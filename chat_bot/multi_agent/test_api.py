import os
from dotenv import load_dotenv
from config.models import get_openrouter_model, get_google_model

# Load environment variables
load_dotenv()

def test_connections():
    print("--- Starting API Connection Test ---")

    # 1. Test Google (Gemini)
    print("\n1. Testing Google (Gemini)...")
    try:
        gemini = get_google_model()
        # LiteLlm generate_content structure might vary slightly by version, 
        # but this is the standard call.
        response = gemini.generate_content("Hello, reply with 'Gemini Online'.")
        print(f"✅ Google Success: {response.text}")
    except Exception as e:
        print(f"❌ Google Failed: {e}")

    # 2. Test OpenRouter (OpenAI)
    print("\n2. Testing OpenRouter (GPT)...")
    try:
        openai = get_openrouter_model()
        response = openai.generate_content("Hello, reply with 'OpenRouter Online'.")
        print(f"✅ OpenRouter Success: {response.text}")
    except Exception as e:
        print(f"❌ OpenRouter Failed: {e}")

    print("\n--- Test Complete ---")

if __name__ == "__main__":
    test_connections()