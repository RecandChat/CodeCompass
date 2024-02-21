# Description: This script is used to clean the data from the original CSV file and save it to a new CSV file.

# It does the following:
# 1. Load the data from the original CSV file.
# 2. Drop unnecessary columns.
# 3. Clean text data. (removes stopwords, special characters, etc.)
# 5. Drops missing values 
# 6. Save the cleaned data to a new CSV file.


import pandas as pd
import neattext.functions as nf

def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def clean_data(df, columns_to_drop, text_columns):
    if df is None:
        return None

    # Drop unnecessary columns
    df = df.drop(columns_to_drop, axis=1)

    # Clean text data
    for col in text_columns:
        # Ensure that the column data type is string and handle missing values
        df[col] = df[col].fillna('').astype(str)
        df[col] = df[col].apply(nf.remove_special_characters)
        df[col] = df[col].apply(nf.remove_stopwords)

    # Filter out rows where 'description' equals the string 'description' -> we don't want rows without a description
    df = df[df['description'].str.lower() != 'description']

    return df

def delete_missing_values(df):
    # List of columns to check for missing values
    columns_to_check = [
        'id', 'name', 'owner_user', 'description', 'url',
        'date_created', 'date_updated', 'date_pushed', 'size', 'stars', 'watchers',
        'updated_at', 'language', 'num_forks', 'license', 'open_issues', 'topics', 
        'is_archived', 'is_disabled', 'is_template', 'has_projects', 
        'has _discussions', 'owner_type', 'has_pages', 'has_wiki', 
        'has_issues', 'has_downloads', 'is_fork'
    ]

    # Drop rows with any missing values in the specified columns
    df = df.dropna(subset=columns_to_check)

    return df


def delete_duplicates(df):
    # Drop duplicate rows based on id
    df = df.drop_duplicates(subset=['id'], keep='first')
    return df

def save_data(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

# File paths - CHANGE THIS TO YOUR CSVs
input_file_path = 'monkelib/Data/original/mostStarredRepos.csv'
output_file_path = 'monkelib/Data/clean/t4.csv'

# Columns to drop and text columns to clean -> these columns should always be dropped as one is the same as open_issues, and allow_forking is not useful in any situation
columns_to_drop = [
   'open_issues_count', 'allow_forking'
]
text_columns = ['description', 'name']

# Script execution
df = load_data(input_file_path)
if df is not None:
    cleaned_df = clean_data(df, columns_to_drop, text_columns)
    cleaned_df = delete_missing_values(cleaned_df)
    cleaned_df = delete_duplicates(cleaned_df)
    save_data(cleaned_df, output_file_path)
else:
    print("Data loading failed, script will exit.")
