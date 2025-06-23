import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) <= 1:
    print("No prompt provided")
    sys.exit(1)
str_prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=str_prompt)]),
]
agent_response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=str_prompt,
)
print(agent_response.text)

if "--verbose" in sys.argv:
    print(f"User prompt: {str_prompt}")
    print(
        f"Prompt tokens: {agent_response.usage_metadata.prompt_token_count}\nResponse tokens: {agent_response.usage_metadata.candidates_token_count}"
    )
