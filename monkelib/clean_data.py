# Description: This script is used to clean the data from the original CSV file and save it to a new CSV file.

# It does the following:
# 1. Load the data from the original CSV file.
# 2. Drop unnecessary columns.
# 3. Clean text data.
# 4. Filter based on 'has_issues'.
# 5. Drop missing values. -> might not work for certain datasets
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

    # Filter based on 'has_issues'
    df = df[df['has_issues'] == True].drop(['has_issues'], axis=1)

    return df

def delete_missing_values(df):
    # Drop rows with any missing values
    df = df.dropna()
    return df

def save_data(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

# File paths - CHANGE THIS TO YOUR CSV
input_file_path = 'monkelib/Data/original/mostStarredRepos.csv'
output_file_path = 'monkelib/Data/clean/mostStarredReposCleaned.csv'

# Columns to drop and text columns to clean
columns_to_drop = [
    'is_archived', 'is_disabled', 'owner_user', 'license', 'has_pages', 
    'owner_type', 'date_created', 'has_projects', 'has_downloads', 'topics', 
    'is_template', 'has _discussions', 'allows_forking', 'date_updated', 'size', 
    'is_fork', 'date_pushed', 'watchers', 'updated_at', 'has_wiki', 'open_issues_count'
]
text_columns = ['description', 'name']

# Script execution
df = load_data(input_file_path)
if df is not None:
    cleaned_df = clean_data(df, columns_to_drop, text_columns)
    cleaned_df = delete_missing_values(cleaned_df)
    save_data(cleaned_df, output_file_path)
else:
    print("Data loading failed, script will exit.")
