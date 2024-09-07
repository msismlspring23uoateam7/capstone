import os
import zipfile
import pandas as pd
from datetime import datetime

class FileHandler:
    def __init__(self, upload_dir="uploaded_files"):
        self.upload_dir = upload_dir
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

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