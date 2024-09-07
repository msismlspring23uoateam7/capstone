# test_data_processing_agent.py
import pytest
import pandas as pd
from agentlite_fraud_detection.data_processing_agent import DataProcessingAgent

@pytest.fixture
def data_processing_agent():
    return DataProcessingAgent()

def test_clean_data(data_processing_agent):
    test_data = pd.DataFrame({"Amount": [100, 200, None], "Time": [3600, 7200, 10800]})
    clean_data = data_processing_agent.clean_data(test_data)
    assert clean_data.isnull().sum().sum() == 0

def test_feature_engineering(data_processing_agent):
    test_data = pd.DataFrame({"Amount": [100, 200, 300], "Time": [3600, 7200, 10800]})
    engineered_data = data_processing_agent.feature_engineering(test_data)
    assert 'Scaled_Amount' in engineered_data.columns
    assert 'Hour' in engineered_data.columns