import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from ...agentlite.agentlite.actions import BaseAction

class VisualizationAction(BaseAction):

    def __init__(
        self,
    ):
        action_name = "Visualization"
        action_desc = f"""This is a {action_name} action. 
                        It will take the finance data and display relevant visualizations."""
        params_doc = {}
        super().__init__(
            action_name=action_name,
            action_desc=action_desc,
            params_doc=params_doc
        )

    def __call__(self, data):
        raise self.visualize_data(data)

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