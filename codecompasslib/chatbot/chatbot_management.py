"""
Functions focusing on handling the initialization and management of the chatbot assistant, including thread management and message handling.
"""
import json
import time
import requests
from openai import OpenAI
from typing import Tuple, Any, Union, Dict, Callable
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads.run import Run
from codecompasslib.chatbot.repo_info import get_repo_structure, get_repo_content, get_repo_branches, get_commit_history, search_repo_code, search_repo_commits, find_repos


def load_tools(file_path: str) -> list:
    """
    Loads tool definitions from a JSON file.

    :param file_path: The path to the JSON file containing the tools definition.
    :return: A list of tool definitions.
    """
    with open(file_path, 'r') as file:
        tools = json.load(file)
    return tools

def initialize_client(api_key: str) -> OpenAI:
    """
    Initializes the OpenAI client with the given API key.

    :param api_key: The API key for authenticating requests to OpenAI.
    :return: An instance of the OpenAI client.
    """
    client = OpenAI(api_key=api_key)
    return client

def create_assistant(client: OpenAI, name: str, instructions: str, model: str, tools: list) -> Assistant:
    """
    Creates an assistant with the specified parameters using the provided OpenAI client.

    :param client: The OpenAI client instance.
    :param name: The name of the assistant.
    :param instructions: The instructions for the assistant.
    :param model: The model to be used by the assistant.
    :param tools: The tools to be enabled for the assistant.
    :return: The created assistant object.
    """
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        model=model,
        tools=tools
    )
    #print(assistant)
    return assistant

def retrieve_assistant(client: OpenAI, assistant_id: str) -> Assistant:
    """
    Retrieves an existing assistant by its ID using the provided OpenAI client.

    :param client: The OpenAI client instance.
    :param assistant_id: The ID of the assistant to retrieve.
    :return: The retrieved assistant object.
    """
    current_assistant = client.beta.assistants.retrieve(assistant_id)
    #print(current_assistant)
    return current_assistant

def create_message_and_run(client: OpenAI, assistant: Assistant, query: str, thread: Thread = None) -> Tuple[Run, Thread]:
    """
    Creates a message and initiates a run for a given query within a thread. If no thread is provided, a new one is created.

    :param assistant: The Assistant object to use for creating the run.
    :param query: The user's query to send to the assistant.
    :param thread: Optional; The thread object to continue the conversation. A new thread is created if not provided.
    :return: A tuple containing the Run object that was created and the Thread object used or created.
    """
    # Create a new thread if not provided
    if not thread: 
        thread = client.beta.threads.create()

    # Create a message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=query
    )
    # Create a run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    return run, thread

def get_function_details(run: Run) -> Tuple[str, Any, str]:
    """
    Extracts and prints details about the function to be called based on the run's required action.

    :param run: The Run object containing details about the required action.
    :return: A tuple containing the function name to be called, its arguments, and the function call's ID.
    """
    print("\nRun Action Required")  # Placeholder for actual run.required_action

    function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
    arguments = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
    function_id = run.required_action.submit_tool_outputs.tool_calls[0].id

    print(f"Function Called: {function_name} with arguments: {arguments}")

    return function_name, arguments, function_id

def get_llama_details(function_output : list) -> Tuple[str, Any, str]:
    """
    Extracts and prints details about the function to be called based on the run's required action.

    :param run: The Run object containing details about the required action.
    :return: A tuple containing the function name to be called, its arguments, and the function call's ID.
    """
    print("\nRun Action Required")  # Placeholder for actual run.required_action

    function_name = function_output[0]
    arguments = function_output[1]
    function_id = function_output[2]

    print(f"Function Called: {function_name} with arguments: {arguments}")

    return function_name, arguments, function_id
    

# Utility function to submit the function response

def submit_tool_outputs(client: OpenAI, run: Run, thread: Thread, function_id: str, function_response: Any) -> Run:
    """
    Submits the output of a tool function call as part of the conversation with an assistant.

    :param run: The Run object representing the current assistant's run.
    :param thread: The Thread object where the conversation is taking place.
    :param function_id: The identifier of the function call within the assistant's run.
    :param function_response: The response from the function call to be submitted.
    :return: An updated Run object after submitting the tool outputs.
    """
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=[
            {
                "tool_call_id": function_id,
                "output": str(function_response),
            }
        ]
    )
    return run

