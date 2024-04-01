import sys
import os

# Get the directory where the current file (app.py) is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (root of the project)
project_root = os.path.dirname(current_dir)

# Add the project root to the Python path
sys.path.insert(0, project_root)

import streamlit as st 
from codecompasslib.chatbot.chatbot_management import initialize_client, retrieve_assistant, get_response_for_streamlit
from codecompasslib.chatbot.secrets_manager import load_openai_key, load_github_token

# Load secrets
openAI_key = load_openai_key(file_path='../secrets/openAI_key')
github_token = load_github_token(file_path='../secrets/github_token')

def main():
    st.title("GitHub Repository Chatbot")
    user_input = st.text_input("Enter your query:")
    submit_button = st.button("Ask")

    if 'thread_id' not in st.session_state:
        st.session_state['thread_id'] = None

    if submit_button:
        client = initialize_client(openAI_key)
        assistant = retrieve_assistant(client, 'asst_cibfhJsvFEKbAo7EmaS34oQD')

        response, thread_id = get_response_for_streamlit(client, assistant, user_input, st.session_state['thread_id'])
        st.session_state['thread_id'] = thread_id
        st.write(response)

if __name__ == "__main__":
    main()