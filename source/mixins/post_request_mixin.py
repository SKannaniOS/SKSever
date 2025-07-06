import json
import os
import time
import random
import gzip
import io

from http.server import BaseHTTPRequestHandler

class PostRequestMixin(BaseHTTPRequestHandler):
    # Configuration flag to enable/disable gzip decompression
    GZIP_ENABLED = True  # Set to False to disable gzip processing
    
    # Handle POST request
    def handle_post_request(self):
        # Read POST data
        if self.path == '/submit/v1/batch':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Check if request is gzip compressed
            content_encoding = self.headers.get('Content-Encoding', '').lower()
            
            # Decompress gzip data if enabled and content is compressed
            if self.GZIP_ENABLED and content_encoding == 'gzip':
                try:
                    # Decompress gzip data
                    post_data = gzip.decompress(post_data)
                    print("✅ Gzip decompression successful")
                except Exception as e:
                    print(f"❌ Gzip decompression failed: {e}")
                    self.send_error(400, 'Error decompressing gzip data\n')
                    return
            elif content_encoding == 'gzip' and not self.GZIP_ENABLED:
                print("⚠️ Gzip compressed request received but gzip processing is disabled")
                self.send_error(400, 'Gzip processing is disabled\n')
                return
        
            # Handle JSON data
            try:
                data = json.loads(post_data.decode('utf-8'))
            except ValueError as e:
                self.send_error(400, 'Error decoding JSON\n')
                print("Error decoding JSON:", e)
                return

            # Handle response
            print("\nReceived data:", data, '\n')
            self.handle_response(data)
        else:
            self.send_error(404, 'Not Found\n')

    # Handle response
    def handle_response(self, json_data):
        batch = json_data.get('batch')
        batch_content = ""
        if batch:
            for event in batch:
                event_name = event.get('event') or event.get('type')
                if event_name:
                    batch_content += event_name
                    batch_content += '\n'
                    
        self.write_batch_event_content(batch_content)

    # Write batch event content to file
    def write_batch_event_content(self, content):
        file_path = self.get_text_file_path('../../output_files/batch_content.txt')
        
        if not self.file_exists(file_path):
            print("File does not exist:", file_path)
            self.send_error(500, 'Server error\n')
            return            

        with open(file_path, 'a') as f:
            f.write(content)
        
        # random_value = random.randint(1, 5)
        # time.sleep(0)
        
        self.send_success('Received data successfully\n')

    # Check if file exists
    def file_exists(self, file_path):
        return os.path.exists(file_path) and os.path.isfile(file_path)
    
    # Get text file path
    def get_text_file_path(self, file_path):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        text_file_path = os.path.join(current_dir, file_path)
        text_file_path = os.path.abspath(text_file_path)
        return text_file_path

    # Send success response
    def send_success(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

    # Send error response
    def send_error(self, status_code, message=None, explain=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))