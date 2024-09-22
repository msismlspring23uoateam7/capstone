import streamlit as st
from sklearn.preprocessing import StandardScaler
from agentlite.actions.BaseAction import BaseAction
from agentlite.logging.streamlit_logger import UILogger
from agentlite_finance.memory.memory_keys import DATA_FRAME

#TODO update this file for stockcdata
class GenericInsightsAction(BaseAction):

    def __init__(
        self,
        shared_mem : dict = None
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
        if 'Amount' in data.columns:
            # Example for credit card fraud detection
            data['Scaled_Amount'] = StandardScaler().fit_transform(data['Amount'].values.reshape(-1, 1))
            if 'Time' in data.columns:
                # Time-based feature (assuming 'Time' column exists)
                data['Hour'] = data['Time'].apply(lambda x: (x // 3600) % 24)
        elif 'Revenue' in data.columns and 'Net_Income' in data.columns and 'Equity' in data.columns:
            # Example for financial data
            data['Profit_Margin'] = data['Net_Income'] / data['Revenue']
            data['ROE'] = data['Net_Income'] / data['Equity']
        else:
            raise ValueError("Unrecognized data format. Unable to perform feature engineering.")
        return data

    def transform_data(self, data):
        """Apply necessary data transformations."""
        if 'Amount' in data.columns:
            data['Normalized_Amount'] = StandardScaler().fit_transform(data['Amount'].values.reshape(-1, 1))
        return data