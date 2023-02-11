#!/usr/bin/python3
"""The review model"""

from models.base_model import BaseModel


class Review(BaseModel):
    """The review class"""

    place_id = ""
    user_id = ""
    text = ""
