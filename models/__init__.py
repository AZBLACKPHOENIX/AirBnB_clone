#!/usr/bin/python3
"""Initialize file storage for handling data."""
from models.engine.file_storage import FileStorage

# Create an instance of FileStorage for data handling
storage = FileStorage()
# Load data from the storage
storage.reload()
