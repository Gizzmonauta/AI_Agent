import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    # Set up argument parser. The argument parser should accept a user prompt and a verbose flag.
    parser = argparse.ArgumentParser(description="Generate content using Gemini API")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the Gemini API")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Prepare the messages. This is where we add the user prompt to the messages list.
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # We call the API in a loop for 20 iterations to generate agent feedback.
    for _ in range(20):
        # Call the Gemini API to generate content
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
        )

        # Verify usage_metadata is not None
        if response.usage_metadata is None:
            raise RuntimeError("Failed to retrieve usage metadata from the API response")
        
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        
        if args.verbose:

            # Print the user prompt
            print(f"User prompt: {args.user_prompt}")
            
            # Print token counts
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        if response.function_calls is not None:
            function_results = []
            # Print function call details
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)
                if not function_call_result.parts:
                    raise Exception("Function call result has no parts.")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Function response is None.")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Function response content is None.")
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=function_results))                
                    
        else:
            # Print the response
            print("Response:")
            print(response.text)
            break

    else:
        print("Maximum iterations reached without a final response from the model.")
        exit(1)

if __name__ == "__main__":
    main()
