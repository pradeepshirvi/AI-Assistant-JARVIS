import google.generativeai as genai
import os

GENAI_API_KEY = "API KEY HERE"  # Replace with your actual API key or set it as an environment variable

genai.configure(api_key=GENAI_API_KEY)

MODEL_NAME = "gemini-1.5-flash"

print(f"Testing generation with model: {MODEL_NAME}")
try:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content("Hello, can you hear me?")
    print("Success! Response received:")
    print(response.text)
except Exception as e:
    print("\n--- ERROR DETAIL ---")
    print(f"Type: {type(e).__name__}")
    print(f"Message: {e}")
    print("--------------------")
