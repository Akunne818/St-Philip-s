#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv
from dotenv import load_dotenv

load_dotenv()

storage_t = getenv("Church_TYPE_STORAGE")
print(storage_t)
if storage_t == "db":
    from models.engine.db_storage import DBStorage

    storage = DBStorage()

else:
    from models.engine.file_storage import Filestorage

    storage = Filestorage()
storage.reload()
