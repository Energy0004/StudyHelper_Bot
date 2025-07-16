# list_models.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- Load Environment Variables ---
# This assumes the script is run from the project root where the .env file exists.
print("Loading environment variables from .env file...")
load_dotenv()

# --- Configure Gemini API ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("\nCRITICAL ERROR: GEMINI_API_KEY not found in your .env file.")
    print("Please ensure your .env file is in the same directory and contains the key.")
    exit(1)

try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("Gemini API configured successfully.")
except Exception as e:
    print(f"\nERROR: Failed to configure Gemini API. Please check if your key is valid. Details: {e}")
    exit(1)

# --- Model Listing Logic ---
print("\nFetching all available models from the Gemini API...")

try:
    # This set contains the models we want to exclude from the main list.
    # We add both the 'models/' prefixed name and the simple name for robustness.
    excluded_models = {
        "gemini-1.5-flash",
        "models/gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "models/gemini-1.5-flash-latest"
    }

    print("-" * 50)
    print("Available Models (excluding Gemini 1.5 Flash):\n")

    found_models = False
    for model in genai.list_models():
        # Check if the model's name is in our exclusion list.
        if model.name in excluded_models:
            print(f"(Skipping excluded model: {model.name})")
            continue

        # Check if the 'generateContent' method is supported by the model.
        # This is the most important check, as it filters out specialized models
        # like those for embedding, which can't be used for chat.
        if 'generateContent' in model.supported_generation_methods:
            found_models = True
            print(f"  Model Name: {model.name}")
            print(f"    - Display Name: {model.display_name}")
            print(f"    - Description: {model.description[:100]}...") # Print first 100 chars
            print(f"    - Input Token Limit: {model.input_token_limit}")
            print(f"    - Output Token Limit: {model.output_token_limit}\n")

    if not found_models:
        print("No other chat-capable models were found.")

    print("-" * 50)

except Exception as e:
    print(f"\nAn error occurred while fetching the model list: {e}")
    print("This could be due to a network issue or a problem with your API key permissions.")