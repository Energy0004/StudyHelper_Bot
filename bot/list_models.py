# save_this_as_list_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This is crucial if your API key is in a .env file
load_dotenv()

# Retrieve the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in environment.")
    print("Please ensure it's in your .env file and load_dotenv() is called,")
    print("or set it as an environment variable directly.")
    exit()

try:
    # Configure the genai library with your API key
    genai.configure(api_key=GEMINI_API_KEY)
    print("Successfully configured Gemini API key.")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    exit()

# --- List the Models ---
try:
    print("\nAvailable models that support 'generateContent':")
    count = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- Name: {m.name}")
            # You can print other details too if you want:
            # print(f"  Display Name: {m.display_name}")
            # print(f"  Description: {m.description}")
            # print(f"  Version: {m.version}")
            # print(f"  Supported Generation Methods: {m.supported_generation_methods}")
            # print("-" * 20)
            count += 1
    if count == 0:
        print("No models found that support 'generateContent'.")
        print("Check your API key permissions or try updating the SDK (`pip install --upgrade google-generativeai`).")

except Exception as e:
    print(f"\nAn error occurred while listing models: {e}")
    print("This could be due to an invalid API key, network issues, or API service problems.")