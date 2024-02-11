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

        _save_to_json(repos_data, 'userRepos.json')
        print("Data successfully written to userRepos.json")

        _save_to_csv(repos_data, 'userRepos.csv')
        print("Data successfully written to userRepos.csv")
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


def get_users_from_following_link() -> bool:
    # Read the JSON file
    with open(PARENT_PATH + '/Data/usersData.json') as f:
        users_data = load(f)

    following_links = []
    for user in users_data:
        following_links.append(user['following_url'].replace('{/other_user}', ""))

    users: list = []
    token: str = _load_secret()

    headers: dict = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    for link in following_links:
        try:
            response: requests.Response = requests.get(link, headers=headers, allow_redirects=False)
            response.raise_for_status()

            for user in response.json():
                users.append(user['login'])

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return False
        except Exception as err:
            print(f"An error occurred: {err}")
            return False

    _save_to_json(users, 'usersFromFollowingLink.json')
    print("Data successfully written to usersFromFollowingLink.json")
    return True


def get_followers_from_user() -> bool:
    # Read the JSON file
    with open(PARENT_PATH + '/Data/usersData.json') as f:
        users_data = load(f)

    followers_links = []
    for user in users_data:
        followers_links.append(user['followers_url'])

    followers: list = []
    token: str = _load_secret()

    headers: dict = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    for link in followers_links:
        try:
            response: requests.Response = requests.get(link, headers=headers, allow_redirects=False)
            response.raise_for_status()

            for user in response.json():
                followers.append(user['login'])

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return False
        except Exception as err:
            print(f"An error occurred: {err}")
            return False

    _save_to_json(followers, 'followersFromUser.json')
    print("Data successfully written to followersFromUser.json")
    return True


def data_from_users() -> bool:
    """

    :return:
    """
    url: str = 'https://api.github.com/users'
    query: dict = {
        'q': 'followers:>1000 repos:>1000',
        'per_page': 100,
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

        # Save the users data to a JSON file
        _save_to_json(users_data, 'usersData.json')
        print("Data successfully written to usersData.json")
        return True

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return False
    except Exception as err:
        print(f"An error occurred: {err}")
        return False


def most_famous_users_repos() -> bool:
    """

    :return:
    """

    users: any = set()
    with open(PARENT_PATH + '/Data/followersFromUser.json') as f:
        followers = load(f)
        for follower in followers:
            users.add(follower)

    with open(PARENT_PATH + '/Data/usersFromFollowingLink.json') as f:
        following = load(f)
        for user in following:
            users.add(user)

    with open(PARENT_PATH + '/Data/usersData.json') as f:
        users_data = load(f)
        for user in users_data:
            users.add(user['login'])

    users = list(users)

    print("Number of users: ", len(users))

    token: str = _load_secret()
    headers: dict = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Limit the users to 10
    users = users[:1000]

    users_data: list = []

    for user in users:
        url: str = f"https://api.github.com/users/{user}/repos"
        try:
            response: requests.Response = requests.get(url, headers=headers, allow_redirects=False)
            response.raise_for_status()

            repos_data: list = []

            for repo in response.json():
                repo_info: dict = _get_repo_fields(repo)
                repos_data.append(repo_info)

            users_data.append(repos_data)

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return False
        except Exception as err:
            print(f"An error occurred: {err}")
            return False

    users_data: list = [item for sublist in users_data for item in sublist]  # Flatten the list

    _save_to_json(users_data, 'mostFamousUsersRepos.json')
    print("Data successfully written to mostFamousUsersRepos.json")

    _save_to_csv(users_data, 'mostFamousUsersRepos.csv')
    print("Data successfully written to mostFamousUsersRepos.csv")
    return True


most_famous_users_repos()
