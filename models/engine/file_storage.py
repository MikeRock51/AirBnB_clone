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
        FileStorage.__objects["{}.{}".format(
            obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""

        with open(FileStorage.__file_path, "w") as f:
            objects = {key: value.to_dict()
                       for key, value in FileStorage.__objects.items()}
            json.dump(objects, f)

    def class_list(self):
        """Maps classes to it's corresponding dictionary"""
        from models.base_model import BaseModel
        from models.user import User
        from models.city import City
        from models.state import State
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        return {
            "BaseModel": BaseModel,
            "User": User,
            "City": City,
            "State": State,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }

    def reload(self):
        """Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists"""

        if not os.path.exists(FileStorage.__file_path):
            return

        with open(FileStorage.__file_path, "r") as f:
            json_dict = json.load(f)
            for vals in json_dict.values():
                cls = self.class_list()[vals['__class__']]
                self.new(cls(**vals))
