"""
Get all the CSVs from the datasets folder, and merge them all into a single dataset. Drop repositories that are
duplicated, via their ID
"""

import pandas as pd
import os

# Get all the CSVs from the datasets folder
csvs = [f for f in os.listdir('datasets') if f.endswith('.csv')]

# Merge them all into a single dataset
df = pd.concat([pd.read_csv(f'datasets/{csv}') for csv in csvs])

# Drop repositories that are duplicated, via their ID
df = df.drop_duplicates(subset='id')

# Print the shape of the dataset
print(df.shape)
