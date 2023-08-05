class Request:
    def __init__(self, environ):
        self.environ = environ
        self.path = environ["PATH_INFO"]
        self.method = environ["REQUEST_METHOD"]