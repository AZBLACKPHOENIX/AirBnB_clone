#!/usr/bin/python3
"""Module for FileStorage class"""

import os.path
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.state import State
from models.review import Review
from models.city import City


class FileStorage:
    """FileStorage class for handling JSON serialization/deserialization"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return all objects in the storage"""
        return FileStorage.__objects

    def new(self, obj):
        """Add a new object to the storage"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize objects to JSON and save to file"""
        serialized_objs = {}
        for key, obj in FileStorage.__objects.items():
            serialized_objs[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(serialized_objs, f)

    def reload(self):
        """Deserialize JSON from file and reload objects into storage"""
        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path) as f:
                obj_dict = json.load(f)
                for key, obj_data in obj_dict.items():
                    class_name, obj_id = key.split('.')
                    class_dict = {
                        'BaseModel': BaseModel,
                        'Amenity': Amenity,
                        'Place': Place,
                        'User': User,
                        'State': State,
                        'Review': Review,
                        'City': City
                    }
                    obj_instance = class_dict[class_name](**obj_data)
                    FileStorage.__objects[key] = obj_instance
