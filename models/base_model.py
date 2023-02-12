#!/usr/bin/python3
"""This module contains the base class for our project"""

import uuid
from datetime import datetime
from copy import copy
from models import storage


class BaseModel:
    """Base class for our project"""

    def __init__(self, *args, **kwargs):
        """Base class object constructor

        Args:
            args: a list of arguments
            kwargs: A dictionary of key/value arguments
        """

        if kwargs != {}:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == "created_at" or key == "updated_at":
                        value = datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Overrides the default __str__ method"""
        return ("[{}] ({}) {}".format(type(self).__name__,
                                      self.id, self.__dict__))

    def save(self):
        """Updates the 'updated_at' variable with the current datetime"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary representation of an instance"""

        instance = copy(self.__dict__)
        instance['__class__'] = type(self).__name__
        instance['created_at'] = instance['created_at'].strftime(
            "%Y-%m-%dT%H:%M:%S.%f")
        instance['updated_at'] = instance['updated_at'].strftime(
            "%Y-%m-%dT%H:%M:%S.%f")
        return instance
