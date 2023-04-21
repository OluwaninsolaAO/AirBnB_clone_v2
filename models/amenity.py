#!/usr/bin/python3
""" Amenities Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity
import os


class Amenity(BaseModel, Base):
    """ Amenties Class """
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place",
                                   secondary=place_amenity,
                                   backref="amenities")
