#!/usr/bin/python3
"""This module defines a class to manage Database storage for hbnb clone"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


user = os.environ.get('HBNB_MYSQL_USER')
password = os.environ.get('HBNB_MYSQL_PWD')
host = os.environ.get('HBNB_MYSQL_HOST', 'localhost')
database = os.environ.get('HBNB_MYSQL_DB')

class DBStorage:
    """This class manages storage of hbnb models in SQL Database"""
    
    __engine = None
    __session = None


    def __init__(self):
        """Initialize the DB Storage class"""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                user,
                password,
                host,
                database),
            pool_pre_ping=True
        )
        hbnb_env = os.environ.get('HBNB_ENV')
        if (hbnb_env == 'test'):
            Base.metadata.drop_all(self.__engine)

        
    def all(self, cls=None):
        """Retrives All Objects from the Database"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
        objects = {}

        if cls is not None:
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for cls in [State, City, User, Place, Review, Amenity]:
                clss.extend(self.__session.query(cls).all())

        # Add all objects to dict
        for obj in objs:
            key = "{}.{}".format(
                obj.__class__.__name__,
                obj.id
                )
            objects[key] = obj
        return objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__session.add(obj)

    def save(self):
        """Saves storage dictionary to database"""
        self.__session.commit()

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=True
            )
        )
        self.__session = Session()


    def delete(self, obj=None):
        """
            delete obj from __objets if it's inside
            if obj is equal to None, do nothing
        """
        if (obj):
            self.__session.delete(obj)

    def close(self):
        """closes the current db session"""
        self.__session.close()