import logging
import sys
import os
import re
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mplfinance as mpf
import seaborn as sns
import numpy as np
logging.basicConfig(level=logging.DEBUG)


# Append path to the shared modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agentlite_finance.llm_handler_v1 import LLMHandlerV1
from agentlite_finance.actions.file_handler_actionv1 import FileHandlerActionV1
from agentlite_finance.shared_memoryv1 import SharedMemoryV1

# Function to preprocess data (e.g., converting date to datetime and handling missing values)
def preprocess_data(data):
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'], errors='coerce')  # Convert date to datetime
    data = data.dropna()  # Drop rows with any NaN values
    return data

# Add the function for dynamic color selection
#def get_color_options():
    colors = {
        'Primary': st.color_picker('Pick a primary color', '#636EFA'),
        'Secondary': st.color_picker('Pick a secondary color', '#EF553B'),
        'Tertiary': st.color_picker('Pick a tertiary color', '#00CC96')
    }
    return colors

# Modify execute_code function to handle the correlation matrix heatmap
def execute_code(response):
    try:
        # Ensure necessary modules are loaded
        if 'go' not in sys.modules:
            import plotly.graph_objects as go
        if 'px' not in sys.modules:
            import plotly.express as px
        if 'pd' not in sys.modules:
            import pandas as pd

        # Access the dataframe stored in session state
        if 'dataframe' not in st.session_state or st.session_state['dataframe'] is None:
            st.error("No data available. Please upload a CSV file.")
            return

        # Log the response from OpenAI to debug
        logging.debug(f"OpenAI Response: {response}")

        # Display the response in Streamlit as well for further inspection
        #st.write("OpenAI Response:")
        st.write(response)

              # Replace placeholder dataframe references and ensure code uses session state
        response = re.sub(r'\b(df|data|dataframe|data_df)\b', "st.session_state['dataframe']", response)

        # Dynamically replace incorrect code in candlestick charts (if detected)
        
         # Handle candlestick chart more specifically
        if 'go.Candlestick' in response:
            response = re.sub(r'go.Figure\(.*?=\[go.Candlestick', "go.Figure(data=[go.Candlestick", response)

        # Fix candlestick charts (common issue)
        if 'go.Candlestick' in response:
            # Display candlestick chart if the request involves candlesticks
            response = re.sub(r'go.Figure\(.*?=\[go.Candlestick', "go.Figure(data=[go.Candlestick", response)
        #response = re.sub(r'go.Figure\(.*?=\[go.Candlestick', "go.Figure(data=[go.Candlestick", response)
        #response = re.sub(r'go.Figure\(.*?=\[go.Candlestick', "go.Figure(data=[go.Candlestick", response)
       
        # Apply corrections for syntax errors (for charts and plotting)
        response = correct_syntax_errors(response)

        # Use regex to extract code blocks (text inside triple quotes or code-like structure)
        code_match = re.findall(r"```python(.*?)```", response, re.DOTALL)

        if code_match:
            # If there is Python code, display and execute it
            st.markdown("### Extracted Python Code:")
            st.code(code_match[0])  # Display the extracted code
            exec(code_match[0], globals())
        else:
            # If no code block found, try to execute the entire response
            exec(response, globals())

    except SyntaxError as se:
        st.error(f"Syntax error: {se}")
    except Exception as e:
        st.error(f"Error executing the code: {e}")

# Function to fix common syntax issues in the LLM-generated code
def correct_syntax_errors(response):
    # Fixing missing imports or syntax issues
    if "import plotly.graph_objects as go" not in response:
        response = "import plotly.graph_objects as go\n" + response
    if "import pandas as pd" not in response:
        response = "import pandas as pd\n" + response

    # Example correction for correlation heatmap (remove non-numeric data)
    if 'corr()' in response:
        response = (
            "numeric_df = st.session_state['dataframe'].select_dtypes(include=['float', 'int'])\n"
            "corr_matrix = numeric_df.corr()\n"
            "fig = px.imshow(corr_matrix, labels=dict(color='Correlation'), x=corr_matrix.columns, y=corr_matrix.columns, color_continuous_scale='RdBu')\n"
            "fig.update_layout(title='Correlation Heatmap of Stocks', width=800, height=600)\n"
            "st.plotly_chart(fig)\n"
        )

    return response

# Function to classify the type of prompt (text, EDA, visualization)
def classify_prompt(prompt):
    visualization_keywords = ['chart', 'plot', 'graph', 'visualize', 'visualization', 'heatmap', 'candlestick', 'bar chart', 'histogram', 'scatter', 'Bollinger Bands', 'MACD']
    if any(keyword in prompt.lower() for keyword in visualization_keywords):
        return 'visualization'
    else:
        return 'text'

# Main function for Streamlit app
def main():
    st.title("Dynamic Stock Data Visualization, EDA, and Insights with LLM Code")

    # Initialize shared memory for managing data and conversations
    shared_mem = SharedMemoryV1()

    # Session state for storing uploaded data
    if 'dataframe' not in st.session_state:
        st.session_state['dataframe'] = None

    # File upload via Streamlit UI
    uploaded_file = st.file_uploader("Upload Stock Data CSV", type=["csv"])

    if uploaded_file:
        file_handler_action = FileHandlerActionV1(shared_mem)
        dataframe = file_handler_action.handle_uploaded_file(uploaded_file)
        dataframe = preprocess_data(dataframe)  # Preprocess the data
        st.session_state['dataframe'] = dataframe
        st.write("Uploaded and Preprocessed Data:")
        st.dataframe(dataframe)

    # Load dataframe from session state if available
    dataframe = st.session_state.get('dataframe')

    if dataframe is None:
        st.error("Please upload a CSV file to proceed.")
        return

    # Initialize LLM handler
    llm_handler = LLMHandlerV1(shared_mem)

    # Handle session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show previous conversations (if needed)
    previous_conversations = shared_mem.get_last_n_conversations(5)
    if previous_conversations:
        st.write("Previous Conversations:")
        for conv in previous_conversations:
            st.write(f"Prompt: {conv['prompt']}")
            st.write(f"Response: {conv['response']}")
            st.write("---")

    # Chat Input for Prompts
    if prompt := st.chat_input("Ask for specific analysis, EDA, insights, or request a specific chart (e.g., 'Show me a 50-day and 200-day moving average for AAL')"):
        # Save the user prompt to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Step 1: Classify the prompt to decide what type of response to generate
        prompt_type = classify_prompt(prompt)

        if prompt_type == 'visualization':
            # Ask for Python code to visualize the data based on the uploaded `dataframe`
            response = llm_handler.handle_prompt(f"Generate Python code to visualize {prompt} using the dataframe.")
        else:
            # Ask for text-based insights (summary, analysis, etc.)
            response = llm_handler.handle_prompt(prompt)

        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown("LLM Response:")

        # Step 2: If it's a code request (either visualization or EDA), try to execute the code
        if prompt_type == 'visualization':
            st.write("Here is the python code and the chart based on the input:")
            execute_code(response)
        else:
            st.write(response)  # Only show the text once for textual responses

if __name__ == "__main__":
    main()