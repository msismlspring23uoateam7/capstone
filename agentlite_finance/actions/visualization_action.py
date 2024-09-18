import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from agentlite.actions import BaseAction
from agentlite_finance.memory.memory_keys import DATA_FRAME

#TODO update this file for stockcdata
class VisualizationAction(BaseAction):

    def __init__(
        self,
        shared_mem
    ):
        action_name = "Visualization"
        action_desc = f"""This is a {action_name} action. 
                        It will take the data and display relevant visualizations."""
        params_doc = {"query": "Let the data be visualised by this action."}
        super().__init__(
            action_name=action_name,
            action_desc=action_desc,
            params_doc=params_doc
        )
        self.shared_mem = shared_mem

    def __call__(self, query):
        data = self.shared_mem.get(DATA_FRAME)
        self.visualize_data(data)
        return {"response": "Visualisations are created. Now, continue with next action based on the task."}

    def visualize_data(self, data):
        # Check for numeric columns in the data
        numeric_columns = data.select_dtypes(include=["float64", "int64"]).columns

        if numeric_columns.empty:
            st.warning("No numeric data found for visualization.")
            return

        # Visualize histograms for each numeric column
        for column in numeric_columns:
            try:
                plt.figure(figsize=(14, 7))
                sns.histplot(data[column], kde=True, bins=50)
                plt.title(f'Distribution of {column}')
                st.pyplot(plt.gcf())
                plt.close()
            except Exception as e:
                st.error(f"Error visualizing {column}: {str(e)}")
                
        self.visualize_correlation_matrix(data)
    
    def visualize_correlation_matrix(self, data):
        try:
            # Select only numeric columns for correlation matrix
            numeric_data = data.select_dtypes(include=["float64", "int64"])
            if numeric_data.empty:
                st.warning("No numeric data available for correlation matrix.")
                return

            plt.figure(figsize=(12, 8))
            sns.heatmap(numeric_data.corr(), annot=True, fmt='.2f', cmap='coolwarm')
            plt.title('Correlation Matrix')
            st.pyplot(plt.gcf())
            plt.close()
        except Exception as e:
            st.error(f"Error in correlation matrix visualization: {str(e)}")