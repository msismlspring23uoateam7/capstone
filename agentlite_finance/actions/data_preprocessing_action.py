from sklearn.preprocessing import StandardScaler
from ...agentlite.agentlite.actions.BaseAction import BaseAction
from ...agentlite.agentlite.logging.streamlit_logger import UILogger

class DataPreProcessingAction(BaseAction):

    def __init__(
        self,
    ):
        action_name = "DataPreProcessing"
        action_desc = f"""This is a {action_name} action. 
                            It will preprocess and transform the given data"""
        params_doc = {}
        super().__init__(
            action_name=action_name,
            action_desc=action_desc,
            params_doc=params_doc
        )

    def __call__(self, data):
        return self.process_data(data)
    
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