import os
import sys
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import category_encoders as ce

# go up to root
# Construct the path to the root directory (one level up from embeddings)
root_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(root_dir)
real_project_dir = os.path.dirname(project_dir)

# Add the project directory to the Python path
sys.path.insert(0, real_project_dir)

from codecompasslib.API.drive_operations import get_creds_drive, list_shared_drive_contents, download_csv_as_pd_dataframe, upload_df_to_drive_as_csv
from codecompasslib.API.get_bulk_data import get_stared_repos, get_user_repos

def encode_csv(df, encoder, label_col, typ="fit"):
    """
    Encode the categorical columns in a DataFrame using the specified encoder.
    Args:
        df (pandas.DataFrame): The DataFrame to be encoded.
        encoder: The encoder object used for encoding the categorical columns.
        label_col (str): The name of the label column.
        typ (str, optional): The type of encoding to perform. Defaults to "fit".

    Returns:
        tuple: A tuple containing the encoded DataFrame and the label column values.
    """
    if typ == "fit":
        df = encoder.fit_transform(df)
    else:
        df = encoder.transform(df)
    y = df[label_col].values
    del df[label_col]
    return df, y

def train_lightGBM_model(df_merged, label_col):
    """
    Trains a LightGBM model using the provided merged dataframe.

    Parameters:
    - df_merged (pandas.DataFrame): The merged dataframe containing the training data.
    - label_col (str): The name of the target variable column.

    Returns:
    - lgb_model (lightgbm.Booster): The trained LightGBM model.
    - ord_encoder (category_encoders.ordinal.OrdinalEncoder): The ordinal encoder used for encoding categorical columns.

    This function trains a LightGBM model using the provided merged dataframe. It performs the following steps:
    1. Sets the hyperparameters for the LightGBM model.
    2. Splits the merged dataframe into training, validation, and test sets.
    3. Encodes categorical columns using ordinal encoding.
    4. Creates LightGBM datasets for training, validation, and test data.
    5. Trains the LightGBM model using the training data.
    6. Returns the trained LightGBM model and the ordinal encoder.

    Note: This function assumes that the merged dataframe has the following columns:
    - 'target': The target variable to be predicted.
    - 'id': An identifier column.
    - 'owner_user': A column representing the owner user.

    The function also assumes that the merged dataframe has numerical columns named "embedding_0" to "embedding_255"
    and a categorical column named "language".

    Example usage:
    df = pd.read_csv('merged_data.csv')
    model, ord_encoder = train_lightGBM_model(df, 'target')
    """
    
    # Training LightGBM model
    MAX_LEAF = 64
    MIN_DATA = 20
    NUM_OF_TREES = 100
    TREE_LEARNING_RATE = 0.15
    EARLY_STOPPING_ROUNDS = 20
    METRIC = "auc"
    SIZE = "sample"
    
    params = {
    "task": "train",
    "boosting_type": "gbdt",
    "num_class": 1,
    "objective": "binary",
    "metric": METRIC,
    "num_leaves": MAX_LEAF,
    "min_data": MIN_DATA,
    "boost_from_average": True,
    # set it according to your cpu cores.
    "num_threads": 20,
    "feature_fraction": 0.8,
    "learning_rate": TREE_LEARNING_RATE,
    }
    
    print("Training LightGBM model")
    
    X = df_merged.drop(columns=['target', 'id', 'owner_user'])
    y = df_merged[label_col]

    X_combined, X_test, y_combined, y_test = train_test_split(X, y, test_size=0.1, random_state=42, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(X_combined, y_combined, test_size=0.1, random_state=42, stratify=y_combined)

    # combine X_train and y_train
    train_data = pd.concat([X_train, y_train], axis=1)
    valid_data = pd.concat([X_val, y_val], axis=1)
    test_data = pd.concat([X_test, y_test], axis=1)
    
    nume_cols = ["embedding_" + str(i) for i in range(256)] + ["stars"]
    cate_cols = ["language"]	
    
    ord_encoder = ce.ordinal.OrdinalEncoder(cols=cate_cols)

    train_x, train_y = encode_csv(train_data, ord_encoder, label_col)
    valid_x, valid_y = encode_csv(valid_data, ord_encoder, label_col, "transform")
    test_x, test_y = encode_csv(test_data, ord_encoder, label_col, "transform")
    
    lgb_train = lgb.Dataset(train_x, train_y.reshape(-1), params=params, categorical_feature=cate_cols)
    lgb_valid = lgb.Dataset(valid_x, valid_y.reshape(-1), reference=lgb_train, categorical_feature=cate_cols)
    lgb_test = lgb.Dataset(test_x, test_y.reshape(-1), reference=lgb_train, categorical_feature=cate_cols)
    lgb_model = lgb.train(params,
                        lgb_train,
                        num_boost_round=NUM_OF_TREES,
                        valid_sets=lgb_valid,
                        categorical_feature=cate_cols,
                        callbacks=[lgb.early_stopping(EARLY_STOPPING_ROUNDS)])
    
    return lgb_model, ord_encoder

def generate_lightGBM_recommendations(target_user, number_of_recommendations=10):
    # Load the data
    DRIVE_ID = "0AL1DtB4TdEWdUk9PVA"
    DATA_FOLDER = "13JitBJQLNgMvFwx4QJcvrmDwKOYAShVx"

    creds = get_creds_drive()
    
    # Load embedded and non-embedded dataset
    df_non_embedded = download_csv_as_pd_dataframe(creds=creds, file_id="1WSgwAhzNbSqC6e_RRBDHpgpQCnGZvVcc")
    df_embedded = download_csv_as_pd_dataframe(creds=creds, file_id="1V7P-bjQCLmFg_7ffG-s-caI6Il6B7Zvp")
    
    print("Data loaded")
    
    # grab starred repos by target user
    starred_by_target = get_stared_repos(target_user)
    starred_repo_ids = ids = [item['id'] for item in starred_by_target[0]]
    
    # Adding stars column to the embedded dataset (add any other column if you want to use it for a model)
    df_merged = pd.merge(df_embedded, df_non_embedded[['id', 'stars', 'language']], on='id', how='left')
    # turn stars column into integer column
    df_merged['stars'] = df_merged['stars'].apply(lambda x: int(x))
    
    label_col = 'target'
    
    # add target column which will be 1 if the user has starred the repo and 0 otherwise
    df_merged[label_col] = df_merged['id'].apply(lambda x: 1 if x in starred_repo_ids else 0)
    
    lgb_model, ord_encoder = train_lightGBM_model(df_merged, label_col)
    
    # make predictions for all the repos
    df_test = df_merged.drop(columns=['id', 'owner_user'])
    full_dataset_x, full_dataset_y = encode_csv(df_test, ord_encoder, label_col, "transform")
    all_preds = lgb_model.predict(full_dataset_x)
    
    # get sorted predictions with highest first
    top_indices = np.argsort(all_preds)[::-1]

    recommendations = [] # list storing the recommendations

    counter = 0
    for index in top_indices:
        if counter == number_of_recommendations:
            break
        # disregard if the repo is already starred by the user
        if df_merged.iloc[index]['id'] in starred_repo_ids:
            continue
        else:
            counter += 1
            recommendations.append((df_merged.iloc[index]['id'], df_merged.iloc[index]['owner_user'], all_preds[index]))
    
    return recommendations
        
def main():
    target_user = 'Rameshwar0852'
    recommendations = generate_lightGBM_recommendations(target_user)
    print("----Recommendations----")
    for repo in recommendations:
        print(f"Repo ID: {repo[0]}, Owner: {repo[1]}, Prediction: {repo[2]}")
    
    return recommendations

if __name__ == "__main__":
    main()