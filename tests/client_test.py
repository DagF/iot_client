import socketserver
import json

class IOTClient(socketserver.TCPServer):

    __main_function = None

    def __init__(self, host, port):
        self.allow_reuse_address = True
        super(IOTClient, self).__init__((host, port), RequestHandler)

    def run(self):
        print("serve")
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        self.server_close()

    def main(self, f):
        self.__main_function = f

    def prosessRequest(self, recv):

        return self.__main_function(recv)


class RequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("running")
        recv = self.request.recv(10000).strip()
        print(recv)
        recv = recv.decode("utf-8").split("\r\n")[-1]
        response = self.server.prosessRequest(recv)
        print(response)
        a = bytes(
                json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')),
                'UTF-8'
            )
        self.request.sendall(
            a
        )

HOST = 'localhost'
PORT = 2001
USERNAME = "test"
PASSWORD = "password"

client = IOTClient(host=HOST, port=PORT)

@client.main
def hello_world(request):
    print("New Request")
    print(request)
    return request

if __name__ == '__main__':
    client.run()
