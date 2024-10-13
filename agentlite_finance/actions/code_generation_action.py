import os
import seaborn as sns
import streamlit as st
import pandas as pd
from openai import OpenAI
import matplotlib.pyplot as plt
from agentlite.actions import BaseAction
from agentlite_finance.memory.memory_keys import DATA_FRAME, DATA_SUMMARY
from agentlite_finance.memory.memory_keys import CODE

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class CodeGenerationAction(BaseAction):

    def __init__(
        self,
        shared_mem: dict = None,
    ):
        action_name = "CodeGenerationAction"
        action_desc = f"""This is a {action_name} action. 
                        It will fetch the python code to dynamically visualise the plots"""
        params_doc = {"query": "Let the code to dynamically visualise the plots be fetched by this action."}
        super().__init__(
            action_name=action_name,
            action_desc=action_desc,
            params_doc=params_doc
        )
        self.shared_mem = shared_mem

    def __call__(self, query):
        code = self.get_implementation(query)
        clean_code = self.fetch_python_code(code)
        self.shared_mem.add(CODE,  clean_code)
        return code


    def get_implementation(self, query):
        code_gen_instructions = """Give me a python method with the name plot_chart_for_stock_data which takes
                                                pandas dataframe as argument. Use your knowledge to generate
                                                accurate python code of the charts using plotly for the user
                                                prompt given. Do not include any sample data.
                                                Do not include the method in any class. 
                                                And this method should print the plot in streamlit UI using
                                                plotly_chart API like st.plotly_chart(fig). Do not call plot_chart_for_stock_data 
                                                method anywhere in the generated code, it will be invoked by other entity. Include all the 
                                                required imports in the code.Do not initialize dataframe on your own."""
        
        data_summary = "Not Available"
        if DATA_SUMMARY in self.shared_mem.keys():
            data_summary = self.shared_mem.get(DATA_SUMMARY)

        sample_data = "Not Available"
        if DATA_FRAME in self.shared_mem.keys():
            sample_data = self.shared_mem.get(DATA_FRAME).copy().iloc[:5,:10]

        complete_prompt = f"""Instructions: \n {code_gen_instructions}
                         Data Summary: \n {data_summary}
                         Sample Data:  \n {sample_data}
                         User Prompt:  \n {query}"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the GPT-4 model
            messages=[
                {"role": "system", "content": "You are an expert data analysis assistant."},
                {"role": "user", "content": complete_prompt}
            ],
            max_tokens=1000,  # Set appropriate max tokens
            temperature=0.5  # Set the temperature as needed
        )

        # Return the content of the response
        return response.choices[0].message.content

    
    

    def fetch_python_code(self, text):
        import re
        # Extract Python code block from the text using regular expression
        code = re.findall(r'```python(.*?)```', text, re.DOTALL)
        
        # Clean the extracted code by stripping unnecessary newlines and spaces
        if code:
            cleaned_code = code[0].strip()
            return cleaned_code
        return None