def create_function_executor() -> Dict[str, Callable]:
    """
    Creates and returns a dictionary of available functions that can be executed 
    by the assistant.

    :return: A dictionary with function names as keys and callable Python functions as values.
    """
    available_functions = {
        "get_repo_structure": get_repo_structure,
        "get_repo_content": get_repo_content,
        "get_repo_branches": get_repo_branches,
        "get_commit_history": get_commit_history,
        "search_repo_code": search_repo_code,
        "search_repo_commits": search_repo_commits,
        "find_repos": find_repos
    }
    return available_functions

def execute_function_call(function_name: str, arguments: str) -> Union[Dict[str, Any], str]:
    """
    Executes a named function with provided JSON-formatted string arguments.

    :param function_name: The name of the function to be executed.
    :param arguments: A JSON-formatted string representing the arguments for the function.
    :return: The result of the function execution, which could be a dictionary or an error message.
    """
    available_functions = create_function_executor()
    function = available_functions.get(function_name, None)
    if function:
        arguments = json.loads(arguments)
        results = function(**arguments)
    else:
        results = f"Error: function {function_name} does not exist"
    return results

def create_new_thread(client: OpenAI) -> str:
    """
    Creates a new thread using the OpenAI client.

    :param client: The OpenAI client instance.
    :return: The ID of the newly created thread.
    """
    thread = client.beta.threads.create()
    print(f"New thread created with ID: {thread.id}")
    return thread.id

def load_thread(client: OpenAI, thread_id: str) -> dict:
    """
    Loads an existing thread by its ID.

    :param client: The OpenAI client instance.
    :param thread_id: The ID of the thread to load.
    :return: The thread object.
    """
    thread = client.beta.threads.retrieve(thread_id)
    print(f"Thread {thread_id} loaded successfully.")
    return thread


def run_chatbot(client: OpenAI, assistant: Assistant, thread_id: str = None):
    """
    Runs the main chatbot loop, allowing user interaction with the assistant.

    :param client: The OpenAI client instance.
    :param assistant: The Assistant object to use.
    :param thread_id: Optional; the ID of an existing thread to continue the conversation from.
    """
    if thread_id:
        thread = load_thread(client, thread_id)  # Load an existing thread if an ID is provided
    else:
        thread_id = create_new_thread(client)  # Create a new thread otherwise
        thread = load_thread(client, thread_id)  # Load the newly created thread for consistency

    while True:
        user_input = input("Please enter your query or type 'STOP' to exit: ")
        if user_input.lower() == "stop":
            break

        run, _ = create_message_and_run(client, assistant=assistant, query=user_input, thread=thread)

        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print("run status", run.status)

            # Check if the run requires action and execute the function call if so
            if run.status == "requires_action":
                function_name, arguments, function_id = get_function_details(run)
                function_response = execute_function_call(function_name, arguments)
                run = submit_tool_outputs(client, run, thread, function_id, function_response)
                continue
            
            # Check if the run is completed and display the assistant's response
            if run.status == "completed":
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                latest_message = messages.data[0]
                text = latest_message.content[0].text.value
                print(f'User: {user_input}')
                print(f'Assistant: {text}')
                break

            time.sleep(1)
            
        try:
            run, _ = create_message_and_run(client, assistant=assistant, query=user_input, thread=thread)

            while True:
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                print("run status", run.status)

                if run.status == "requires_action":
                    try:
                        function_name, arguments, function_id = get_function_details(run)
                        function_response = execute_function_call(function_name, arguments)
                        run = submit_tool_outputs(client, run, thread, function_id, function_response)
                    except Exception as e:
                        print("An error occurred while processing the request. Please try again.")
                        break  # Break out of the inner loop to prompt for a new user input

                if run.status == "completed":
                    messages = client.beta.threads.messages.list(thread_id=thread.id)
                    latest_message = messages.data[0]
                    text = latest_message.content[0].text.value
                    print(f'Assistant: {text}')
                    break  # Break out of the inner loop to prompt for a new user input

                time.sleep(1) 
        
        except Exception as e:
            print("An unexpected error occurred. Let's try another question.")
            # Here, you simply print an error message and continue to the next iteration of the loop
