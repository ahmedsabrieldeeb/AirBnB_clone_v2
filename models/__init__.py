#!/usr/bin/python3
"""initiates an object of storage bases (file/database)"""

from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
import os

if (os.environ.get("HBNB_TYPE_STORAGE") == "db"):
    storage = DBStorage()
    storage.reload()
else:
    storage = FileStorage()
    storage.reload()
