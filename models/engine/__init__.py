# models/engine/__init__.py

from models.engine.file_storage import FileStorage

# Create an instance of FileStorage for handling data
storage = FileStorage()
# Load data from the storage
storage.reload()
