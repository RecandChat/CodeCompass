"""
Contains functions related to loading secrets like API keys and URLs. 
"""

import json


def load_openai_key(file_path='./secrets/openAI_key.json') -> str:
    """
    Loads the OpenAI API key from a specified file.

    :param file_path: The path to the file containing the OpenAI API key.
    :return: The OpenAI API key, or an empty string if the file cannot be found.
    """   
    try:
        with open(file_path) as f:
            key = json.load(f)['key']
            print("OpenAI API key loaded successfully.")
            return key
    except FileNotFoundError:
        print("OpenAI API key file not found.")
        return ""