__author__ = 'poojm'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()
session.query(Restaurant).all()

cheesepizza = MenuItem(name="Cheese Pizza",
                        description="Made with all natural ingredients and fresh mozzarella",
                        course="Entree",
                        price="$8.99",
                        restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()
session.query(MenuItem).all()

firstResult = session.query(MenuItem).first()
print firstResult.name

items = session.query(MenuItem).all()
for item in items:
    print item.name

veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger').all()
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"

UrbanVeggieBurger = session.query(MenuItem).filter_by(id=11).one()
print UrbanVeggieBurger.price
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()
print UrbanVeggieBurger.price