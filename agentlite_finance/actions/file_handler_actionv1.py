import pandas as pd  # Add this at the top of the file

class FileHandlerActionV1:
    def __init__(self, shared_mem):
        self.shared_mem = shared_mem

    def handle_uploaded_file(self, uploaded_file):
        # Process the uploaded file (assuming it's a CSV)
        dataframe = pd.read_csv(uploaded_file)  # Ensure pandas is imported
        
        # Store the dataframe in shared memory using the add method
        self.shared_mem.add('dataframe', dataframe)

        return dataframe