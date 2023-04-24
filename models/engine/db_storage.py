#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from ..base_model import Base, BaseModel
from os import getenv
from sqlalchemy import create_engine, inspect

HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
HBNB_MYSQL_PORT = getenv('HBNB_MYSQL_PORT')
HBNB_ENV = 'dev'


class DBStorage:
    """This class manages storage of hbnb . in database"""
    __engine = None
    __session = None

    def __init__(self):
        """initializes the database"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(HBNB_MYSQL_USER, HBNB_MYSQL_PWD,
                                              HBNB_MYSQL_HOST, HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all instances of a given class"""
        from ..user import User
        from ..state import State
        from ..city import City
        from ..place import Place
        from ..review import Review
        from ..amenity import Amenity

        result_dict = {}
        for model in [User, State, City, Place, Amenity, Review]:
            if cls is not None and model != cls:
                continue
            query_results = self.__session.query(model).all()
            for obj in query_results:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                result_dict[key] = obj
        return result_dict

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception:
                self.__session.rollback()

    def save(self):
        """Saves storage dictionary to file"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Loads storage dictionary from file"""
        from ..user import User
        from ..state import State
        from ..city import City
        from ..place import Place
        from ..review import Review
        from ..amenity import Amenity

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """calls remove() method on the private
        session attribute (self.__session)"""
        self.__session.close()
