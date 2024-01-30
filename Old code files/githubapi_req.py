import requests
import time
import json

# Replace with your personal access token
# Load the token from the pat.json file
with open('secrets/pat.json') as f:
    token_data = json.load(f)
    token = token_data['token']


# GitHub API URL for searching repositories
url = 'https://api.github.com/search/repositories'

# Setting query parameters for the most starred Python repositories
query_params = {
    'q': 'language:python',
    'per_page': 10  # Number of results per page (max 100)
}

# Headers with authorization token
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
}

try:
    response = requests.get(url, headers=headers, params=query_params)
    response.raise_for_status()  # This will raise an exception for HTTP error codes

    repos_data = []

    # Process each repository in the response
    for repo in response.json()['items']:
        repo_info = {
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
        repos_data.append(repo_info)

    # Writing data to a JSON file
    with open('../most_starred_python_repos.json', 'w', encoding='utf-8') as f:
        json.dump(repos_data, f, ensure_ascii=False, indent=4)

    print("Data successfully written to most_starred_python_repos.json")

except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
except Exception as err:
    print(f"An error occurred: {err}")

# Handling API rate limit (Sleep for 2 seconds)
time.sleep(2)
