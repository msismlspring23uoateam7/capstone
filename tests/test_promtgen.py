import pytest
import pandas as pd
from agentlite_fraud_detection.promptgen import PromptGenerator

@pytest.fixture
def prompt_generator():
    custom_templates = {
        "Fraud Analysis": "Analyze the following data for potential fraud cases:\n\n{data}",
        "Summary": "Please summarize the following data:\n\n{data}"
    }
    return PromptGenerator(custom_templates=custom_templates)

def test_custom_template(prompt_generator):
    test_data = pd.DataFrame({"Amount": [100, 200, 300, 400]})
    prompt = prompt_generator.generate_prompt(test_data, task="Fraud Analysis")
    assert "potential fraud cases" in prompt

def test_default_template(prompt_generator):
    test_data = pd.DataFrame({"Revenue": [1000, 2000, 1500, 3000], "Net_Income": [100, 200, 150, 300]})
    prompt = prompt_generator.generate_prompt(test_data)
    assert "company performance" in prompt

def test_fallback_template(prompt_generator):
    test_data = pd.DataFrame({"Other_Column": [1, 2, 3, 4]})
    prompt = prompt_generator.generate_prompt(test_data, task="Unknown Task")
    assert "Perform Unknown Task" in prompt