import socketserver

class IOTClient(socketserver.TCPServer):

    __main_function = None

    def __init__(self, host, port):
        socketserver.TCPServer.__init__((host, port), RequesHandler)
        self.serve_forever()

    def main(self, f):
        def wrapper(*args):
            self.__main_function = f
            return f(*args)
        return wrapper

    def prosessRequest(self, recv):
        self.__main_function(recv)


class RequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            recv = self.request.recv(4096)
            self.server.prosessRequest(recv)