#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class """

    if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade='all, delete', backref='state')
    else:
        name = ""
        cities = []

    @property
    def cities(self):
        """A getter for the attribute cities"""
        from models import storage
        from models.city import City
        cities = storage.all(City)
        result = []

        for city in cities.values():
            if city.state_id == self.id:
                result.append(city)

        return result
