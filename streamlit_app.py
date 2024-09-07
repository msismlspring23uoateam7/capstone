import streamlit as st
import logging
from agentlite_fraud_detection.data_processing_agent import DataProcessingAgent
from agentlite_fraud_detection.llm_processor import LLMProcessor
from agentlite_fraud_detection.visualization_agent import VisualizationAgent
from agentlite_fraud_detection.file_handler import FileHandler

logging.basicConfig(level=logging.DEBUG)

def main():
    # Initialize agents
    data_processing_agent = DataProcessingAgent()
    llm_processor = LLMProcessor(api_key="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")
    #Andrew
    #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
    #Pramod
    #sk-Vo7jCT5lrwMyJ1YeqpzmYvDaS9sYF4Xt_BPLSaiOywT3BlbkFJVP2JXFoP36HSMWqWluMD88AkB7t0KHJ8j-FM0BUngA
    visualization_agent = VisualizationAgent()
    file_handler = FileHandler()

    st.title("Data Processing & Visualization with LLM")
    st.write("Please upload the file to proceed with data cleaning and visualization!")

    # File Upload
    uploaded_file = st.file_uploader("Upload a ZIP or CSV file", type=["zip", "csv"])
    
    if uploaded_file:
        messages = st.container(border = True)
    
        if prompt := st.chat_input("Please type init to start processing the data"):
            messages.chat_message("user").write(prompt)

            try:
                # Step 1: Handle the file
                data = file_handler.handle_uploaded_file(uploaded_file)
                messages.chat_message("assistant").write("Uploaded Data:")
                messages.chat_message("assistant").dataframe(data)
            except ValueError as e:
                messages.chat_message("assistant").error(f"File handling error: {str(e)} Please rerun the app once it has been fixed")
                return

            try:
                # Step 2: Process the data
                processed_data = data_processing_agent.process_data(data)
                messages.chat_message("assistant").write("Processed Data:")
                messages.chat_message("assistant").dataframe(processed_data)
            except ValueError as e:
                messages.chat_message("assistant").error(f"Data processing error: {str(e)} Please rerun the app once it has been fixed")
                return

            try:
                # Step 3: Generate LLM insights
                insights = llm_processor.generate_insights(processed_data)
                messages.chat_message("assistant").write("LLM Insights:")
                messages.chat_message("assistant").write(insights)
            except Exception as e:
                messages.chat_message("assistant").error(f"LLM error: {str(e)} Please rerun the app once it has been fixed")
                return

            try:
                # Step 4: Visualize the data
                messages.chat_message("assistant").write("Visualizing Data")
                visualization_agent.visualize_data(processed_data)

                # Visualizing Correlation Matrix
                messages.chat_message("assistant").write("Correlation Matrix")
                visualization_agent.visualize_correlation_matrix(processed_data)
            except Exception as e:
                messages.chat_message("assistant").error(f"Visualization error: {str(e)} Please rerun the app once it has been fixed")

if __name__ == "__main__":
    main()