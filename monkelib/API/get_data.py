"""
Functional description:
    - This file contains the functions that are used to get data from the GitHub API.
    - Helper functions are prefixed with an underscore, and they should not be used outside of this file.
"""
# --- Imports ---
import requests
from json import dump, load
from pandas import DataFrame
from os.path import dirname
from pathlib import Path

# --- Constants ---
LANGUAGE_LIST: list = ['Python', 'Java', 'Go', 'JavaScript', 'C++', 'TypeScript', 'PHP', 'C', 'Ruby', "C#", 'Nix',
                       'Shell', 'Rust', 'Scala', 'Kotlin', 'Swift']
QUERY_PARAMS: list = ['language', 'in:name', 'in:description', 'in:readme']
QUERY_TOPICS: list = ['machine-learning', 'deep-learning', 'data-science', 'artificial-intelligence', 'neural-networks',
                      'computer-vision', 'natural-language-processing', 'reinforcement-learning', 'data-mining',
                      'big-data', 'data-analysis', 'data-visualization', 'data-engineering']
PARENT_PATH: str = dirname(dirname(__file__))  # Get the parent directory of the current directory (monkelib)
OUTER_PATH: str = dirname(dirname(dirname(__file__)))  # Get the most outer directory of the project


# --- Helper functions ---
def _save_to_json(data, filename) -> None:
    """
    This function saves data to a JSON file.
    :param data: The data to be saved.
    :param filename: The name of the file to save the data to.
    :return: True if the data was successfully saved, False if not.
    """
    with open(Path(PARENT_PATH + '/Data/' + filename), 'w', encoding='utf-8') as f:
        dump(data, f, ensure_ascii=False, indent=4)


def _save_to_csv(data, filename) -> None:
    """
    This function saves data to a CSV file.
    :param data: The data to be saved.
    :param filename: The name of the file to save the data to.
    :return: True if the data was successfully saved, False if not.
    """

    df = DataFrame(data)
    df.to_csv(Path(PARENT_PATH + '/Data/' + filename), index=False)


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
        'allows_forking': repo['allow_forking'],
        'open_issues_count': repo['open_issues_count'],
        'open_issues': repo['open_issues'],
        'topics': repo['topics'],
    }
    return repo_fields


def _load_secret() -> str:
    """
    This function loads the GitHub Personal Access Token from the pat.json file.
    :return: The GitHub Personal Access Token.
    """
    with open(OUTER_PATH + '/secrets/pat.json') as f:
        token_data = load(f)
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
        response: requests.Response = requests.get(url, allow_redirects=False)
        response.raise_for_status()

        repos_data: list = []

        for repo in response.json():
            repo_info: dict = _get_repo_fields(repo)
            repos_data.append(repo_info)

        # _save_to_json(repos_data, 'userRepos.json')
        # print("Data successfully written to userRepos.json")
        #
        # _save_to_csv(repos_data, 'userRepos.csv')
        # print("Data successfully written to userRepos.csv")
        return True

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return False
    except Exception as err:
        print(f"An error occurred: {err}")
        return False


def get_data() -> bool:
    """
    This function gets the most starred repositories for multiple languages from the GitHub API.
    :return: True if the request was successful, False if not.
    """

    url: str = 'https://api.github.com/search/repositories'

    queryList: list = []
    for query in QUERY_PARAMS:
        if query == 'language':
            for language in LANGUAGE_LIST:
                queryList.append({
                    'q': f'{query}:{language}',
                    'per_page': 100,
                })

        else:
            for topic in QUERY_TOPICS:
                queryList.append({
                    'q': f'{topic} {query}',
                    'per_page': 100,
                })

    token: str = _load_secret()

    headers: dict = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    dataList: list = []
    for query in queryList:
        try:
            response: requests.Response = requests.get(url, headers=headers, params=query, allow_redirects=False)
            response.raise_for_status()

            repos_data: list = []

            for repo in response.json()['items']:
                repo_info = _get_repo_fields(repo)
                repos_data.append(repo_info)

            dataList.append(repos_data)
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return False
        except Exception as err:
            print(f"An error occurred: {err}")
            return False

    dataList: list = [item for sublist in dataList for item in sublist]  # Flatten the list
    _save_to_json(dataList, 'mostStarredRepos.json')
    print("Data successfully written to mostStarredRepos.json")

    _save_to_csv(dataList, 'mostStarredRepos.csv')
    print("Data successfully written to mostStarredRepos.csv")
    return True


def get_users_from_following_link(link: list) -> list:
    """
    This function gets the users from the following link.
    :param link: The following link.
    :return: A list of users.
    """
    users: list = []
    for url in link:
        try:
            response: requests.Response = requests.get(url, allow_redirects=False)
            response.raise_for_status()

            for user in response.json():
                users.append(user['login'])

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    return users


def get_followers_from_user(username: str) -> list:
    """
    This function gets the followers of a user.
    :param username: The username of the user.
    :return: A list of followers.
    """
    url: str = f"https://api.github.com/users/{username}/followers"
    followers: list = []
    try:
        response: requests.Response = requests.get(url, allow_redirects=False)
        response.raise_for_status()

        for user in response.json():
            followers.append(user['login'])

        return followers

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return followers
    except Exception as err:
        print(f"An error occurred: {err}")
        return followers


def data_from_users() -> bool:
    """

    :return:
    """
    url: str = 'https://api.github.com/users'
    query: dict = {
        'q': 'followers:>1000 repos:>1000',
        'per_page': 40,
    }

    token: str = _load_secret()

    headers: dict = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        response: requests.Response = requests.get(url, headers=headers, params=query, allow_redirects=False)
        response.raise_for_status()

        users_data: list = []

        for user in response.json():
            users_data.append({
                'login': user['login'],
                'followers_url': user['followers_url'],
                'following_url': user['following_url'],
            })

        followers_list: list = [get_followers_from_user(user['login']) for user in users_data]
        following_list: list = [get_users_from_following_link([user['following_url']]) for user in users_data]

        users: list = [user['login'] for user in users_data]
        users = list(set(users + [item for sublist in followers_list for item in sublist] +
                         [item for sublist in following_list for item in sublist]))

        data = []
        for user in users:
            if get_user_repo(user):
                data.append(user)

        _save_to_json(data, 'usersWithData.json')
        print("Data successfully written to usersWithData.json")

        return True

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return False
    except Exception as err:
        print(f"An error occurred: {err}")
        return False


data_from_users()
