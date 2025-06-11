import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
import argparse



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Check if the API key is available
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables.")
    sys.exit(1)

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description="Generate text using the Gemini API.")
parser.add_argument("prompt", type=str, help="Prompt for the AI model.")
parser.add_argument("--verbose", action="store_true", help="Include verbose output.")
args = parser.parse_args()

user_prompt = args.prompt
verbose_mode = args.verbose

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

try:
    if verbose_mode:
        print(f"User prompt: {user_prompt}")
    
    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    )

    print(response.text)

    if verbose_mode:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)