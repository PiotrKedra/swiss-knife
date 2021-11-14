import http.server 
import socketserver
import socket


class CustomHandler(http.server.BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("Hello world".format(self.path).encode('utf-8'))


def run(server_class=http.server.HTTPServer, handler_class=CustomHandler):

    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.setsockopt(socket.SOL_SOCKET, 25, str("swissknife0" + '\0').encode('utf-8')) 

    server_address = ('', 8004)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()