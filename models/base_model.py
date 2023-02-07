#!/usr/bin/python3
"""This module contains the base class for our project"""

import uuid
from datetime import datetime

class BaseModel:
    """Base class for our project"""
    
    def __init__(self, *args, **kwargs):
        """Base object constructor"""

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def __str__(self):
        """Overrides the default __str__ method"""
        return ("[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__))

    
