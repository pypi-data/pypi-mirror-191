from parse import parse

from .util import Request, Response
from .middleware import Middleware

class Glask:
    def __init__(self):
        self.routes = {}
        self.middleware = Middleware(self)

    def __call__(self, environ, start_response):
        return self.middleware(environ, start_response)

    def route(self, path):
        assert path not in self.routes, "Such route already exists."

        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request.path)
        if handler != None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def default_response(self, response):
        response.status = "404 Not Found"
        response.body = "Not Found"

    def add_middleware(self, middleware):
        self.middleware.add(middleware)