import os
import zipfile
import pandas as pd
import streamlit as st
from datetime import datetime
from agentlite.actions import BaseAction
from agentlite_finance.memory.memory_keys import FILE
from agentlite_finance.memory.memory_keys import DATA_FRAME

class FileHandlerAction(BaseAction):
    def __init__(
        self,
        shared_mem,
        upload_dir="uploaded_files",
    ):
        action_name = "FileHandler"
        action_desc = f"""This is a {action_name} action. 
                        It will take a csv as input and load it directly or
                        take a zip file as input, extract the csv file from it
                        and then load the csv file"""
        params_doc = {"query": "Let the data be loaded from the file."}
        super().__init__(
            action_name=action_name,
            action_desc=action_desc,
            params_doc=params_doc
        )
        self.shared_mem = shared_mem
        self.upload_dir = upload_dir
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

    def __call__(self, query):
        self.file = self.shared_mem.get(FILE)
        dataframe = self.handle_uploaded_file(self.file)
        st.write("Uploaded Data:")
        st.dataframe(dataframe)
        self.shared_mem.add(DATA_FRAME, dataframe)
        return {"response": "File successfully processed and saved as data frame."}

    def handle_uploaded_file(self, uploaded_file):
        # Generate a unique file name with timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{timestamp}_{uploaded_file.name}"
        file_path = os.path.join(self.upload_dir, file_name)

        # Save the uploaded file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Handle the file based on its type
        if zipfile.is_zipfile(file_path):
            return self._extract_zip(file_path)
        elif uploaded_file.name.endswith('.csv'):
            return pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file type. Please upload a ZIP or CSV file.")

    def _extract_zip(self, zip_path):
        # Extract ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.upload_dir)

        # Find CSV files in the extracted contents
        extracted_files = [f for f in os.listdir(self.upload_dir) if f.endswith('.csv')]
        if extracted_files:
            # If multiple CSV files, allow user to handle which one to choose
            if len(extracted_files) > 1:
                print(f"Multiple CSV files found: {extracted_files}. Reading the first one.")
            
            # Read and return the first CSV file
            return pd.read_csv(os.path.join(self.upload_dir, extracted_files[0]))
        else:
            raise ValueError("No CSV files found in the ZIP archive.")

    def list_extracted_files(self):
        """Utility function to list extracted files (for debugging or user interaction)."""
        return [f for f in os.listdir(self.upload_dir)]