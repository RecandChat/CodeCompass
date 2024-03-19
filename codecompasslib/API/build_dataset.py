"""
Load the user_list.txt file to grab the user
- I need to grab users until I have 1000 of them, if the user is already in the processed_users.txt file I need to skip
it
- Once I have that list of users I need to add them to the processed_users.txt file (which might not exist yet)
- Once I have the list of users I need to grab their repository info and add them to a csv file called dataset.csv
- The csv file should then be merged with the existing dataset.csv file if it exists, dropping any duplicates by ID
"""
from get_bulk_data import get_user_repos
import pandas as pd
import os

processed_users = set()
try:
    with open('processed_users.txt', 'r') as file:
        for line in file:
            processed_users.add(line.strip())
except FileNotFoundError:
    pass

users = []
with open('user_list.txt', 'r') as file:
    for line in file:
        users.append(line.strip())

counter = 0
# Count how many CSV files have been created located under the datasets folder
for i in range(1, 100):
    if f'dataset{i}.csv' not in os.listdir('datasets'):
        counter = i
        break

print("Counter: ", counter)

while True:
    users_to_process: list = [user for user in users if user not in processed_users]
    users_to_process = users_to_process[:1000]
    print(users_to_process)

    repos = []
    for user in users_to_process:
        repo, flag = get_user_repos(user)
        if flag:
            repos.extend(repo)
        else:
            if len(repo) == 0:
                print(f'User {user} not found')
            else:
                print("Error with user", user)
                repos.extend(repo)

    df = pd.DataFrame(repos)
    print(df.shape)
    df.to_csv(f'datasets/dataset{counter}.csv', index=False)

    with open('processed_users.txt', 'a') as file:
        for user in users_to_process:
            file.write(user + '\n')

    processed_users.update(users_to_process)

    print("Processed users:", len(processed_users))
    if len(users_to_process) < 1000 or len(processed_users) == len(users) or counter == 80:
        break

    users_to_process.clear()
    repos.clear()
    counter += 1
