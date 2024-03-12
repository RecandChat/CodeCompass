from requests import Response, get
from requests.exceptions import HTTPError
from pandas import DataFrame
from helper_functions import load_secret, get_repo_fields, save_to_csv
from drive_operations import upload_df_to_drive_as_csv, get_creds_drive


TOKEN: str = load_secret()
HEADER: dict = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'CodeCompass/v1.0.0'
}

DRIVE_ID = "0AL1DtB4TdEWdUk9PVA"
DATA_FOLDER = "13JitBJQLNgMvFwx4QJcvrmDwKOYAShVx"
creds = get_creds_drive()


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
    try:
        response: Response = get(url, headers=HEADER, allow_redirects=False)
        response.raise_for_status()

        followers: list = []

        for follower in response.json():
            followers.append(follower['login'])

        return followers, True

    except HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return [], False
    except Exception as err:
        print(f"An error occurred: {err}")
        return [], False


def get_following(username: str) -> (list, bool):
    """
    This function gets the following of a user.
    :param username: The username of the user.
    :return: A list of following and a boolean indicating if the request was successful.
    """
    url: str = f'https://api.github.com/users/{username}/following'
    try:
        response: Response = get(url, headers=HEADER, allow_redirects=False)
        response.raise_for_status()

        following: list = []

        for follow in response.json():
            following.append(follow['login'])

        return following, True

    except HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return [], False
    except Exception as err:
        print(f"An error occurred: {err}")
        return [], False


def get_user_repos(username: str) -> (list, bool):
    """
    This function gets the repositories of a user.
    :param username: The username of the user.
    :return: A list of repositories and a boolean indicating if the request was successful.
    """
    url: str = f'https://api.github.com/users/{username}/repos'
    try:
        response: Response = get(url, headers=HEADER, allow_redirects=False)
        response.raise_for_status()

        repo_data: list = []

        for repo in response.json():
            repo_data.append(get_repo_fields(repo))

        return repo_data, True

    except HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return [], False
    except Exception as err:
        print(f"An error occurred: {err}")
        return [], False


def get_misc_data(query_parameters: list = None) -> bool:
    """
    This function gets the repositories from the GitHub API based on the query parameters and saves it to a csv file.
    :param query_parameters: The query parameters. Accepted fields are 'language', 'in:name', 'in:description',
    'in:readme'.
    :return: A boolean indicating if the request was successful.
    """
    ACCEPTED_FIELDS: list = ['language', 'in:name', 'in:description', 'in:readme']

    if query_parameters is None:
        query_parameters = ['language', 'in:name', 'in:description', 'in:readme']

    if not all(item in ACCEPTED_FIELDS for item in query_parameters):
        print("Invalid query parameters.")
        return False

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
            return False
        except Exception as err:
            print(f"An error occurred: {err}")
            return False

    data_list: list = [item for sublist in data_list for item in sublist]
    df: DataFrame = DataFrame(data_list)
    df.drop_duplicates(subset='id', keep='first', inplace=True)
    #save_to_csv(df, 'miscData.csv')
    upload_df_to_drive_as_csv(creds, df, 'miscData.csv', DATA_FOLDER)
    return True


def get_bulk_data(user_amount: int = 100) -> bool:
    """
    This function gets the repositories of the users and saves it to a csv file.
    :param user_amount: How many users to get.
    :return: Returns a boolean indicating if the request was successful.
    """

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
                return False

            following_list: list
            following_flag: bool

            following_list, following_flag = get_following(user)
            if following_flag:
                users.update(following_list)
            else:
                print(f"An error occurred with user: {user} following")
                return False
    else:
        print("An error occurred with getting users.")
        return False

    print("Amount of users: ", len(users))

    if len(users) > 3000:
        print("Too many users, limiting it to 3000")
        users = set(list(users)[:3000])

    users_repos: list = []
    for user in users:
        user_data, flag = get_user_repos(user)
        if flag:
            users_repos.append(user_data)
        else:
            print(f"An error occurred with user: {user}")
            return False

    users_repos: list = [item for sublist in users_repos for item in sublist]

    df: DataFrame = DataFrame(users_repos)
    df.drop_duplicates(subset='id', keep='first', inplace=True)
    #save_to_csv(df, 'original/bulkDataNew.csv')
    upload_df_to_drive_as_csv(creds, df, 'bulkDataNew.csv', DATA_FOLDER)
    return True
