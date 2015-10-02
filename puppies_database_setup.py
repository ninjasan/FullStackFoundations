__author__ = 'poojm'

import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250))
    city = Column(String(250))
    state = Column(String(2))
    email = Column(String(100))

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    dateOfBirth = Column(Date)
    gender = Column(String(7), nullable=False)
    weight = Column(Integer)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)

engine = create_engine('sqlite:///shelters.db')
Base.metadata.create_all(engine)
