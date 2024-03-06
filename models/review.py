#!/usr/bin/python3
from models.base_model import BaseModel

class Review(BaseModel):
    """Review class inherits from BaseModel and represents a review."""
    place_id = ""
    user_id = ""
    text = ""
