import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# test_lightgbm_model.py

import pytest
import pandas as pd
from codecompasslib.models.lightgbm_model import generate_lightGBM_recommendations, preprocess_data


@pytest.fixture
def sample_data():
    # Sample data for testing
    df_non_embedded = pd.DataFrame({
        'id': list(range(1, 26)),
        'stars': list(range(1, 26)),
        'language': ['Python', 'Java', 'Python', 'JavaScript', 'Python'] * 5,
        'description': [f'Description {i}' for i in range(1, 26)],
    })
    df_embedded = pd.DataFrame({
        'id': list(range(1, 26)),
        'owner_user': ['user1', 'user2', 'user3', 'user4', 'user5'] * 5,
    })
    
    return df_non_embedded, df_embedded


def test_preprocess_data(sample_data, monkeypatch):
    df_non_embedded, df_embedded = sample_data
    target_user = 'user1'
    label_col = 'target'

    # Mock the API calls
    def mock_get_user_repos(username):
        print("Mock get_user_repos called with username:", username)
        return [[{'id': 1}, {'id': 6}, {'id': 11}, {'id': 16}, {'id': 21}]]  # Simulate 5 repos owned by user1

    def mock_get_stared_repos(username):
        return [[{'id': 3}]]  # Simulate 1 starred repo
    
    # Apply the mock functions
    monkeypatch.setattr('codecompasslib.models.lightgbm_model.get_user_repos', mock_get_user_repos)
    monkeypatch.setattr('codecompasslib.models.lightgbm_model.get_stared_repos', mock_get_stared_repos)
    
    # Call the function
    df_merged, starred_or_owned_by_user = preprocess_data(df_embedded, df_non_embedded, label_col, target_user)

    # Assertions
    assert len(df_merged) == 25
    assert 'target' in df_merged.columns
    assert len(starred_or_owned_by_user) == 6  # Expecting 6 repos owned or starred by user1


def test_generate_lightGBM_recommendations(sample_data, monkeypatch):
    # Mock the API calls
    def mock_get_user_repos(username):
        return [[{'id': 1}, {'id': 2}]]  # Simulate 2 repos owned by user1
    
    def mock_get_stared_repos(username):
        return [[{'id': 3}]]  # Simulate 1 starred repo
    
    # Apply the mock functions
    monkeypatch.setattr('codecompasslib.models.lightgbm_model.get_user_repos', mock_get_user_repos)
    monkeypatch.setattr('codecompasslib.models.lightgbm_model.get_stared_repos', mock_get_stared_repos)
    
    # Prepare sample data
    df_non_embedded, df_embedded = sample_data
    target_user = 'user1'
    
    # Call the function
    recommendations = generate_lightGBM_recommendations(target_user, df_non_embedded, df_embedded, 1)
    
    # Assertions
    assert len(recommendations) == 1  # Assuming number_of_recommendations is set to 10 and 7 of them are already owned/starred by the user