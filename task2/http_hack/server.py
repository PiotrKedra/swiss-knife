#!/usr/bin/python
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import codecs

home = './responses/home.html'
send = './responses/send.json'


def get_network_settings():
    with open('network_settings.txt') as json_file:
        data = json.load(json_file)
        return data


class handleRoutes(BaseHTTPRequestHandler):
    def performGetRequest(self):
        if self.path == '/home':
            f = codecs.open(home, 'rb')
            self.sendResponse(f.read(), 200, 'text/html')
            f.close()
            return

    def performPostRequest(self):
        if self.path == '/send':
            f = codecs.open(send, 'rb')
            self.sendResponse(f.read(), 200, 'application/json')
            f.close()
            return
        else:
            return self.sendResponse('Not found.', 404, 'text/plain')

    def sendResponse(self, res, status, type):
        self.send_response(status)
        self.send_header('Content-type', type)
        self.end_headers()
        self.wfile.write(res)
        return


def main():
    network_settings = get_network_settings()

    addr = ("169.254.68.39", network_settings['port'])
    server = HTTPServer(addr, handleRoutes)
    server.serve_forever()


if __name__ == '__main__':
    main()
