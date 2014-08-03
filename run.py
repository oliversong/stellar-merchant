# runs the app obviously

import tornado.web
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from app import app

print("""

    Stellar merchant application

""")

if app.config['ENV'] == 'development':
    if __name__ == "__main__":
        app.run()
else:
    wsgi_app = WSGIContainer(app)
    http_server = HTTPServer(wsgi_app)
    print "Listening on port 5000."
    http_server.listen(5000)
    IOLoop.instance().start()
