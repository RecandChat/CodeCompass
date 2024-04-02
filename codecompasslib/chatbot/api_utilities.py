"""
Includes utility functions for making API requests and preprocessing responses.
"""
import requests
from typing import Dict, Any, Union
from codecompasslib.chatbot.secrets_manager import load_github_token

"""
ASK THE CODE API functions
"""

def remove_useful_urls(response_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Removes the 'usefulUrls' key from the API response JSON object if present.

    :param response_json: A dictionary representing the JSON response from an API.
    :return: The modified dictionary with the 'usefulUrls' key removed if it was present.
    """
    if 'usefulUrls' in response_json:
        del response_json['usefulUrls']
    return response_json


def make_api_request(endpoint_url: str, params: Dict[str, Any]) -> Union[Dict[str, Any], str]:
    """
    Makes a POST request to the specified API endpoint with given parameters and returns the processed JSON response.
    Removes the 'usefulUrls' field from the response if it exists. In case of an error, returns an error message.

    :param endpoint_url: The URL of the API endpoint to which the request is made.
    :param params: A dictionary of parameters to be sent in the request.
    :param github_token: The GitHub token used for Authorization header.
    :return: A dictionary representing the JSON response from the API or a string containing an error message.
    """
    github_token = load_github_token(file_path='secrets/github_token')
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(endpoint_url, json=params, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        response_json = remove_useful_urls(response_json)
        return response_json
    else:
        return f"Failed to communicate with the API: {response.status_code}, Reason: {response.reason}"