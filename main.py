import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
from available_functions import available_functions
from call_function import call_function

args = sys.argv[1:]

if not args:
    print("Must provide Prompt")
    exit(1)
user_prompt = " ".join(args)
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]
system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents= messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
    )
except Exception as e:
    print(f"Error Encounter: {e}")
    exit()

function_call_result = call_function(response.function_calls[0])

function_call_responses  = []

if function_call_result.parts[0].function_response.response:
    function_call_responses.append(function_call_result.parts[0])
else:
    raise Exception("function_call_result doesn't return '.parts[0].function_response.response'")

if "--verbose" in args:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    if response.function_calls is not None:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(response.text)