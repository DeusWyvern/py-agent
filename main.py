import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    max_iterations = 20

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(1, max_iterations):
        generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    agent_response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if verbose:
        print(f"Prompt tokens: {agent_response.usage_metadata.prompt_token_count}")
        print(
            f"Response tokens: {agent_response.usage_metadata.candidates_token_count}"
        )

    if not agent_response.function_calls:
        return agent_response.text

    function_responses = []
    for function_call_part in agent_response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        call_function_result = call_function(function_call_part, verbose)
        if (
            not call_function_result.parts[0].function_response.response
            or not call_function_result.parts
        ):
            raise Exception("ERROR: empty function call result")
        elif verbose:
            print(
                f"-> {call_function_result.parts[0].function_response.response['result']}"
            )
        function_responses.append((call_function_result.parts[0]))

        if not function_responses:
            raise Exception("no function responses generate, exiting.")
        return function_responses


if __name__ == "__main__":
    main()
