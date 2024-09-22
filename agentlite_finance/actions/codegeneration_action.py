import os
import seaborn as sns
import streamlit as st
import pandas as pd
from openai import OpenAI
import matplotlib.pyplot as plt
from agentlite.actions import BaseAction
from agentlite_finance.memory.memory_keys import DATA_FRAME
from agentlite_finance.memory.memory_keys import CODE

client = OpenAI(api_key="sk-Vo7jCT5lrwMyJ1YeqpzmYvDaS9sYF4Xt_BPLSaiOywT3BlbkFJVP2JXFoP36HSMWqWluMD88AkB7t0KHJ8j-FM0BUngA")

class CodegenerationAction(BaseAction):

    def __init__(
        self,
        shared_mem: dict = None,
    ):
        action_name = "Codegeneration"
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
        data = self.shared_mem.get(DATA_FRAME)
        code = self.get_implementation()
        print(code)
        st.write(code)
        clean_code = self.fetch_python_code(code) #TODO check where it is needed or not
        self.shared_mem.add(CODE,  clean_code)
        print(clean_code)
        return {"response": "Python code is fetched. Now, continue with next action based on the task."}


    def get_implementation(self):
        # Generate the prompt using the prompt generator
        # prompt = self.prompt_generator.generate_prompt(data, task=task)
        # prompt = data
        # Use the newer OpenAI ChatCompletion API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the GPT-4 model
            messages=[
                {"role": "system", "content": "You are an expert in Python Programmer and a data visualization expert."},
                {"role": "user", "content": """Give me a python method with name plot_line_chart_for_stock_data.Use your
                                                knowledge to generate accurate python code of the charts using plotly.
                                                Do not include the method in any class. 
                                                And this method should print the plot
                                                in streamlit UI. Do not call the method, It will be invoked by
                                                other entity."""}
            ],
            max_tokens=1000,  # Set appropriate max tokens
            temperature=0.7  # Set the temperature as needed
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