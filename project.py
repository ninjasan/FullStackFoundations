__author__ = 'poojm'
from flask import Flask, request, redirect, render_template
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    # get first restaurant
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    menuItems = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant.id).all()
    return render_template('menu.html', restaurant=restaurant, items=menuItems)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['item_name'],
                        description=request.form['item_description'],
                        course=request.form['item_course'],
                        price=request.form['item_price'],
                        restaurant = restaurant)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant.id))
    else:
        return render_template('NewMenuItem.html', restaurant=restaurant)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/items/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    item = session.query(MenuItem).filter(MenuItem.id == menu_id).one()

    if request.method == 'POST':
        session.query(MenuItem).filter(MenuItem.id == menu_id).update({MenuItem.name: request.form['new_name']}, synchronize_session=False)
        session.commit()

        return redirect(url_for('restaurantMenu', restaurant_id=restaurant.id))
    else:
        return render_template('EditMenuItem.html', restaurant=restaurant, item=item)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/items/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    item = session.query(MenuItem).filter(MenuItem.id == menu_id).one()

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant.id))
    else:
        return render_template('deletemenuitem.html', restaurant=restaurant, item=item)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)