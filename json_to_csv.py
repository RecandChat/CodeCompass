import pandas as pd

# Converting JSON data to a pandas DataFrame
df = pd.read_json("most_starred_python_repos.json")
df.to_csv("data.csv", index=False)