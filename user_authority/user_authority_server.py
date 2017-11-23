import json
import tornado.ioloop
import tornado.web
from passlib.hash import argon2

user_hashes = {}
class CreateSlateUserHandler(tornado.web.RequestHandler):
  def post(self):
    try:
      username = self.get_argument("username")
      password = self.get_argument("password")
    except:
      self.write("Invalid Request")
      return

    if username not in user_hashes:
      user_hashes[username] = argon2.using(rounds=513).hash(password)
      self.write("Username registered try logging in")
    else:
      self.write("Username already exists")

class LoginHandler(tornado.web.RequestHandler):
  def post(self):
    if self.get_secure_cookie("username"):
      self.write("Welcome back: %s" % str(self.get_secure_cookie("username")))
      return

    try:
      username = self.get_argument("username")
      password = self.get_argument("password")
    except:
      self.write("Invalid Request")
      return

    if username not in user_hashes:
      self.write("Username does not exist")
      return

    if argon2.verify(password, user_hashes[username]):
      self.write("Login by password successful")
      self.set_secure_cookie("username", username)
    else:
      self.write("Invalid password")

class LogoutHandler(tornado.web.RequestHandler):
  def post(self):
    print("Logout called")
    if self.get_secure_cookie("username"):
      self.clear_cookie("username")
      self.write("Cookie Cleared")
      return

if __name__ == "__main__":
    port_number = 8889
    address     = '127.0.0.1'

    app = tornado.web.Application([
        (r"/auth/create-slate-user", CreateSlateUserHandler),
        (r"/auth/login",             LoginHandler),
        (r"/auth/logout",            LogoutHandler)
    ], cookie_secret="TODO_Secret Cookies_TODO")
    app.listen(port_number, address=address)
    print("Listening for user auth requests on %s:%d" % (address,port_number))
    tornado.ioloop.IOLoop.current().start()
