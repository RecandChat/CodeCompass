import sys
import os
import re

# Get the directory where the current file (app.py) is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory of the current directory
parent_dir = os.path.dirname(current_dir)

# Get the directory one level up from the parent directory
grandparent_dir = os.path.dirname(parent_dir)

# Add this directory to the Python path
sys.path.insert(0, grandparent_dir)

import time
import openai
import streamlit as st
from typing import Any
from openai import OpenAI
from openai.types.beta.threads.run import Run
from codecompasslib.chatbot.chatbot_management import initialize_client, get_function_details, execute_function_call
from codecompasslib.chatbot.secrets_manager import load_openai_key, load_github_token
from codecompasslib.chatbot.repo_info import (get_repo_structure, get_repo_content, 
                                              get_repo_branches, get_commit_history, 
                                              search_repo_code, search_repo_commits, find_repos)

# helper function to submit tool outputs

def submit_tool_outputs(client: OpenAI, run: Run, thread_id: str, function_id: str, function_response: Any) -> Run:

    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run.id,
        tool_outputs=[
            {
                "tool_call_id": function_id,
                "output": str(function_response),
            }
        ]
    )
    return run

# Function map for convenience
function_map = {
        "get_repo_structure": get_repo_structure,
        "get_repo_content": get_repo_content,
        "get_repo_branches": get_repo_branches,
        "get_commit_history": get_commit_history,
        "search_repo_code": search_repo_code,
        "search_repo_commits": search_repo_commits,
        "find_repos": find_repos
    }

# Function to process the user input and call the appropriate function

def process_function_call(user_input):
    # Function to extract a URL from the input text
    def extract_url(text):
        url_regex = r'https?://github\.com/[a-zA-Z0-9-]+/[a-zA-Z0-9-]+'
        match = re.search(url_regex, text)
        return match.group(0) if match else None

    # Extract URL from user input
    url = extract_url(user_input)

    # Match user input with specific functions
    if "structure of" in user_input and url:
        return function_map["get_repo_structure"](url=url)
    elif "content of" in user_input and url:
        file_paths = []  # Extract or define file paths based on your requirement
        return function_map["get_repo_content"](url=url, filePaths=file_paths)
    elif "branches of" in user_input and url:
        return function_map["get_repo_branches"](url=url)
    elif "commit history of" in user_input and url:
        file_path = None  # Extract or define file path if needed
        return function_map["get_commit_history"](url=url, filePath=file_path)
    elif "search code in" in user_input and url:
        search_keywords = []  # Extract search keywords from user input
        return function_map["search_repo_code"](url=url, searchKeywords=search_keywords)
    elif "search commits in" in user_input and url:
        search_keywords = []  # Extract search keywords from user input
        return function_map["search_repo_commits"](url=url, searchKeywords=search_keywords)
    elif "find repos with" in user_input:
        search_keywords = []  # Extract search keywords from user input
        return function_map["find_repos"](searchKeywords=search_keywords)
    else:
        return "Function not recognized or missing parameters."

# Loading secrets and initialize the client
openai.api_key = load_openai_key(file_path='./secrets/openAI_key')
github_token = load_github_token(file_path='./secrets/github_token')
assistant_id = "asst_cibfhJsvFEKbAo7EmaS34oQD" # GPT3.5 assistant
#assistant_id = "asst_lfVLtdNac9aVUvDIIlw5c1nY" # GPT4 assistant
client = initialize_client(openai.api_key)

# Streamlit app setup
st.set_page_config(page_title="CodeCompassBot", page_icon=":speech_balloon:")
st.title("CodeCompass Chatbot")

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

if st.button("Exit Chat"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state
    st.session_state.thread_id = None

if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-3.5-turbo" # GPT3.5 assistant
    #st.session_state.openai_model = "gpt-4-0125-preview" # GPT4 assistant (ONLY FOR DEMO USE)
if "messages" not in st.session_state:
    st.session_state.messages = []


if st.session_state.start_chat:
    if prompt := st.chat_input("Enter your query"):
        # Append user query to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Process function call first and check its output
        function_output = process_function_call(prompt)

        # Continue with sending the user's original input to OpenAI
        response = client.beta.threads.messages.create(thread_id=st.session_state.thread_id, role="user", content=prompt)

        run = client.beta.threads.runs.create(thread_id=st.session_state.thread_id, assistant_id=assistant_id)

        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(thread_id=st.session_state.thread_id, run_id=run.id)

            if run.status == 'requires_action':
                function_name, arguments, function_id = get_function_details(run)
                function_response = execute_function_call(function_name, arguments)
                run = submit_tool_outputs(client, run, st.session_state.thread_id, function_id, function_response)

        messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)

        for message in messages:
            if message.run_id == run.id and message.role == "assistant":
                st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})

    # Display all messages in the chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

else:
    st.write("Click 'Start Chat' to begin.")