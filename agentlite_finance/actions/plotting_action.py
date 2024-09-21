import streamlit as st
from sklearn.preprocessing import StandardScaler
from agentlite.actions.BaseAction import BaseAction
from agentlite.logging.streamlit_logger import UILogger
from agentlite_finance.memory.memory_keys import CODE

#TODO update this file for stockcdata
class PlottingAction(BaseAction):

    def __init__(
        self,
        shared_mem
    ):
        action_name = "PreProcessing"
        action_desc = f"""This is a {action_name} action. 
                            It will preprocess and transform the given data"""
        params_doc = {"query": "Let the data be pre-processed by this action."}
        super().__init__(
            action_name=action_name,
            action_desc=action_desc,
            params_doc=params_doc
        )
        self.shared_mem = shared_mem

    def __call__(self, query):
        print()
        if self.shared_mem.get(CODE) is None:
            return {"response": "Could not find dataframe. Load dataframe using FileHandler action first."}
        code_response = self.shared_mem.get(CODE)
        updated_data = self.execute_code(code_response)
        return {"response": "Pre-Processing is done. Now, continue with next action based on the task."}
    
    def process_data(self, data):

        
        return data

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