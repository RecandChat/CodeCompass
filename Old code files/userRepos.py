import requests
import time
import json

url = "https://api.github.com/users/Lukasaurus11/repos"
    
try:
    response = requests.get(url)
    response.raise_for_status()  # This will raise an exception for HTTP error codes

    repos_data = []

    for repo in response.json():
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
    with open('userData.json', 'w', encoding='utf-8') as f:
        json.dump(repos_data, f, ensure_ascii=False, indent=4)

    print("Data successfully written to userData.json")

except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
except Exception as err:
    print(f"An error occurred: {err}")

# Handling API rate limit (Sleep for 2 seconds)
time.sleep(2)
    


