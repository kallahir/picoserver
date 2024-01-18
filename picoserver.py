import socket

from request import Request
from route import Route
from utils import HTTP_CODES

class PathAlreadyBoundException(Exception):
    pass

class PicoServer:
    def __init__(self, host="0.0.0.0", port=80, buffer_length=4096):
        self._host = host
        self._port = port
        self._routes = {}
        self._socket = None
        self._connect = None
        self._buffer_length = buffer_length 

    def start(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self._host, self._port))
        self._socket.listen(1)
        print("[server start]")
        while True:
            if self._socket is None:
                break
            try:
                self._connect, _ = self._socket.accept()
                r = Request(str(self._connect.recv(self._buffer_length), "utf8")) 
                if r.empty():
                    self._connect.close()
                    continue
                route = self.find_route(r)
                if route:
                    route.handler(r)
                else:
                    self.respond(400, "text/plain", "route not found")
            except Exception as e:
                self.respond(500, "text/plain", str(e))
            except KeyboardInterrupt:
                self.stop()
            finally:
                if self._connect:
                    self._connect.close()

    def stop(self):
        print("[server stopping]")
        if self._connect:
            self._connect.close()
            self._connect = None
        if self._socket:
            self._socket.close()
            self._socket = None
        print("[server stopped]")
    
    def route(self, path, method="GET"):
        def decorator(handler):
            if path in self._routes:
                raise PathAlreadyBoundException()
            self._routes[path] = Route(path, method, handler)
        return decorator
    
    def find_route(self, request: Request):
        if request.path in self._routes:
            route = self._routes[request.path]
            if request.method != route.method:
                return None
            return route 
        return None

    def respond(self, http_status, content_type, content):
        self._connect.sendall(bytes(f"HTTP/1.1 {http_status} {HTTP_CODES[http_status]}\r\nContent-Type: {content_type}\r\n\r\n{content}", "utf8"))
