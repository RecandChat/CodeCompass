from requests import Response, get
from requests.exceptions import HTTPError
from re import search
from time import sleep
from codecompasslib.API.helper_functions import load_secret, get_repo_fields


TOKEN: str = load_secret()
HEADER: dict = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'CodeCompass/v1.0.0'
}


def get_users(user_amount: int = 100) -> (list, bool):
    """
    This functions gets the users from the GitHub API based on the query parameters.
    These are them having at least 1000 followers and 1000 repos.
    :return: A list of users and a boolean indicating if the request was successful.
    """
    url: str = 'https://api.github.com/search/users'
    query_parameters: dict = {
        'q': 'repos:>1000 followers:>1000',
        'per_page': user_amount,
    }

    try:
        response: Response = get(url, headers=HEADER, params=query_parameters, allow_redirects=False)
        response.raise_for_status()

        users_data: list = []

        for user in response.json()['items']:
            users_data.append(user['login'])

        return users_data, True

    except HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return [], False
    except Exception as err:
        print(f"An error occurred: {err}")
        return [], False


def get_followers(username: str) -> (list, bool):
    """
    This function gets the followers of a user.
    :param username: The username of the user.
    :return: A list of followers and a boolean indicating if the request was successful.
    """
    url: str = f'https://api.github.com/users/{username}/followers'
    query_parameters: dict = {
        'per_page': 100,
    }
    followers: list = []

    while url != '':
        if len(followers) > 1900:
            break
        try:
            response: Response = get(url, headers=HEADER, params=query_parameters, allow_redirects=False)
            response.raise_for_status()

            for follower in response.json():
                followers.append(follower['login'])

            # Check if there is a next page
            link_header = response.headers.get('Link')
            if link_header:
                match = search(r'<(https://api.github.com/[^>]*)>; rel="next"', link_header)
                url = match.group(1) if match else "None"
            else:
                url = ''

        except HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return followers, False
        except Exception as err:
            print(f"An error occurred: {err}")
            return followers, False

    return followers, True


def get_following(username: str) -> (list, bool):
    """
    This function gets the following of a user.
    :param username: The username of the user.
    :return: A list of following and a boolean indicating if the request was successful.
    """
    url: str = f'https://api.github.com/users/{username}/following'
    query_parameters: dict = {
        'per_page': 100,
    }
    following: list = []

    while url != '':
        if len(following) > 1900:
            break
        try:
            response: Response = get(url, headers=HEADER, params=query_parameters, allow_redirects=False)
            response.raise_for_status()

            for follow in response.json():
                following.append(follow['login'])

            # If following < 100, then there is no next page
            if len(following) < 100:
                url = ''
            else:
                # Check if there is a next page
                link_header = response.headers.get('Link')
                if link_header:
                    match = search(r'<(https://api.github.com/[^>]*)>; rel="next"', link_header)
                    url = match.group(1) if match else "None"
                else:
                    url = ''

        except HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return following, False
        except Exception as err:
            print(f"An error occurred: {err}")
            return following, False

    return following, True


def get_stared_repos(username: str) -> (list, bool):
    """
    This function gets the repositories starred by a user.
    :param username: The username of the user.
    :return: A list of repositories and a boolean indicating if the request was successful.
    """
    url: str = f'https://api.github.com/users/{username}/starred'
    query_parameters: dict = {
        'per_page': 500,
    }
    starred_repos: list = []

    while url != '':
        if len(starred_repos) > 1900:
            break
        try:
            response: Response = get(url, headers=HEADER, params=query_parameters, allow_redirects=False)
            response.raise_for_status()

            for starred_repo in response.json():
                starred_repos.append(get_repo_fields(starred_repo))

            # Check if there is a next page
            link_header = response.headers.get('Link')
            if link_header:
                match = search(r'<(https://api.github.com/[^>]*)>; rel="next"', link_header)
                url = match.group(1) if match else ""
            else:
                url = ''

        except HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return starred_repos, False
        except Exception as err:
            print(f"An error occurred: {err}")
            return starred_repos, False

    return starred_repos, True


