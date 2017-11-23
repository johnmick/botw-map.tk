import json
import tornado.ioloop
import tornado.web

port_number = 8888
address     = "127.0.0.1"

with open("seeds.json", "r") as f:
    data = json.load(f)

class SeedHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(data))

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/seed-list", SeedHandler)
    ])
    app.listen(port_number, address=address)
    print("Listening for seed requests on 8888")
    tornado.ioloop.IOLoop.current().start()
