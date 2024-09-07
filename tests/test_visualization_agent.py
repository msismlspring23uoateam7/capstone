import pytest
import pandas as pd
from agentlite_fraud_detection.visualization_agent import VisualizationAgent
import matplotlib.pyplot as plt

@pytest.fixture
def visualization_agent():
    return VisualizationAgent()

def test_visualize_financial_data(visualization_agent):
    test_data = pd.DataFrame({"Revenue": [100000, 200000, 150000, 400000], "Profit_Margin": [0.1, 0.2, 0.15, 0.4]})
    plt.figure()
    visualization_agent.visualize_data(test_data)
    assert plt.gcf().number == 1  # Check that a figure was created

def test_visualize_correlation_matrix(visualization_agent):
    test_data = pd.DataFrame({"Revenue": [100000, 200000, 150000, 400000], "Profit_Margin": [0.1, 0.2, 0.15, 0.4], "ROE": [0.05, 0.12, 0.09, 0.18]})
    plt.figure()
    visualization_agent.visualize_correlation_matrix(test_data)
    assert plt.gcf().number == 1  # Check that a correlation matrix plot was created