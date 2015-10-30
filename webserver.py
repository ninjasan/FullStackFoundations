__author__ = 'poojm'

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import re
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
                output += "<h2>What would you like me to say?</h2>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form>"
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
                output += "<h2>What would you like me to say?</h2>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hola'>"
                output += "<input name='message' type='text' >"
                output += "<input type='submit' value='Submit'></form>"
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
                    output += "<a href='/restaurants/%s/edit'>Edit Name</a></br>" % restaurant.id
                    output += "<a href='/restaurants/%s/delete'>Remove</a></br>" % restaurant.id
                    output += "</p>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h2>Enter a name</h2>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='message' type='text' >"
                output += "<input type='submit' value='Create'> </form>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/edit'):
                addrParts = self.path.split('/')
                curRestaurant = session.query(Restaurant).filter(Restaurant.id == addrParts[2]).one()
                print curRestaurant

                #form to rename restaurant
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h2>Enter a new name for %s</h2>" % curRestaurant.name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % addrParts[2]
                output += "<input name='updateName' type='text' >"
                output += "<input type='submit' value='Update'> </form>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/delete'):
                print "got to the delete page!"
                addrParts = self.path.split('/')
                curRestaurant = session.query(Restaurant).filter(Restaurant.id == addrParts[2]).one()
                print curRestaurant

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h2>Confirm you'd like to delete %s</h2>" % curRestaurant.name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % addrParts[2]
                output += "<input type='submit' value='Delete'> </form>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, "File NOT found")
    def do_POST(self):
        try:
            if self.path.endswith("/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                addNewRestaurant = Restaurant(name = messagecontent[0])
                session.add(addNewRestaurant)
                session.commit()

                #redirect
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            if self.path.endswith("/edit"):
                print "trying to post new name..."
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('updateName')

                print "New name: %s" % messagecontent[0]
                addrParts = self.path.split('/')
                session.query(Restaurant).filter(Restaurant.id == addrParts[2]).update({Restaurant.name: messagecontent[0]}, synchronize_session=False)
                session.commit()

                print "committed!"

                #redirect
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            if self.path.endswith("/delete"):
                print "trying to delete..."
                addrParts = self.path.split('/')
                curRestaurant = session.query(Restaurant).filter(Restaurant.id == addrParts[2]).one()
                session.delete(curRestaurant)
                session.commit()

                print "deleted!"

                #redirect
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            if self.path.endswith("/hello"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += "<h2>What would you like me to say?</h2>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2>What would you like me to say?</h2>"
                output += "<input name='message' type='text' >"
                output += "<input type='submit' value='Submit'> </form>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
            if self.path.endswith("/hola"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += "<h2>What would you like me to say?</h2>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hola'>"
                output += "<h2>What would you like me to say?</h2>"
                output += "<input name='message' type='text' >"
                output += "<input type='submit' value='Submit'> </form>"
                output += "</body></html>"

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