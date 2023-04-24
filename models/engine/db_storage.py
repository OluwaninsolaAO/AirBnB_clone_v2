#!/usr/bin/python3
"""Defines a new engine that uses SQLAlchemy"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """DBStorage Engine running on SQLAlchemy"""

    __engine = None
    __session = None

    def __init__(self):
        """class constructor for DBStorage"""

        credentials = ['HBNB_MYSQL_USER', 'HBNB_MYSQL_PWD',
                       'HBNB_MYSQL_HOST', 'HBNB_MYSQL_DB']
        env = [os.environ.get(c) for c in credentials]
        e = 'mysql+mysqldb://{}:{}@{}/{}'.format(*env[:])
        self.__engine = create_engine(e, pool_pre_ping=True)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

        #  drop all tables if the environment variable
        #  HBNB_ENV is equal to test
        if os.environ.get('HBNB_ENV') == 'test':
            from models.base_model import Base
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries the current database session (self.__session)
        for all objects depending of the class name (argument cls)"""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        class_list = [State, City, User, Place, Review, Amenity]
        objs = {}
        if cls is not None:
            for obj in self.__session.query(cls).all():
                objs.update({obj.to_dict()['__class__'] + '.' + obj.id: obj})
        else:
            for class_item in class_list:
                for obj in self.__session.query(class_item).all():
                    key = obj.to_dict()['__class__'] + '.' + obj.id
                    objs.update({key: obj})
        return objs

    def new(self, obj):
        """Add obj to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database
        """
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        from models.base_model import Base

        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """call reload() method for commiting objects to db"""
        self.__session.remove()
