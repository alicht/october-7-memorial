import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import traceback
from pathlib import Path
import os

PORT = 8000

class MemorialHandler(SimpleHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')

    def end_headers(self):
        self.send_cors_headers()
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        try:
            print(f"\nReceived GET request for: {self.path}")

            if self.path == '/':
                self.path = '/newtab.html'
                return super().do_GET()
            elif self.path == '/scrape':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                # Create photos directory if it doesn't exist
                photos_dir = Path('assets/photos')
                photos_dir.mkdir(parents=True, exist_ok=True)

                data = [{
                    "name": "Doron Asher",
                    "age": 33,
                    "headline": "A loving father and dedicated physician",
                    "local_photo": "doron-asher.jpg",  # Local photo file name
                    "bio": "Doron Asher was a dedicated physician who lost his life during the October 7 attack. He was known for his compassionate care of patients and his devotion to his family."
                }]

                # Download photos if they don't exist
                from scripts.download_assets import download_image
                for victim in data:
                    if victim.get('local_photo') and not (photos_dir / victim['local_photo']).exists():
                        image_url = 'https://static.timesofisrael.com/www/uploads/2023/10/WhatsApp-Image-2023-10-08-at-13.44.49.jpeg'
                        download_image(image_url, victim['local_photo'])

                self.wfile.write(json.dumps(data).encode())
                return
            else:
                # Serve static files
                self.path = self.path.lstrip('/')
                print(f"Attempting to serve file: {self.path}")
                return super().do_GET()

        except Exception as e:
            print(f"Error in request handling: {str(e)}")
            print("Traceback:", traceback.format_exc())
            self.send_error(500, str(e))

def run_server():
    try:
        server_address = ('0.0.0.0', PORT)
        httpd = HTTPServer(server_address, MemorialHandler)
        print(f'\nServer starting on http://0.0.0.0:{PORT}')
        print('Ready to handle requests...')
        httpd.serve_forever()
    except Exception as e:
        print(f"Server startup error: {str(e)}")
        print("Traceback:", traceback.format_exc())
        raise

if __name__ == '__main__':
    run_server()