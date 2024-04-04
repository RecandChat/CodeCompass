import os
import sys
from typing import Tuple
from pandas import DataFrame, read_csv, merge, concat
from numpy import ndarray, argsort
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from category_encoders import ordinal

# go up to root
# Construct the path to the root directory (one level up from embeddings)
root_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(root_dir)
real_project_dir = os.path.dirname(project_dir)

# Add the project directory to the Python path
sys.path.insert(0, real_project_dir)

from codecompasslib.API.get_bulk_data import get_stared_repos, get_user_repos


def encode_csv(df: DataFrame, encoder, label_col: str, typ: str = "fit") -> Tuple[DataFrame, ndarray]:
    """
    Encode the categorical columns in a DataFrame using the specified encoder.
    :param df: The DataFrame to be encoded.
    :param encoder: The encoder object used for encoding the categorical columns.
    :param label_col: The name of the label column.
    :param typ: The type of encoding to perform. Defaults to "fit".
    :return: A tuple containing the encoded DataFrame and the label column values.
    """
    if typ == "fit":
        df = encoder.fit_transform(df)
    else:
        df = encoder.transform(df)
    y: ndarray = df[label_col].values
    del df[label_col]
    return df, y


def train_lightGBM_model(df_merged: DataFrame, label_col: str) -> Tuple[lgb.Booster, ordinal.OrdinalEncoder]:
    """
    Trains a LightGBM model using the provided merged dataframe.

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


    :param df_merged: DataFrame containing the training data.
    :param label_col: The name of the target variable column.
    :return: A tuple containing the trained LightGBM model and the ordinal encoder.
    """

    # Training LightGBM model
    MAX_LEAF: int = 64
    MIN_DATA: int = 20
    NUM_OF_TREES: int = 100
    TREE_LEARNING_RATE: float = 0.15
    EARLY_STOPPING_ROUNDS: int = 20
    METRIC: str = "auc"
    SIZE: str = "sample"

    params: dict = {
        "task": "train",
        "boosting_type": "gbdt",
        "num_class": 1,
        "objective": "binary",
        "metric": METRIC,
        "num_leaves": MAX_LEAF,
        "min_data": MIN_DATA,
        "boost_from_average": True,
        "num_threads": 20,
        "feature_fraction": 0.8,
        "learning_rate": TREE_LEARNING_RATE,
    }

    print("Training LightGBM model")

    X: DataFrame = df_merged.drop(columns=['target', 'id', 'owner_user'])
    y: DataFrame = df_merged[label_col]

    X_combined, X_test, y_combined, y_test = train_test_split(X, y, test_size=0.1, random_state=42, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(X_combined, y_combined, test_size=0.1, random_state=42,
                                                      stratify=y_combined)

    # combine X_train and y_train
    train_data = concat([X_train, y_train], axis=1)
    valid_data = concat([X_val, y_val], axis=1)
    test_data = concat([X_test, y_test], axis=1)
    
    nume_cols = ["embedding_" + str(i) for i in range(256)] + ["stars"]
    cate_cols = ['language']	
    
    ord_encoder = ordinal.OrdinalEncoder(cols=cate_cols)

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


def load_data() -> Tuple[DataFrame, DataFrame]:
    """
    Load the data from the Google Drive
    :return: The non-embedded and embedded datasets
    """
    df_non_embedded: DataFrame = read_csv("codecompasslib/models/data_full.csv")
    df_embedded: DataFrame = read_csv("codecompasslib/models/df_embedded_combined.csv")

    print("Data loaded")
    return df_non_embedded, df_embedded


def generate_lightGBM_recommendations(target_user: str, df_non_embedded: DataFrame, df_embedded: DataFrame,
                                      number_of_recommendations: int = 10) -> list:
    """
    Generate recommendations using a LightGBM model.
    :param target_user: The target user for whom recommendations are to be generated.
    :param df_non_embedded: The non-embedded dataset.
    :param df_embedded: The embedded dataset.
    :param number_of_recommendations: The number of recommendations to generate. Defaults to 10.
    :return: A list of recommendations.
    """
    owned_by_target_repo_ids: list = [item['id'] for item in get_user_repos(target_user)[0]]
    starred_repo_ids = [item['id'] for item in get_stared_repos(target_user)[0]]

    # Adding stars column to the embedded dataset (add any other column if you want to use it for a model)
    df_merged: DataFrame = merge(df_embedded, df_non_embedded[['id']], on='id', how='left')
    # turn stars column into integer column
    df_merged['stars'] = df_merged['stars'].apply(lambda x: int(x))
    
    label_col: str = 'target'
    
    # add target column which will be 1 if the user has starred or owns the repo and 0 otherwise
    df_merged[label_col] = df_merged['id'].apply(lambda x: 1 if x in starred_repo_ids+owned_by_target_repo_ids else 0)
    
    lgb_model: lgb.Booster
    ord_encoder: ordinal.OrdinalEncoder
    lgb_model, ord_encoder = train_lightGBM_model(df_merged, label_col)

    # make predictions for all the repos
    df_test: DataFrame = df_merged.drop(columns=['id', 'owner_user'])
    full_dataset_x, full_dataset_y = encode_csv(df_test, ord_encoder, label_col, "transform")
    all_preds = lgb_model.predict(full_dataset_x)

    # get sorted predictions with the highest one first
    top_indices = argsort(all_preds)[::-1]

    recommendations: list = []  # list storing the recommendations

    counter: int = 0
    not_to_recommend: list = owned_by_target_repo_ids + starred_repo_ids
    for index in top_indices:
        if counter == number_of_recommendations:
            break
        # disregard if the repo is already starred by the user
        if df_merged.iloc[index]['id'] in not_to_recommend:
            continue
        else:
            counter += 1
            recommendations.append((df_merged.iloc[index]['id'], df_merged.iloc[index]['owner_user'], all_preds[index]))
    
    return recommendations
    