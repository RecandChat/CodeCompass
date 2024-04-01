import pytest
from unittest.mock import patch, Mock
from codecompasslib.chatbot.api_utilities import remove_useful_urls, make_api_request

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
    with patch('api_utilities.requests.post') as mocked_post:
        mocked_post.return_value = Mock(status_code=200, json=lambda: {"data": "some data", "usefulUrls": ["http://example.com"]})
        response = make_api_request("https://fakeurl.com/api/test", {})
        assert "usefulUrls" not in response
        assert response == {"data": "some data"}

