import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


import pytest
from unittest.mock import patch, Mock, MagicMock
from codecompasslib.chatbot.api_utilities import remove_useful_urls, make_api_request
from codecompasslib.chatbot.chatbot_management import load_tools, initialize_client, create_assistant, create_message_and_run
import openai

"""
API Utilities Tests
"""

def test_remove_useful_urls_with_key_present(api_response_with_useful_urls) -> None:
    """
    Tests the remove_useful_urls function with a response JSON that contains the 'usefulUrls' key.
    Verifies that the 'usefulUrls' key is successfully removed.
    :param api_response_with_useful_urls: A sample API response containing the 'usefulUrls' key.
    :return: None
    """
    modified_response = remove_useful_urls(api_response_with_useful_urls)
    assert "usefulUrls" not in modified_response
    assert "data" in modified_response

def test_remove_useful_urls_with_key_absent(api_response_without_useful_urls) -> None:
    """
    Tests the remove_useful_urls function with a response JSON that does not contain the 'usefulUrls' key.
    Verifies that the response remains unchanged.
    :param api_response_without_useful_urls: A sample API response without the 'usefulUrls' key.
    :return: None
    """
    modified_response = remove_useful_urls(api_response_without_useful_urls)
    assert modified_response == api_response_without_useful_urls

def test_make_api_request_success(mock_github_token) -> None:
    """
    Tests the make_api_request function for a successful API call.
    Uses mocking to simulate a successful HTTP response.
    :param mock_github_token: Fixture to mock the loading of the GitHub token.
    :return: None
    """
    with patch('codecompasslib.chatbot.api_utilities.requests.post') as mocked_post:
        mocked_post.return_value = Mock(status_code=200, json=lambda: {"data": "some data", "usefulUrls": ["http://example.com"]})
        response = make_api_request("https://fakeurl.com/api/test", {})
        assert "usefulUrls" not in response
        assert response == {"data": "some data"}

"""
Chatbot Management Tests
"""

def test_load_tools(mock_tools_json_file, mock_tool_definitions):
    """Tests if tool definitions are correctly loaded from a JSON file."""
    loaded_tools = load_tools(mock_tools_json_file)
    assert loaded_tools == mock_tool_definitions, "Failed to load the correct tool definitions from the file"

@pytest.mark.parametrize("api_key", ["test_api_key"])
def test_initialize_client(api_key):
    """Tests if the OpenAI client is initialized with the provided API key."""
    with patch('codecompasslib.chatbot.chatbot_management.OpenAI', return_value=MagicMock()) as MockClient:
        initialize_client(api_key)
        MockClient.assert_called_once_with(api_key=api_key)

def test_create_assistant():
    """Tests if an assistant is created with specified parameters."""
    mock_client = Mock()
    mock_client.beta.assistants.create.return_value = Mock()
    name = "Test Assistant"
    instructions = "Helpful assistant."
    model = "gpt-3.5-turbo"
    tools = []

    assistant = create_assistant(mock_client, name, instructions, model, tools)

    mock_client.beta.assistants.create.assert_called_once_with(
        name=name,
        instructions=instructions,
        model=model,
        tools=tools
    )
    assert assistant == mock_client.beta.assistants.create.return_value, "Failed to return the correct assistant object"

"""
Repo Info tests
"""


