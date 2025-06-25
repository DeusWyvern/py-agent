import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions

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
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)

if agent_response.function_calls:
    for function_call_part in agent_response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    print(agent_response.text)

if "--verbose" in sys.argv:
    print()
    print(
        f"User prompt: {str_prompt}",
        f"Prompt tokens: {agent_response.usage_metadata.prompt_token_count}",
        f"Response tokens: {agent_response.usage_metadata.candidates_token_count}",
    )
