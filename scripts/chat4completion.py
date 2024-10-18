import sys
import requests
import time


# Create a payload with the message to start the conversation
user_msg_template = """<suffix>{suffix}</suffix><prefix>{prefix}</prefix><middle/>"""

payload = {
    "messages": [
        {
            "role": "system",
            "content": '''You are coding assistant specialized in completing code given <suffix/> and <prefix/>. 
                When given surrounding code <suffix/> and <prefix/>, only return the <middle/> part of the code between 
                the <prefix/> and <suffix/> without any additional comments or explanations, DO NOT include existing code in <suffix/> or <prefix/>.
                Make sure the code is valid and complete after filling the <middle/> part.
                You only respond with the content in <middle/> without any formating.
                Don't miss "\n" in the end of a line, it's very important for the code to be valid.
                See examples below for reference.
                Example 1 (python):
                User: <suffix>     return area</suffix><prefix>def calculate_circle_area(radius): \n     pi = 3.14 \n     area = </prefix><middle/>
                Assistant: pi * radius * radius\n
                Example 2 (C#):
                User: <suffix>) \n     { \n         list.Add(str); \n     } \n }</suffix><prefix>static void AppendStringToList(List<string> list, string str) \n { \n     if (!string.</prefix><middle/>
                Assistant: IsNullOrEmpty(str)
                Example 3 (C#):
                User: <suffix>)\n { \n     if (!string.IsNullOrEmpty(str)) \n     { \n         list.Add(str); \n     } \n }</suffix><prefix>static void AppendStringToList(Li</prefix><middle/>
                Assistant: st<string> list, string str) 
                Example 4 (C#):
                User: <suffix>\n { \n     if (!string.IsNullOrEmpty(str)) \n     { \n         list.Add(str); \n     } \n }</suffix><prefix>static void AppendStringToList(List</prefix><middle/>
                Assistant: <string> list, string str) 
                Example 5 (C#):
                User: <suffix></suffix><prefix>static void AppendStringToList(List<</prefix><middle/>
                Assistant: string> list, string str) \n { \n     if (!string.IsNullOrEmpty(str)) \n     { \n         list.Add(str); \n     } \n }
                Example 6 (python):
                User: <suffix> in range(2, n + 1, 2): \n         print(i, end=' ')</suffix><prefix>def print_even_numbers(n): \n     for </prefix><middle/>
                Assistant: i
                '''
        },
        {
            "role": "user",
            "content": ""
        }
    ],

    "max_tokens": 1024,
    "temperature": 0.0,
    "stop": "<|endoftext|>"
}


def get_user_message(prefix, suffix):
    return user_msg_template.format(suffix=suffix, prefix=prefix)


def call_chat_api(model_url, api_key, prompt, suffix):

    # Set up the headers with the API key for authentication
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    message = get_user_message(prompt, suffix)
    payload["messages"][1]["content"] = message

    # Make the POST request to the Azure OpenAI Chat API
    response = requests.post(model_url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the generated text
        response_data = response.json()
        generated_message = response_data["choices"][0]["message"]["content"]

        return generated_message
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")
        return None


if __name__ == "__main__":
    start = time.perf_counter()
    prompt = "def calculate_circle_area(radius): \n     pi = 3.14 \n     area = "
    suffix = "return area"
    model_url = sys.argv[1]
    api_key = sys.argv[2]
    generated_message = call_chat_api(model_url, api_key, prompt, suffix)
    print(f"{generated_message}")
    print("Time elapsed: ", time.perf_counter() - start,  "seconds\n")
