__author__ = 'poojm'

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161 Hola! <a href='/hello'>Back to Hello</a>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "Add a new restaurant <a href='/restaurants/new'>here</a>"
                for restaurant in restaurants:
                    print restaurant.name
                    output += "<p>"
                    output += "Name: %s</br>" % restaurant.name
                    output += "<a href='/restaurant/%s/edit/'>Edit Name</a></br>" % restaurant.id
                    output += "<a href='/restaurant/%s/remove/'>Remove</a></br>" % restaurant.id
                    output += "</p>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'><h2>Enter a name</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"

                #form to create new one
                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/restaurant/id/edit'):
                #form to rename restaurant
                return
            if self.path.endswith('/restaurant/confirm'):
                #if you click submit restaurant will be deleted
                return
        except IOError:
            self.send_error(404, "File NOT found")
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            addNewRestaurant = Restaurant(name = messagecontent[0])
            session.add(addNewRestaurant)
            session.commit()

            restaurants = session.query(Restaurant).all()
            output = ""
            output += "<html><body>"
            output += "Add a new restaurant <a href='/restaurants/new'>here</a>"
            for restaurant in restaurants:
                print restaurant.name
                output += "<p>"
                output += "Name: %s</br>" % restaurant.name
                output += "<a href='/restaurant/%s/edit/'>Edit Name</a></br>" % restaurant.id
                output += "<a href='/restaurant/%s/remove/'>Remove</a></br>" % restaurant.id
                output += "</p>"
            output += "</body></html>"
            #output = ""
            #output += "<html><body>"
            #output += " <h2> Okay, how about this: </h2>"
            #output += "<h1> %s </h1>" % messagecontent[0]
            #output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #output += "</body></html>"
            self.wfile.write(output)
            print output
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "Encountered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()