def get_user_repos(username: str) -> (list, bool):
    """
    This function gets the repositories of a user.
    :param username: The username of the user.
    :return: A list of repositories and a boolean indicating if the request was successful.
    """
    url: str = f'https://api.github.com/users/{username}/repos'
    query_parameters: dict = {
        'per_page': 100,
    }
    repos: list = []

    while url != '':
        if len(repos) > 1900:
            break
        try:
            response: Response = get(url, headers=HEADER, params=query_parameters, allow_redirects=False)
            response.raise_for_status()

            for repo in response.json():
                repos.append(get_repo_fields(repo))

            # Check if there is a next page
            link_header = response.headers.get('Link')
            if link_header:
                match = search(r'<(https://api.github.com/[^>]*)>; rel="next"', link_header)
                url = match.group(1) if match else "None"
            else:
                url = ''

        except HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return repos, False
        except Exception as err:
            print(f"An error occurred: {err}")
            return repos, False

    return repos, True


def get_misc_data(query_parameters: list = None) -> list:
    """
    This function gets the repositories from the GitHub API based on the query parameters returns a list of information.
    :param query_parameters: The query parameters. Accepted fields are 'language', 'in:name', 'in:description',
    'in:readme'.
    :return: A list with the fetched data.
    """
    ACCEPTED_FIELDS: list = ['language', 'in:name', 'in:description', 'in:readme']

    if query_parameters is None:
        query_parameters = ['language', 'in:name', 'in:description', 'in:readme']

    if not all(item in ACCEPTED_FIELDS for item in query_parameters):
        print("Invalid query parameters.")
        return []

    url: str = 'https://api.github.com/search/repositories'
    LANGUAGE_LIST: list = ['Python', 'Java', 'Go', 'JavaScript', 'C++', 'TypeScript', 'PHP', 'C', 'Ruby', "C#", 'Nix',
                           'Shell', 'Rust', 'Scala', 'Kotlin', 'Swift']
    QUERY_TOPICS: list = ['machine-learning', 'deep-learning', 'data-science', 'artificial-intelligence',
                          'neural-networks', 'computer-vision', 'natural-language-processing', 'reinforcement-learning',
                          'data-mining', 'big-data', 'data-analysis', 'data-visualization', 'data-engineering']

    query_list: list = []
    for parameter in query_parameters:
        if parameter == 'language':
            for language in LANGUAGE_LIST:
                query_list.append({
                    'q': f'{parameter}:{language}',
                    'per_page': 100,
                })
        else:
            for topic in QUERY_TOPICS:
                query_list.append({
                    'q': f'{topic} {parameter}',
                    'per_page': 100,
                })

    data_list: list = []
    for query in query_list:
        try:
            response: Response = get(url, headers=HEADER, params=query, allow_redirects=False)
            response.raise_for_status()

            repos_data: list = []

            for repo in response.json()['items']:
                repo_info = get_repo_fields(repo)
                repos_data.append(repo_info)

            data_list.append(repos_data)
        except HTTPError as err:
            print(f"HTTP error occurred: {err}")
            break
        except Exception as err:
            print(f"An error occurred: {err}")
            break

    data_list = [item for sublist in data_list for item in sublist]
    return data_list


def get_bulk_data(user_amount: int = 100) -> list:
    """
    This function gets the repositories of the users.
    :param user_amount: How many users to get.
    :return: Returns a list with the fetched data.
    """

    count: int = 1
    users: set = set()
    users_list: list
    users_flag: bool

    users_list, users_flag = get_users(user_amount)
    if users_flag:
        for user in users_list:
            users.add(user)

            followers_list: list
            followers_flag: bool

            followers_list, followers_flag = get_followers(user)
            if followers_flag:
                users.update(followers_list)
            else:
                print(f"An error occurred with user: {user} followers")
                continue

            following_list: list
            following_flag: bool

            following_list, following_flag = get_following(user)
            if following_flag:
                users.update(following_list)
            else:
                print(f"An error occurred with user: {user} following")
                continue

            if user_amount != 1:
                sleep(60)
            print("Count: ", count)
            count += 1

    else:
        print("An error occurred with getting users.")
        return []

    print("Amount of users: ", len(users))
    return list(users)
