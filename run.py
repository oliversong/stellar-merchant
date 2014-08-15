# runs the app obviously

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging
from app import app

if app.config['ENV'] == 'development':
    if __name__ == "__main__":
        app.run()
else:
    enable_pretty_logging()
    wsgi_app = WSGIContainer(app)
    http_server = HTTPServer(wsgi_app)
    print "Listening on port 5000."
    http_server.listen(5000)
    IOLoop.instance().start()
