#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel

# new imports for phase 2
from os import getenv
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    state_id = Column(String(60), ForeignKey("states_id"), nullable=False)
    name = Column(String(60), nullable=False)
    places = relationship(
        'Place',
        backref='cities',
        cascade="all, delete-orphan")
