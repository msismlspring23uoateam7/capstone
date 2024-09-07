import pytest
from agentlite_fraud_detection.manager_agent import AgentManager
from agentlite_fraud_detection.data_processing_agent import DataProcessingAgent
from agentlite_fraud_detection.llm_processor import LLMProcessor
from agentlite_fraud_detection.visualization_agent import VisualizationAgent
from agentlite_fraud_detection.file_handler import FileHandler

def test_agent_manager_workflow():
    data_processing_agent = DataProcessingAgent()
    llm_processor = LLMProcessor(api_key="fake_api_key")
    visualization_agent = VisualizationAgent()
    file_handler = FileHandler()

    manager = AgentManager(data_processing_agent, llm_processor, visualization_agent, file_handler)
    assert manager.data_processing_agent == data_processing_agent