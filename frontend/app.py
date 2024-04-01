import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # help to locate chatbot folder 

import streamlit as st 
from codecompasslib.chatbot.chatbot_management import initialize_client, retrieve_assistant, get_response_for_streamlit
from codecompasslib.chatbot.repo_info import get_repo_structure, get_repo_content, get_repo_branches, get_commit_history, search_repo_code, search_repo_commits, find_repos
from codecompasslib.chatbot.secrets_manager import load_openai_key, load_github_token

# Load secrets
openAI_key = load_openai_key(file_path='secrets/openAI_key')
github_token = load_github_token(file_path='secrets/github_token')

def main():
    st.title("GitHub Repository Chatbot")
    user_input = st.text_input("Enter your query:")
    submit_button = st.button("Ask")

    if 'thread_id' not in st.session_state:
        st.session_state['thread_id'] = None

    if submit_button:
        client = initialize_client(load_openai_key())
        assistant = retrieve_assistant(client, 'asst_cibfhJsvFEKbAo7EmaS34oQD')

        response, thread_id = get_response_for_streamlit(client, assistant, user_input, st.session_state['thread_id'])
        st.session_state['thread_id'] = thread_id
        st.write(response)

if __name__ == "__main__":
    main()