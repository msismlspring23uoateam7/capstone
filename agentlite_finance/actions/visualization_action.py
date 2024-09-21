import seaborn as sns
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from agentlite.actions import BaseAction
from agentlite_finance.memory.memory_keys import DATA_FRAME
from agentlite_finance.memory.memory_keys import CODE

#TODO update this file for stockcdata
class VisualizationAction(BaseAction):

    def __init__(
        self,
        shared_mem: dict = None,
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
     #   self.plot_stock_data(data)
        exec(self.shared_mem.get(CODE))
        exec("plot_line_chart_for_stock_data(self.shared_mem.get(DATA_FRAME))")
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

    import matplotlib.pyplot as plt

    def plot_stock_data(self, df):
        # Ensure the 'Date' column is in datetime format
        df['Date'] = pd.to_datetime(df['date'])

        # Set 'Date' as the index
        df.set_index('Date', inplace=True)

        # Plot the stock data
        plt.figure(figsize=(10,6))
        plt.plot(df['open'], label='open', color='blue')
        plt.plot(df['high'], label='high', color='green')
        plt.plot(df['low'], label='low', color='red')
        plt.plot(df['close'], label='close', color='purple')

        # Labels and title
        plt.title(f"Stock Prices for {df['Name'][0]}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()

        # Show the plot
        plt.show()
        st.pyplot(plt)
        # st.pyplot(plt.gcf())
        plt.close()
