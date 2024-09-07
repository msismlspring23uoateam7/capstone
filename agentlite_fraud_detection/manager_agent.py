import streamlit as st
from agentlite_fraud_detection.data_processing_agent import DataProcessingAgent
from agentlite_fraud_detection.llm_processor import LLMProcessor
from agentlite_fraud_detection.visualization_agent import VisualizationAgent
from agentlite_fraud_detection.file_handler import FileHandler

class AgentManager:
    def __init__(self, data_processing_agent, llm_processor, visualization_agent, file_handler):
        self.data_processing_agent = data_processing_agent
        self.llm_processor = llm_processor
        self.visualization_agent = visualization_agent
        self.file_handler = file_handler

    def execute_workflow(self):
        st.title("AgentLite Framework: Enhanced Data Analysis")

        # File upload widget
        uploaded_file = st.file_uploader("Upload a ZIP or CSV file", type=["zip", "csv"])
        
        if uploaded_file:
            try:
                data = self.file_handler.handle_uploaded_file(uploaded_file)
                st.write("Uploaded Data:")
                st.dataframe(data)

                # Process the data
                processed_data = self.data_processing_agent.process_data(data)
                st.write("Processed Data:")
                st.dataframe(processed_data)

                # Generate LLM insights
                insights = self.llm_processor.generate_insights(processed_data, task="general_analysis")
                st.write("LLM Insights:")
                st.write(insights)

                # Visualize the data
                self.visualization_agent.visualize_data(processed_data)
                self.visualization_agent.visualize_correlation_matrix(processed_data)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")