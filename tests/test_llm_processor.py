import pytest
from agentlite_fraud_detection.llm_processor import LLMProcessor
import pandas as pd

@pytest.fixture
def llm_processor():
    custom_templates = {
        "Fraud Analysis": "Analyze the following data for potential fraud cases:\n\n{data}",
        "Anomaly Detection": "Identify any anomalies in the following data:\n\n{data}"
    }
    return LLMProcessor(api_key="your_openai_api_key", custom_templates=custom_templates)

def test_generate_insights_with_custom_template(llm_processor):
    test_data = pd.DataFrame({"Amount": [100, 200, 300, 400]})
    result = llm_processor.generate_insights(test_data, task="Fraud Analysis")
    assert isinstance(result, str)
    assert len(result) > 0

def test_generate_insights_with_default_template(llm_processor):
    test_data = pd.DataFrame({"Revenue": [1000, 2000, 1500, 3000], "Net_Income": [100, 200, 150, 300]})
    result = llm_processor.generate_insights(test_data, task="general_analysis")
    assert isinstance(result, str)
    assert len(result) > 0