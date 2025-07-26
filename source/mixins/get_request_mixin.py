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
            response_data = self.read_json_file('json_files/sample_config.json')
            self.send_success(json.dumps(response_data))
        elif parsed_path == "/denylist":
            response_data = self.read_js_function('sample_files/denylist.js')
            self.send_success(response_data)
        else:
            self.send_error(404, 'Configuration file not found.\n')
            self.end_headers()

    def read_json_file(self, filepath):
        with open(filepath, 'r') as file:
            return json.load(file)

    def read_file(self, filepath):
        with open(filepath, 'r') as file:
            return file.read()

    def read_js_function(self, filepath):
        with open(filepath, 'r') as file:
            content = file.read()
        
        # Find the start of the function
        lines = content.split('\n')
        function_lines = []
        in_function = False
        
        for line in lines:
            # Skip comment blocks
            stripped_line = line.strip()
            if stripped_line.startswith('/***') or stripped_line.startswith('***') or stripped_line.startswith('***/'):
                continue
            if stripped_line.startswith('*') and 'function' not in line:
                continue
            
            # Start capturing when we find any function declaration
            if 'function transformEvent' in line or 'export function' in line:
                in_function = True
            
            if in_function:
                function_lines.append(line)
        
        return '\n'.join(function_lines)

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