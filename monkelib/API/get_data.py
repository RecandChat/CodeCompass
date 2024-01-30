"""
Functional description:
    - This file contains the functions that are used to get data from the GitHub API.
    - Helper functions are prefixed with an underscore, and they should not be used outside of this file.
"""
# --- Imports ---
import requests
import json
import pandas as pd


# --- Helper functions ---
def _save_to_json(data, filename) -> None:
    """
    This function saves data to a JSON file.
    :param data: The data to be saved.
    :param filename: The name of the file to save the data to.
    :return: True if the data was successfully saved, False if not.
    """
    with open(f"Data/{filename}", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def _save_to_csv(data, filename) -> None:
    """
    This function saves data to a CSV file.
    :param data: The data to be saved.
    :param filename: The name of the file to save the data to.
    :return: True if the data was successfully saved, False if not.
    """
    df = pd.DataFrame(data)
    df.to_csv(f"Data/{filename}", index=False)


def _get_repo_fields(repo: dict) -> dict:
    """
    This function gets the fields of a repository.
    The fields have been chosen beforehand, mentioned in the wiki of this project.
    :param repo: The repository.
    :return: A dictionary containing the fields of the repository.
    """
    repo_fields: dict = {
        'id': repo['id'],
        'name': repo['name'],
        'owner_login': repo['owner']['login'],
        'owner_type': repo['owner']['type'],
        'description': repo['description'] or "No description",
        'stars': repo['stargazers_count'],
        'url': repo['url'],
        'updated_at': repo['updated_at'],
        'language': repo['language']
    }
    return repo_fields


def _load_secret() -> str:
    """
    This function loads the GitHub Personal Access Token from the pat.json file.
    :return: The GitHub Personal Access Token.
    """
    with open('secrets/pat.json') as f:
        token_data = json.load(f)
        token: str = token_data['token']
    return token


# --- Functions ---
def get_user_repo(username: str) -> bool:
    """
    This function gets the user's repository data from the GitHub API.
    :param username: The username of the user.
    :return: True if the request was successful, False if not.
    """
    url: str = f"https://api.github.com/users/{username}/repos"
    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()  # This will raise an exception for HTTP error codes

        repos_data: list = []

        for repo in response.json():
            repo_info: dict = _get_repo_fields(repo)
            repos_data.append(repo_info)

        # Writing data to a JSON file
        _save_to_json(repos_data, 'userRepos.json')
        print("Data successfully written to userRepos.json")

        # Writing data to a CSV file
        _save_to_csv(repos_data, 'userRepos.csv')
        print("Data successfully written to userRepos.csv")
        return True

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return False
    except Exception as err:
        print(f"An error occurred: {err}")
        return False


def get_most_starred_python_repos() -> bool:
    """
    This function gets the most starred Python repositories from the GitHub API.
    :return: True if the request was successful, False if not.
    """

    url: str = 'https://api.github.com/search/repositories'
    query_params: dict = {
        'q': 'language:python',
        'per_page': 10  # Number of results per page (max 100)
    }
    # Load the token from the pat.json file
    token: str = _load_secret()

    headers: dict = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        response: requests.Response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()  # This will raise an exception for HTTP error codes

        repos_data: list = []

        for repo in response.json()['items']:
            repo_info = _get_repo_fields(repo)
            repos_data.append(repo_info)

        # Writing data to a JSON file
        _save_to_json(repos_data, 'most_starred_python_repos.json')
        print("Data successfully written to most_starred_python_repos.json")

        # Writing data to a CSV file
        _save_to_csv(repos_data, 'most_starred_python_repos.csv')
        print("Data successfully written to most_starred_python_repos.csv")
        return True

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return False
    except Exception as err:
        print(f"An error occurred: {err}")
        return False
