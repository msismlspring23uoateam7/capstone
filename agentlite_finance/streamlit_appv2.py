import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from agentlite_finance.llm_handler_v1 import LLMHandlerV1
from agentlite_finance.actions.file_handler_actionv1 import FileHandlerActionV1
from agentlite_finance.shared_memoryv1 import SharedMemoryV1
from agentlite_finance.manager_agent import ManagerAgent  # Import ManagerAgent

# Visualization actions class
class VisualizationActions:
    @staticmethod
    def plot_line_chart(data):
        fig, ax = plt.subplots(figsize=(10, 6))
        data[['date', 'open', 'high', 'low', 'close']].set_index('date').plot(ax=ax)
        plt.title("Line Chart for Stock Prices (Open, High, Low, Close)")
        plt.xlabel("Date")
        plt.ylabel("Price")
        st.pyplot(fig)

    @staticmethod
    def plot_candlestick_chart(data):
        fig = go.Figure(data=[go.Candlestick(x=data['date'],
                                             open=data['open'],
                                             high=data['high'],
                                             low=data['low'],
                                             close=data['close'])])
        fig.update_layout(title='Candlestick Chart', xaxis_title='Date', yaxis_title='Price')
        st.plotly_chart(fig)

    @staticmethod
    def plot_moving_average(data, window=20):
        data['SMA'] = data['close'].rolling(window=window).mean()
        fig, ax = plt.subplots(figsize=(10, 6))
        data[['date', 'close', 'SMA']].set_index('date').plot(ax=ax)
        plt.title(f"Moving Average (Window: {window} days)")
        plt.xlabel("Date")
        plt.ylabel("Price")
        st.pyplot(fig)

    @staticmethod
    def plot_histogram(data, column='close'):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data[column], bins=30, kde=True, ax=ax)
        plt.title(f"Histogram of {column.capitalize()} Prices")
        plt.xlabel(f"{column.capitalize()} Price")
        plt.ylabel("Frequency")
        st.pyplot(fig)

    @staticmethod
    def plot_bar_chart(data):
        fig, ax = plt.subplots(figsize=(10, 6))
        data['Name'].value_counts().plot(kind='bar', ax=ax)
        plt.title("Bar Chart for Stock Names")
        plt.xlabel("Stock Name")
        plt.ylabel("Count")
        st.pyplot(fig)

    @staticmethod
    def plot_boxplot(data):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=data[['open', 'high', 'low', 'close']], ax=ax)
        plt.title("Boxplot for Stock Prices (Open, High, Low, Close)")
        st.pyplot(fig)

    @staticmethod
    def plot_correlation_heatmap(data):
        correlation_matrix = data[['open', 'high', 'low', 'close', 'volume']].corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
        plt.title("Correlation Heatmap for Stock Data")
        st.pyplot(fig)

    @staticmethod
    def plot_scatter(data, x_column, y_column):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x=data[x_column], y=data[y_column], ax=ax)
        plt.title(f"Scatter Plot ({x_column.capitalize()} vs {y_column.capitalize()})")
        plt.xlabel(x_column.capitalize())
        plt.ylabel(y_column.capitalize())
        st.pyplot(fig)

# Main function
def main():
    st.title("Comprehensive Stock Data Analysis with Manager Agent")

    # Step 1: Initialize SharedMemoryV1 for managing data and conversations
    shared_mem = SharedMemoryV1()

    # Step 2: File upload via Streamlit UI
    uploaded_file = st.file_uploader("Upload Stock Data CSV", type=["csv"])

    # Step 3: Initialize the necessary agents
    file_handler_action = FileHandlerActionV1(shared_mem)
    llm_handler = LLMHandlerV1(shared_mem)
    visualization_actions = VisualizationActions()

    # Initialize ManagerAgent to manage the interactions
    manager_agent = ManagerAgent(shared_mem, llm_handler, file_handler_action, visualization_actions)

    if uploaded_file:
        # Step 4: Use ManagerAgent to handle the file upload
        manager_agent.handle_user_input({"upload": True, "file": uploaded_file})

        # Convert date column to datetime
        dataframe = shared_mem.get('dataframe')
        dataframe['date'] = pd.to_datetime(dataframe['date'])
        st.write("Uploaded Data:")
        st.dataframe(dataframe)

    # Handle session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Step 5: Chat Input for Prompts
    if prompt := st.chat_input("Ask for specific analysis or insights, or request a specific chart (e.g., 'Show me a line chart')"):
        # Save the user prompt to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Step 6: Use ManagerAgent to handle the prompt
        response = manager_agent.handle_user_input({"analyze": True, "prompt": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)

        # Step 7: Let ManagerAgent handle visualizations based on prompt
        if "line chart" in prompt.lower():
            st.write("Generating line chart for stock prices...")
            manager_agent.handle_user_input({"visualize": True, "chart_type": "line chart"})
        elif "candlestick" in prompt.lower():
            st.write("Generating candlestick chart...")
            manager_agent.handle_user_input({"visualize": True, "chart_type": "candlestick"})
        elif "moving average" in prompt.lower():
            st.write("Generating moving average chart...")
            manager_agent.handle_user_input({"visualize": True, "chart_type": "moving average"})
        elif "histogram" in prompt.lower():
            st.write("Generating histogram for stock prices...")
            manager_agent.handle_user_input({"visualize": True, "chart_type": "histogram"})
        elif "bar chart" in prompt.lower():
            st.write("Generating bar chart for stock names...")
            manager_agent.handle_user_input({"visualize": True, "chart_type": "bar chart"})
        elif "boxplot" in prompt.lower():
            st.write("Generating boxplot for stock prices...")
            manager_agent.handle_user_input({"visualize": True, "chart_type": "boxplot"})
        elif "correlation heatmap" in prompt.lower():
            st.write("Generating correlation heatmap...")
            manager_agent.handle_user_input({"visualize": True, "chart_type": "correlation heatmap"})
        elif "scatter plot" in prompt.lower():
            st.write("Generating scatter plot...")
            manager_agent.handle_user_input({"visualize": True, "chart_type": "scatter plot"})
        else:
            st.write("Please ask for a specific chart (e.g., 'Show me a line chart').")

if __name__ == "__main__":
    main()