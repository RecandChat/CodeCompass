"""
The entry point of application that brings everything together and runs the chatbot.
"""
from secrets_manager import load_openai_key, load_github_token
from chatbot_management import initialize_client, create_assistant, load_tools, retrieve_assistant, run_chatbot

# Load secrets
openAI_key = load_openai_key(file_path='secrets/openAI_key')
github_token = load_github_token(file_path='secrets/github_token')

# Initialize the OpenAI client
client = initialize_client(openAI_key)

# Create an assistant
"""
new_assistant = create_assistant(
    client=client,
    name="CodeCompass",
    instructions="You are a helpful assistant that analyzes code from github repositories and files when given a github url. You will answer questions about the structure of a repository, the content of files, or any other code-related queries.",
    model="gpt-3.5-turbo-0125",
    tools=load_tools('chatbot/tools.json'))
"""

# Retrieve assistant
older_assistant = retrieve_assistant(client, 'asst_gDv1PyXxMQ0GPQLYyh5KUm9C')

# Run the chatbot
run_chatbot(client, assistant=older_assistant)