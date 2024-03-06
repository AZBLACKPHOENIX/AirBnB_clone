#!/usr/bin/python3
"""Module for FileStorage class."""

import json
from models.base_model import BaseModel


class FileStorage:
    """Class for serializing and deserializing instances to and from JSON."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Add a new object to __objects."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to a JSON file."""
        json_dict = {}
        for key, value in FileStorage.__objects.items():
            json_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(json_dict, f)

    def reload(self):
        """Deserialize the JSON file to __objects."""
        try:
            with open(FileStorage.__file_path, "r") as f:
                json_dict = json.load(f)
                for key, value in json_dict.items():
                    class_name = value["__class__"]
                    obj = eval(class_name + "(**value)")
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass

