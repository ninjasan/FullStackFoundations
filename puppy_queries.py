__author__ = 'poojm'

from datetime import timedelta, date
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from puppies_database_setup import Base, Shelter, Puppy

engine = create_engine('sqlite:///shelters.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# 1. Query all of the puppies and return the results in ascending alphabetical order
puppies = session.query(Puppy).order_by(asc('name')).all()
for puppy in puppies:
    print puppy.name

# 2. Query all of the puppies that are less than 6 months old organized by the youngest first
sixMonthsAgo = date.today() - timedelta(days=180)
puppies = session.query(Puppy).filter(Puppy.dateOfBirth > sixMonthsAgo).order_by(desc('dateOfBirth')).all()
for puppy in puppies:
    print puppy.name + ", " + str(puppy.dateOfBirth)

# 3. Query all puppies by ascending weight
puppies = session.query(Puppy).order_by(asc('weight')).all()
for puppy in puppies:
    print puppy.name + ", " + str(puppy.weight)

# 4. Query all puppies grouped by the shelter in which they are staying
puppies = session.query(Puppy).