from json import load
from pandas import DataFrame
from os.path import dirname
from pathlib import Path
import requests

PARENT_PATH: str = dirname(dirname(__file__))  # Get the parent directory of the current directory (codecompasslib)
OUTER_PATH: str = dirname(dirname(dirname(__file__)))  # Get the most outer directory of the project


def save_to_csv(data: any, filename: str) -> None:
    """
    This function saves the data to a csv file.
    :param data: The data to be saved.
    :param filename: The name of the file.
    :return: Does not return anything.
    """
    df = DataFrame(data)
    df.to_csv(Path(PARENT_PATH + '/Data/' + filename), index=False)


def get_repo_fields(repo: dict) -> dict:
    """
    This function gets the fields of a repository.
    The fields have been chosen beforehand, mentioned in the wiki of this project.
    :param repo: The repository.
    :return: A dictionary containing the fields of the repository.
    """
    repo_fields: dict = {
        'id': repo['id'],
        'name': repo['name'],
        'owner_user': repo['owner']['login'],
        'owner_type': repo['owner']['type'],
        'description': repo['description'] or "No description",
        'url': repo['url'],
        'is_fork': repo['fork'],  # Forked from another repo
        'date_created': repo['created_at'],
        'date_updated': repo['updated_at'],  # different from date pushed because of pull requests
        'date_pushed': repo['pushed_at'],
        'size': repo['size'],  # size in KB
        'stars': repo['stargazers_count'],
        'watchers': repo['watchers_count'],
        'updated_at': repo['updated_at'],
        'language': repo['language'],
        'has_issues': repo['has_issues'],
        'has_projects': repo['has_projects'],
        'has_downloads': repo['has_downloads'],
        'has_wiki': repo['has_wiki'],
        'has_pages': repo['has_pages'],
        'has _discussions': repo['has_discussions'],
        'num_forks': repo['forks'],
        'is_archived': repo['archived'],
        'is_disabled': repo['disabled'],
        'is_template': repo['is_template'],
        'license': repo['license']['name'] if repo['license'] else "No license",
        'open_issues': repo['open_issues'],
        'topics': repo['topics'],
    }
    return repo_fields


def load_secret() -> str:
    """
    This function loads the secret token.
    :return: The secret token.
    """
    try:
        with open(OUTER_PATH + '/secrets/pat.json') as f:
            TOKEN = load(f)['token']
            print("Token loaded successfully.")
    except FileNotFoundError:
        print("Secret file not found.")
        return ''

    # Check if the token is valid
    HEADER: dict = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'CodeCompass'
    }

    url: str = 'https://api.github.com/user'

    try:
        response: requests.Response = requests.get(url, headers=HEADER)
        response.raise_for_status()
        print("Token is valid.")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}. Token might be invalid.")
        return ''
    except Exception as err:
        print(f"An error occurred: {err}. Token might be invalid.")
        return ''

    return TOKEN
