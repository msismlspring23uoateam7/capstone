import pandas as pd

#import warnings
#from urllib3.exceptions import InsecureRequestWarning

# Suppress only the NotOpenSSLWarning
#warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

class FileHandlerActionV1:
    def __init__(self, shared_mem):
        self.shared_mem = shared_mem

    def handle_uploaded_file(self, uploaded_file):
        try:
            # Ensure that the uploaded file is a CSV
            if not uploaded_file.name.endswith('.csv'):
                return "Error: Uploaded file is not a CSV. Please upload a CSV file."

            # Process the uploaded file (assuming it's a CSV)
            dataframe = pd.read_csv(uploaded_file)
            
            # Preprocess the dataframe (e.g., handle missing values, convert columns)
            dataframe = self.preprocess_dataframe(dataframe)

            # Store the dataframe in shared memory
            self.shared_mem.add('dataframe', dataframe)

            return dataframe
        
        except Exception as e:
            return f"Error processing the file: {e}"

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