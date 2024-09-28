import streamlit as st
from openai import OpenAI
from sklearn.preprocessing import StandardScaler
from agentlite.actions.BaseAction import BaseAction
from agentlite.logging.streamlit_logger import UILogger
from agentlite_finance.memory.memory_keys import DATA_FRAME
from agentlite_finance.memory.memory_keys import DATA_SUMMARY

client = OpenAI(api_key="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")

#TODO update this file for stockcdata
class GenericInsightsAction(BaseAction):

    def __init__(
        self,
        shared_mem : dict = None
    ):
        action_name = "GenericInsightsAction"
        action_desc = f"""This is a {action_name} action. 
                            It will provide text based information about the data."""
        params_doc = {"query": "Let any generic query be handled by this action."}
        super().__init__(
            action_name=action_name,
            action_desc=action_desc,
            params_doc=params_doc
        )
        self.shared_mem = shared_mem

    def __call__(self, query):
        result = self.get_result(query)
        st.write(result)
        return {"response": "Text based information is provided. Now, continue with next action based on the task."}


    def get_result(self, query):
        result_instructions = """Use your knowledge to generate accurate results of the user prompt.
                                                Take help of data and some sample to generate your result."""
        
        data_summary = self.shared_mem.get(DATA_SUMMARY)
        data = self.shared_mem.get(DATA_FRAME)

        #get distinct stocks from the data
        unique_stocks = data['Name'].unique()        

        #get required stocks from the prompt
        stocks_needed = []
        for i in unique_stocks:
            if i in query.split():
                stocks_needed.append(i)

        if stocks_needed == []:
            st.write('Please mention the name of the stock to be analyzed in upper case.')

        #filter the data based on the stocks mentioned
        filtered_data = data[data['Name'].isin(stocks_needed)].copy()
        
        #sample_data = self.shared_mem.get(DATA_FRAME).copy().iloc[:5,:10]
        sample_data = filtered_data.copy().iloc[:5,:10]

        complete_prompt = f"""Instructions: \n {result_instructions}
                         Data: \n {filtered_data}
                         Sample Data:  \n {sample_data}
                         User Prompt:  \n {query}"""
        print("***** CODEGEN LLM PROMPT" + complete_prompt)
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
