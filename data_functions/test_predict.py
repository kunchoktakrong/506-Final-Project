import pandas as pd
from data_functions.predictForest import load_data_and_train
def test_model_runs():
    accuracy = load_data_and_train(test_mode=True)
    assert accuracy > 0.5 
