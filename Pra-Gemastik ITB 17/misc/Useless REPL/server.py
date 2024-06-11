#!/usr/bin/env python3

import socketserver
from socket import socket


class IncomingConnection(socketserver.BaseRequestHandler):
    def handle(self):
        super().handle()
        req: socket = self.request
        req.sendall(b">> ")
        while line := req.recv(4096):
            try:
                print(eval(line, {"__builtins__": {}}))
            except Exception as e:
                print(e)
            req.sendall(b">> ")


class ReusableTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    server = ReusableTCPServer(("0.0.0.0", 1337), IncomingConnection)
    server.serve_forever()
