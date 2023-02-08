#!/usr/bin/python3
"""Serializes instances to a JSON file
and deserializes JSON file to instances
"""

import json
import os

class FileStorage:
    """Stores and retrieves data"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets obj with the key <obj class name>.id in __objects"""
        FileStorage.__objects["{}.{}".format(obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""

        with open(FileStorage.__file_path, "w") as f:
            f.write(json.dumps(FileStorage.__objects))

    def reload(self):
        """Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists"""

        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r") as f:
                FileStorage.__objects = json.load(f)
