import google.generativeai as genai
import os

GENAI_API_KEY = "AIzaSyC4v45ZtZk59Sa8ELtI0l9rGIop-2S2ACg"
genai.configure(api_key=GENAI_API_KEY)

print("Searching for a working model...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Trying model: {m.name}")
            try:
                model = genai.GenerativeModel(m.name)
                response = model.generate_content("Hi")
                print(f"SUCCESS! Working model found: {m.name}")
                break
            except Exception as e:
                print(f"Failed with {m.name}: {e}")
except Exception as e:
    print(f"Error listing models: {e}")
