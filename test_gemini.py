
import google.generativeai as genai
import os
from dotenv import load_dotenv
import traceback

# Load env from backend/.env
env_path = os.path.join(os.getcwd(), 'backend', '.env')
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("ERROR: API Key not found!")
    exit(1)

genai.configure(api_key=api_key)

models_to_test = ['gemini-1.5-flash', 'gemini-1.5-pro']

for model_name in models_to_test:
    print(f"\nTesting model: {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, can you hear me?")
        print(f"SUCCESS with {model_name}!")
        print(f"Response: {response.text}")
    except Exception:
        print(f"FAILED with {model_name}:")
        traceback.print_exc()
