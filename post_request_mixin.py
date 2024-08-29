import json
import os
from http.server import BaseHTTPRequestHandler

class PostRequestMixin(BaseHTTPRequestHandler):
    def handle_post_request(self):
        # Read POST data
        if self.path == '/submit/v1/batch':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
        
            # Handle JSON data
            try:
                data = json.loads(post_data.decode('utf-8'))
            except ValueError as e:
                self.send_error(400, 'Error decoding JSON\n')
                print("Error decoding JSON:", e)
                return

            # Handle response
            print("Received data:", data)
            self.handle_response(data)
            self.send_success('Received data successfully\n')
        else:
            self.send_error(404, 'Not Found_1\n')

    def handle_response(self, json_data):
        batch = json_data.get('batch')
        batch_content = ""
        if batch:
            for event in batch:
                event_name = event.get('event')
                if event_name:
                    batch_content += event_name
                    batch_content += '\n'
                    
        self.write_batch_event_content(batch_content)
    
    def write_batch_event_content(self, content):
        print("Writing batch content to file:", content)
        script_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(script_dir, 'batch_content.txt'), 'a') as f:
            f.write(content + '\n')

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