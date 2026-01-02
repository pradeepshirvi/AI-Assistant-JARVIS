import google.generativeai as genai
import os

# Use the key the user provided (temporarily for testing)
GENAI_API_KEY = "AIzaSyC4v45ZtZk59Sa8ELtI0l9rGIop-2S2ACg"
genai.configure(api_key=GENAI_API_KEY)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")
