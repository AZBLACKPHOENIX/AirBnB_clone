#!/usr/bin/python3
"""Module for the BaseModel class."""

import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """BaseModel class definition."""

    def __init__(self, *args, **kwargs):
        """Initialize BaseModel instance."""
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        if len(kwargs) != 0:
            for key, val in kwargs.items():
                if key in {"created_at", "updated_at"}:
                    setattr(self, key, datetime.strptime(val, time_format))
                elif key != '__class__':
                    setattr(self, key, val)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.today()
            self.updated_at = datetime.today()
            models.storage.new(self)

    def save(self):
        """Save BaseModel instance."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return dictionary representation of BaseModel instance."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "__class__": self.__class__.__name__,
        }

    def __str__(self):
        """Return string representation of BaseModel instance."""
        class_name = self.__class__.__name__
        return f"[{class_name}] ({self.id}) {self.__dict__}"
