import pytest
from agentlite_fraud_detection.file_handler import FileHandler

def test_file_handler_initialization():
    handler = FileHandler(upload_dir="test_dir")
    assert handler.upload_dir == "test_dir"