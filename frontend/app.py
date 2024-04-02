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

def main():
    st.title("GitHub Repository Chatbot")
    st.write(css, unsafe_allow_html=True)

    if 'response_pending' not in st.session_state:
        st.session_state.response_pending = False

    user_input = st.text_input("Enter your query:")
    ask_button = st.button("Ask")
    check_response_button = st.button("Check Response")

    if ask_button and user_input:
        # Start the conversation
        client = initialize_client(openAI_key)
        assistant = retrieve_assistant(client, 'asst_cibfhJsvFEKbAo7EmaS34oQD')
        _, _ = run_chatbot_streamlit(client, assistant, user_input)  # This initiates the conversation
        st.session_state.response_pending = True

    if check_response_button and st.session_state.response_pending:
        # Attempt to retrieve the response
        response, status = run_chatbot_streamlit(client, assistant, "")
        if status == 'completed':
            st.write(response)
            st.session_state.response_pending = False
        else:
            st.write("Checking for response...")
            
if __name__ == "__main__":
    main()