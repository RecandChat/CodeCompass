"""
Functions focusing on fetching various types of information about repositories.
"""

from typing import Any, Dict, List, Optional, Union
from codecompasslib.chatbot.api_utilities import make_api_request
from codecompasslib.chatbot.secrets_manager import load_askthecode_api_base_url


def get_repo_structure(url: str, branch: Optional[str] = None, relativePaths: Optional[List[str]] = None) -> Union[Dict[str, Any], str]:
    """
    Retrieves the structure of a GitHub repository at the specified URL, optionally filtering by branch and relative paths.

    :param url: The URL of the GitHub repository.
    :param branch: Optional; the specific branch to get the structure from.
    :param relativePaths: Optional; specific relative paths within the repository to include in the structure.
    :return: A dictionary representing the structure of the repository or an error message.
    """
    base_url = load_askthecode_api_base_url()
    get_repo_structure_url = f"{base_url}/api/repository/structure"
    params = {
        'url': url,
        'branch': branch,
        'relativePaths': relativePaths
    }
    return make_api_request(get_repo_structure_url, params)

# get repo content
def get_repo_content(url: str, filePaths: List[str], branch: Optional[str] = None, relativePath: Optional[str] = None) -> Union[Dict[str, Any], str]:
    """
    Retrieves the content of specific files within a GitHub repository, optionally filtered by branch and a relative path.

    :param url: The URL of the GitHub repository.
    :param filePaths: The list of file paths within the repository whose content is to be retrieved.
    :param branch: Optional; the specific branch to get the content from.
    :param relativePath: Optional; the specific relative path within the repository to filter the file paths.
    :return: A dictionary representing the content of the specified files or an error message.
    """
    base_url = load_askthecode_api_base_url()
    get_repo_content_url = f"{base_url}/api/repository/content"
    params = {
        'url': url,
        'filePaths': filePaths,
        'branch': branch,
        'relativePath': relativePath
    }
    return make_api_request(get_repo_content_url, params)
    

# get repo branches
def get_repo_branches(url: str) -> Union[Dict[str, Any], str]:
    """
    Retrieves the list of branches for the specified GitHub repository.

    :param url: The URL of the GitHub repository.
    :return: A dictionary containing the list of branches or an error message.
    """
    base_url = load_askthecode_api_base_url()
    get_repo_branches_url = f"{base_url}/api/repository/branch/list"
    params = {'url': url}
    return make_api_request(get_repo_branches_url, params)
   
    
# Get commit history
def get_commit_history(url: str, branch: Optional[str] = None, filePath: Optional[str] = None) -> Union[Dict[str, Any], str]:
    """
    Retrieves the commit history for a specified file or branch within a GitHub repository.

    :param url: The URL of the GitHub repository.
    :param branch: Optional; the specific branch to retrieve the commit history from.
    :param filePath: Optional; the specific file path to retrieve the commit history for.
    :return: A dictionary representing the commit history or an error message.
    """
    base_url = load_askthecode_api_base_url()
    get_commit_history_url = f"{base_url}/api/repository/commit/history"
    params = {
        'url': url,
        'branch': branch,
        'filePath': filePath
    }
    return make_api_request(get_commit_history_url, params)
    
# search repo code
def search_repo_code(url: str, searchKeywords: List[str], branch: Optional[str] = None, relativePath: Optional[str] = None, searchHitLinesCount: Optional[int] = None, skipMatchesCount: Optional[int] = None) -> Union[Dict[str, Any], str]:
    """
    Searches for specific keywords within the code of a GitHub repository, with optional filtering by branch, path, and pagination controls.

    :param url: The URL of the GitHub repository.
    :param searchKeywords: A list of keywords to search within the repository code.
    :param branch: Optional; the specific branch to search within.
    :param relativePath: Optional; the specific directory path to limit the search to.
    :param searchHitLinesCount: Optional; the number of lines to include in each search hit.
    :param skipMatchesCount: Optional; the number of matches to skip (for pagination).
    :return: A dictionary representing the search results or an error message.
    """
    base_url = load_askthecode_api_base_url()
    search_repo_code_url = f"{base_url}/api/search/repository/code"
    params = {
        'url': url,
        'searchKeywords': searchKeywords,
        'branch': branch,
        'relativePath': relativePath,
        'searchHitLinesCount': searchHitLinesCount,
        'skipMatchesCount': skipMatchesCount
    }
    return make_api_request(search_repo_code_url, params)

# search repo commits
def search_repo_commits(url: str, searchKeywords: List[str]) -> Union[Dict[str, Any], str]:
    """
    Searches for commits in a GitHub repository based on specified keywords.

    :param url: The URL of the GitHub repository.
    :param searchKeywords: A list of keywords to search for within the commit history.
    :return: A dictionary representing the search results or an error message.
    """
    base_url = load_askthecode_api_base_url()
    search_repo_commits_url = f"{base_url}/api/search/repository/commits"
    params = {
        'url': url,
        'searchKeywords': searchKeywords
    }
    return make_api_request(search_repo_commits_url, params)
    
def find_repos(searchKeywords: List[str], language: Optional[str] = None) -> Union[Dict[str, Any], str]:
    """
    Searches for GitHub repositories based on specified keywords and optionally filtered by programming language.

    :param searchKeywords: A list of keywords to search for repositories.
    :param language: Optional; the programming language to filter the search results by.
    :return: A dictionary representing the search results or an error message.
    """
    base_url = load_askthecode_api_base_url()
    find_repos_url = f"{base_url}/api/search/repository"
    params = {
        'searchKeywords': searchKeywords,
        'language': language
    }
    return make_api_request(find_repos_url, params)