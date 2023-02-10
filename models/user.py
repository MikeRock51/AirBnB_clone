#!/usr/bin/python3
"""The user class model"""

from models.base_model import BaseModel

class User(BaseModel):
    """The user class"""

    # def __init__(self, *args, **kwargs):
    #     """User object constructor"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
