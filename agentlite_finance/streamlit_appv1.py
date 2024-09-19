import sys
print(sys.modules)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from agentlite_finance.llm_handler_v1 import LLMHandlerV1
from agentlite_finance.actions.file_handler_actionv1 import FileHandlerActionV1
from agentlite_finance.shared_memoryv1 import SharedMemoryV1  # Correctly import SharedMemoryV1

# Visualization functions

def plot_line_chart(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    data[['date', 'open', 'high', 'low', 'close']].set_index('date').plot(ax=ax)
    plt.title("Line Chart for Stock Prices (Open, High, Low, Close)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    st.pyplot(fig)

def plot_candlestick_chart(data):
    fig = go.Figure(data=[go.Candlestick(x=data['date'],
                                         open=data['open'],
                                         high=data['high'],
                                         low=data['low'],
                                         close=data['close'])])
    fig.update_layout(title='Candlestick Chart', xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig)

def plot_moving_average(data, window=20):
    data['SMA'] = data['close'].rolling(window=window).mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    data[['date', 'close', 'SMA']].set_index('date').plot(ax=ax)
    plt.title(f"Moving Average (Window: {window} days)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    st.pyplot(fig)

def plot_histogram(data, column='close'):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data[column], bins=30, kde=True, ax=ax)
    plt.title(f"Histogram of {column.capitalize()} Prices")
    plt.xlabel(f"{column.capitalize()} Price")
    plt.ylabel("Frequency")
    st.pyplot(fig)

def plot_bar_chart(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    data['Name'].value_counts().plot(kind='bar', ax=ax)
    plt.title("Bar Chart for Stock Names")
    plt.xlabel("Stock Name")
    plt.ylabel("Count")
    st.pyplot(fig)

def plot_boxplot(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=data[['open', 'high', 'low', 'close']], ax=ax)
    plt.title("Boxplot for Stock Prices (Open, High, Low, Close)")
    st.pyplot(fig)

def plot_correlation_heatmap(data):
    correlation_matrix = data[['open', 'high', 'low', 'close', 'volume']].corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
    plt.title("Correlation Heatmap for Stock Data")
    st.pyplot(fig)

def plot_scatter(data, x_column, y_column):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=data[x_column], y=data[y_column], ax=ax)
    plt.title(f"Scatter Plot ({x_column.capitalize()} vs {y_column.capitalize()})")
    plt.xlabel(x_column.capitalize())
    plt.ylabel(y_column.capitalize())
    st.pyplot(fig)

def main():
    st.title("Comprehensive Stock Data Analysis with Visualizations")

    # Step 1: Initialize SharedMemoryV1 for managing data and conversations
    shared_mem = SharedMemoryV1()  # Use the custom memory class

    # Step 2: File upload via Streamlit UI
    uploaded_file = st.file_uploader("Upload Stock Data CSV", type=["csv"])

    if uploaded_file:
        # Use FileHandlerActionV1 to process the uploaded file
        file_handler_action = FileHandlerActionV1(shared_mem)
        dataframe = file_handler_action.handle_uploaded_file(uploaded_file)
        dataframe['date'] = pd.to_datetime(dataframe['date'])
        st.write("Uploaded Data:")
        st.dataframe(dataframe)

        # Save the dataframe in shared memory
        shared_mem.add('dataframe', dataframe)

    # Initialize LLM handler
    llm_handler = LLMHandlerV1(shared_mem)

    # Handle session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat Input for Prompts
    if prompt := st.chat_input("Ask for specific analysis or insights, or request a specific chart (e.g., 'Show me a line chart')"):
        # Save the user prompt to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Step 3: Get response from LLM based on the prompt and data
        response = llm_handler.handle_prompt(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)

        # Save conversation history
        shared_mem.add_conversation(prompt, response)

        # Step 4: Let user explicitly request visualizations via prompt
        if "line chart" in prompt.lower():
            st.write("Generating line chart for stock prices...")
            plot_line_chart(shared_mem.get('dataframe'))
        elif "candlestick" in prompt.lower():
            st.write("Generating candlestick chart...")
            plot_candlestick_chart(shared_mem.get('dataframe'))
        elif "moving average" in prompt.lower():
            st.write("Generating moving average chart...")
            plot_moving_average(shared_mem.get('dataframe'))
        elif "histogram" in prompt.lower():
            st.write("Generating histogram for stock prices...")
            plot_histogram(shared_mem.get('dataframe'))
        elif "bar chart" in prompt.lower():
            st.write("Generating bar chart for stock names...")
            plot_bar_chart(shared_mem.get('dataframe'))
        elif "boxplot" in prompt.lower():
            st.write("Generating boxplot for stock prices...")
            plot_boxplot(shared_mem.get('dataframe'))
        elif "correlation heatmap" in prompt.lower():
            st.write("Generating correlation heatmap...")
            plot_correlation_heatmap(shared_mem.get('dataframe'))
        elif "scatter plot" in prompt.lower():
            st.write("Generating scatter plot...")
            # You can customize which columns to plot against each other
            plot_scatter(shared_mem.get('dataframe'), x_column='open', y_column='close')
        else:
            st.write("Please ask for a specific chart (e.g., 'Show me a line chart').")

if __name__ == "__main__":
    main()