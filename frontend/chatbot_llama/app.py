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
import json
import requests
import streamlit as st
from typing import Any
from openai.types.beta.threads.run import Run
from codecompasslib.chatbot.chatbot_management import get_llama_details, execute_function_call
from codecompasslib.chatbot.secrets_manager import load_llama_key, load_github_token
from codecompasslib.chatbot.repo_info import (get_repo_structure, get_repo_content, 
                                              get_repo_branches, get_commit_history, 
                                              search_repo_code, search_repo_commits, find_repos)

# Function map to relate user commands to function calls
function_map = {
    "get_repo_structure": get_repo_structure,
    "get_repo_content": get_repo_content,
    "get_repo_branches": get_repo_branches,
    "get_commit_history": get_commit_history,
    "search_repo_code": search_repo_code,
    "search_repo_commits": search_repo_commits,
    "find_repos": find_repos
}

import requests

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": "Bearer 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"}

def query(payload, client, api_key):
    """Send a query to the specified client with a payload."""
    response = requests.post(client, headers=api_key, json=payload)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to get response", "status_code": response.status_code}

def process_function_call(user_input):
    """Process user input to determine which function to call."""
    def extract_url(text):
        """Extract GitHub URL from the provided text."""
        url_regex = r'https?://github\.com/[a-zA-Z0-9-]+/[a-zA-Z0-9-]+'
        match = re.search(url_regex, text)
        return match.group(0) if match else None

    url = extract_url(user_input)

    if "structure of" in user_input and url:
        return function_map["get_repo_structure"](url=url)
    elif "content of" in user_input and url:
        file_paths = []  # Define file paths based on your requirement
        return function_map["get_repo_content"](url=url, filePaths=file_paths)
    elif "branches of" in user_input and url:
        return function_map["get_repo_branches"](url=url)
    elif "commit history of" in user_input and url:
        file_path = None  # Define file path if needed
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

# Load secrets and initialize the client
llama_api_key = load_llama_key(file_path='/Users/mirandadrummond/VSCode/CodeCompass/secrets/llama_key.json')
github_token = load_github_token(file_path='/Users/mirandadrummond/VSCode/CodeCompass/secrets/github_token.json')
assistant_id = 'Meta-Llama-3-8B'
client = f"https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

# Setup Streamlit UI
st.set_page_config(page_title="CodeCompassBot", page_icon=":speech_balloon:")
st.title("CodeCompass Chatbot")

# Manage session states for chat functionalities
if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True

if st.button("Exit Chat"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state
    st.session_state.thread_id = None

if "llama_model" not in st.session_state:
    st.session_state.openai_model = "Meta-Llama-3-8B"  # GPT3.5 assistant

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.start_chat:
    prompt = st.chat_input("Enter your query")
    if prompt:
        # Append user query to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Process function call first and check its output
        # function_output = process_function_call(prompt)
        # function_name, arguments, function_id = get_llama_details(function_output)
        # function_response = execute_function_call(function_name, arguments)
        
        answer = query({"inputs": prompt}, client, llama_api_key)
        # parse answer to get the response
        if answer:
            formatted_answer = json.dumps(answer, indent=2)
            st.session_state.messages.append({"role": "assistant", "content": formatted_answer})
        else:
            st.session_state.messages.append({"role": "assistant", "content": prompt})
            

    # Display all messages in the chat history
    # Display all messages in the chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and message["content"].startswith('['):
                # Use st.json for better formatting of JSON data
                st.json(message["content"])
            else:
                st.markdown(message["content"])
else:
    st.write("Click 'Start Chat' to begin.")
