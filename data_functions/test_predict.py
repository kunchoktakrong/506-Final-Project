import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_functions.predictForest import load_data_and_train

def test_model_runs():
    accuracy = load_data_and_train(test_mode=True)
    assert accuracy > 0.5
