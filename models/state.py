#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel

# new imports for phase 2
from os import getenv
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class State(BaseModel):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='cities', cascade="all, delete")

    if getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def cities(self):
            cities = storage.all(City).values()
            cities_list = []
            for city in cities:
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
