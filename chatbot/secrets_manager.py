"""
Contains functions related to loading secrets like API keys and URLs. 
"""

def load_openai_key(file_path='secrets/openAI_key') -> str:
    """
    Loads the OpenAI API key from a specified file.

    :param file_path: The path to the file containing the OpenAI API key.
    :return: The OpenAI API key, or an empty string if the file cannot be found.
    """
    try:
        with open(file_path, 'r') as file:
            openai_key = file.read().strip()  # Use strip() to remove newline characters
            print("OpenAI key loaded successfully.")
            return openai_key
    except FileNotFoundError:
        print(f"OpenAI key file not found at {file_path}.")
        return ""

def load_github_token(file_path='secrets/github_token') -> str:
    """
    Loads the GitHub token from a specified file.

    :param file_path: The path to the file containing the GitHub token.
    :return: The GitHub token, or an empty string if the file cannot be found.
    """
    try:
        with open(file_path, 'r') as file:
            github_token = file.read().strip()  # Use strip() to remove newline characters
            print("GitHub token loaded successfully.")
            return github_token
    except FileNotFoundError:
        print(f"GitHub token file not found at {file_path}.")
        return ""
    
def load_askthecode_api_base_url(file_path= 'secrets/askthecode_API') -> str:
    """
    Loads the AskTheCode API base URL from a local secrets file.

    :return: The base URL as a string.
    """
    with open(file_path, 'r') as file:
        base_url = file.read().strip()
    return base_url

def load_assistant_instructions(file_path='secrets/instructions') -> str:
    """
    Loads the assistant instructions from a specified file.

    :param file_path: The path to the file containing the assistant instructions.
    :return: The assistant instructions, or an empty string if the file cannot be found.
    """
    try:
        with open(file_path, 'r') as file:
            instructions = file.read().strip()  # Use strip() to remove newline characters
            print("Assistant instructions loaded successfully.")
            return instructions
    except FileNotFoundError:
        print(f"Assistant instructions file not found at {file_path}.")
        return ""