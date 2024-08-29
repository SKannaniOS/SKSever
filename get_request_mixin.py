import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

class GetRequestMixin(BaseHTTPRequestHandler):
    def handle_get_request(self):
        # Handle GET request
        parsed_url = urlparse(self.path)
        parsed_path = parsed_url.path
        if parsed_path == "/sourceConfig":
            response_data = self.read_json_file('sample_config.json')
            self.send_success(json.dumps(response_data))
        else:
            self.send_error(404, 'Configuration file not found.\n')
            self.end_headers()

    def read_json_file(self, filepath):
        with open(filepath, 'r') as file:
            return json.load(file)

    def send_success(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

    def send_error(self, status_code, message=None, explain=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))