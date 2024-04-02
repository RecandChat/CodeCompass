import sys
import os

# Get the directory where the current file (app.py) is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (root of the project)
project_root = os.path.dirname(current_dir)
# Add the project root to the Python path
sys.path.insert(0, project_root)

import streamlit as st
from htmlTemplates import css, bot_template, user_template
from codecompasslib.chatbot.chatbot_management import initialize_client, retrieve_assistant, run_chatbot_streamlit
from codecompasslib.chatbot.secrets_manager import load_openai_key, load_github_token

# Load secrets
openAI_key = load_openai_key(file_path='./secrets/openAI_key')
github_token = load_github_token(file_path='./secrets/github_token')

# Initialize the OpenAI client and assistant outside of main
client = initialize_client(openAI_key)
assistant = retrieve_assistant(client, 'asst_cibfhJsvFEKbAo7EmaS34oQD')

def main():
    st.title("GitHub Repository Chatbot")
    st.write(css, unsafe_allow_html=True)

    try:
        run_chatbot_streamlit(client, assistant)
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()