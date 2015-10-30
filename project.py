__author__ = 'poojm'
from flask import Flask, request, redirect
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
    output = ""
    if restaurant:
        # list out all menu items, prices, descriptions
        output += "To add a new item, click <a href='/restaurants/{0}/new'>here</a><br><br>".format(restaurant_id)
        menuItems = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant.id).all()
        for item in menuItems:
            output += item.name
            output += " <a href='/restaurants/{0}/items/{1}/edit/'>Edit</a>".format(restaurant_id, item.id)
            output += "<br>"
            output += item.price
            output += "<br>"
            output += item.description
            output += "<br><br>"
    else:
        output += "no restaurant found"
    return output

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
        return redirect('/restaurants/%d/' % restaurant_id, 302)
    else:
        output = ""
        output += "<h2>Enter a new item for %s</h2>" % restaurant.name
        output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/new/'><br>" % restaurant_id
        output += "Name: <input name='item_name' type='text' ><br>"
        output += "Price: <input name='item_price' type='text' ><br>"
        output += "Description: <input name='item_description' type='text' ><br>"
        output += "Course: <input name='item_course' type='text' ><br>"
        output += "<input type='submit' value='Add!'> </form>"
        output += "</body></html>"
        return output

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/items/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    item = session.query(MenuItem).filter(MenuItem.id == menu_id).one()

    if request.method == 'POST':
        session.query(MenuItem).filter(MenuItem.id == menu_id).update({MenuItem.name: request.form['new_name']}, synchronize_session=False)
        session.commit()

        return redirect('/restaurants/%d/' % restaurant_id, 302)
    else:
        output = ""
        output += "Edit the {0} item for {1}".format(item.name, restaurant.name)
        output += "<br>"
        output += "Enter a new name:<br>"
        output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/{0}/items/{1}/edit/'><br>".format(restaurant_id, menu_id)
        output += "<input name='new_name' type='text'><br>"
        output += "<input type='submit' value='Submit'><br>"
        output += "</form>"
        return output

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)