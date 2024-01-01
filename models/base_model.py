#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime

# imports for phase 2
from os import getenv
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# setting up SQLAlchemy and determining storage type.
Base = declarative_base()
storage_type = getenv('HBNB_TYPE_STORAGE')


class BaseModel:
    """A base class for all hbnb models"""

    # new defenitions for using SQLAlchemy
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new base model"""

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs:
            for k in kwargs:
                if k in ['created_at', 'updated_at']:
                    s = "%Y-%m-%dT%H:%M:%S.%f"
                    setattr(
                        self, k,
                        datetime.strptime(
                            kwargs[k], s))
                elif k != '__class__':
                    setattr(self, k, kwargs[k])
                if not hasattr(kwargs, 'id'):
                    setattr(self, 'id', str(uuid.uuid4()))
                if not hasattr(kwargs, 'created_at'):
                    setattr(self, 'created_at', datetime.now())
                if not hasattr(kwargs, 'updated_at'):
                    setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """Returns a string representation of the instance"""
        objs = self.__dict__.copy()
        objs.pop("__sa_instance_state", None)
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, objs)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        objs = {}
        objs.update(self.__dict__)
        objs.update({
            '__class__': (str(type(self)).split('.')[-1]).split('\'')[0]
            })
        objs['created_at'] = self.created_at.isoformat()
        objs['updated_at'] = self.updated_at.isoformat()
        return objs

    def delete(self):
        """delete the current instance"""
        from models import storage
        storage.delete(self)
