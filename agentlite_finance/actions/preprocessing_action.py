import streamlit as st
from sklearn.preprocessing import StandardScaler
from agentlite.actions.BaseAction import BaseAction
from agentlite.logging.streamlit_logger import UILogger
from agentlite_finance.memory.memory_keys import DATA_FRAME

#TODO update this file for stockcdata
class PreprocessingAction(BaseAction):

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
        if self.shared_mem.get(DATA_FRAME) is None:
            return {"response": "Could not find dataframe. Load dataframe using FileHandler action first."}
        data = self.shared_mem.get(DATA_FRAME)
        updated_data = self.process_data(data)
        st.write("Processed Data:")
        st.dataframe(updated_data)
        self.shared_mem.update(DATA_FRAME, updated_data)
        return {"response": "Pre-Processing is done. Now, continue with next action based on the task."}
    
    def process_data(self, data):
        # Clean the data
        data = self.clean_data(data)
        
        # Check if data is empty after cleaning
        if data.empty:
            raise ValueError("Data is empty after cleaning. Please upload valid data.")
        
        # Perform feature engineering
        data = self.feature_engineering(data)
        
        # Transform the data
        data = self.transform_data(data)
        
        return data

    def clean_data(self, data):
        """Remove null values and duplicates from the data."""
        data.dropna(inplace=True)
        data.drop_duplicates(inplace=True)
        return data

    def feature_engineering(self, data):
        """Perform specific feature engineering based on the type of data."""
        return data

    def transform_data(self, data):
        """Apply necessary data transformations."""
        return data
    
    def preprocess_dataframe(self, dataframe):
        # Example preprocessing: Convert 'date' column to datetime, handle missing values
        if 'date' in dataframe.columns:
            dataframe['date'] = pd.to_datetime(dataframe['date'], errors='coerce')

        # Optionally, handle missing data in a more nuanced way (e.g., fill or flag)
        # For example, forward-fill missing values for numeric columns
        #dataframe = dataframe.fillna(method='ffill')
        dataframe = dataframe.ffill()


        # Drop any rows with missing dates or other critical fields
        dataframe = dataframe.dropna(subset=['date'])

        return dataframe