class Response:
    def __init__(self):
        self.body = ""
        self.headers = []
        self.status = "200 OK"
    
    def __call__(self, environ, start_response):
        start_response(self.status, self.headers)
        return [self.body.encode("utf-8")]