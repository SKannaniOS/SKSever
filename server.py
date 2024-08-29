from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import os

from get_request_mixin import GetRequestMixin
from post_request_mixin import PostRequestMixin

script_dir = os.path.dirname(os.path.realpath(__file__))

# HTTPRequestHandler class
class RequestHandler(PostRequestMixin, GetRequestMixin, BaseHTTPRequestHandler):
    def do_POST(self):
        cleaned_path = self.path.replace('/v1/batch', '')
        if cleaned_path == '/submit':
            self.handle_post_request()
        else:
            self.send_error(404, 'Not Found\n')
    
    def do_GET(self):
        self.handle_get_request()

# Function to start the server
def start_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting server on port', port)
    httpd.serve_forever()

# Run the server on port from 0 to 65535 (since port is 16-bit number)
if __name__ == '__main__':
    start_server(12791)

# ------------------------------------------------------------ #
# to start the server, run the following command:
# python3 server.py

# To start tunneling, run the following command:
# ssh -p 443 -R0:localhost:12791 a.pinggy.io
# ------------------------ or -------------------------------- #
# ssh -R 80:localhost:12791 serveo.net
# ------------------------------------------------------------ #