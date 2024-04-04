import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import pytest
from codecompasslib.models.lightgbm_model import generate_lightGBM_recommendations, load_data

def test_train_lightGBM_model():
    # Load data
    df_non_embedded, df_embedded = load_data()
    