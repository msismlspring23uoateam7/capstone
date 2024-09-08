import streamlit as st

from ..agentlite.agentlite.agents import BaseLLM, get_llm_backend
from ..agentlite.agentlite.commons import TaskPackage
from ..agentlite.agentlite.logging.streamlit_logger import UILogger

from actions.file_handler_action import FileHandlerAction
from actions.data_preprocessing_action import DataPreProcessingAction
from actions.visualization_action import VisualizationAction
from manager.finance_data_manager import FinanceDataManagerAgent
from agents.data_summarization_agent import DataSummarizationAgent


def execute_workflow(self):
    
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

def main():
    st.title("AgentLite Framework: Enhanced Data Analysis")
    uploaded_file = st.file_uploader("Upload a ZIP or CSV file", type=["zip", "csv"])
    if uploaded_file:
        # Initialize LLM and logger
        llm = get_llm_backend({"llm_name": "gpt-3.5-turbo", "temperature": 0.7})
        logger = UILogger()

        # Initialize agents
        file_handler_action = FileHandlerAction()
        data_processing_action = DataPreProcessingAction()
        llm_processor = DataSummarizationAgent(
            api_key="DUMMY_KEY")
        visualization_action = VisualizationAction()

        # Manager agent
        finance_data_manager = FinanceDataManagerAgent(
            llm=llm,
            team=[
                    file_handler_action,
                    data_processing_action,
                    visualization_action
                ],
            logger=logger
        )

        task_pack = TaskPackage(instruction="Start a finance data analysis pipeline")
        response = finance_data_manager(task_pack)
        st.write(response)

if __name__ == "__main__":
    main()
