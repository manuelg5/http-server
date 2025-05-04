from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
import os
from urllib.parse import urlparse

DATA_FILE = "checkins.json"
PORT = 8080

# Load previous check-ins if available
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        checkins = json.load(f)
else:
    checkins = []

class MyHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='text/html'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def log_message(self, format, *args):
        with open("access.log", "a") as f:
            f.write("%s - - [%s] %s\n" % (
                self.client_address[0],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                format % args
            ))

    def do_GET(self):
        parsed_path = urlparse(self.path).path

        if parsed_path == '/':
            self._set_headers()
            self.wfile.write(b"""
                <html>
                <head><title>Custom Server</title></head>
                <body>
                    <h1>Welcome to My HTTP Server</h1>
                    <p>Visit <a href='/api/status'>/api/status</a> to see JSON output.</p>
                    <p>Visit <a href='/dashboard'>/dashboard</a> to view check-in dashboard.</p>
                </body>
                </html>
            """)

        elif parsed_path == '/api/status':
            self._set_headers(200, 'application/json')
            response = {
                "status": "online",
                "timestamp": datetime.now().isoformat(),
                "message": "Server is running great!"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif parsed_path == '/api/checkins':
            self._set_headers(200, 'application/json')
            self.wfile.write(json.dumps(checkins[-50:], indent=2).encode('utf-8'))

        elif parsed_path == '/dashboard':
            self._set_headers(200, 'text/html')
            table = "".join(
                f"<tr><td>{c['client_id']}</td><td>{c['status']}</td><td>{c['timestamp']}</td></tr>"
                for c in reversed(checkins[-50:])
            )
            html = f"""
                <html>
                <head><title>Check-In Dashboard</title></head>
                <body>
                    <h1>Recent Device Check-Ins</h1>
                    <table border="1">
                        <tr><th>Client ID</th><th>Status</th><th>Timestamp</th></tr>
                        {table}
                    </table>
                </body>
                </html>
            """
            self.wfile.write(html.encode('utf-8'))

        else:
            self._set_headers(404)
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        parsed_path = urlparse(self.path).path

        if parsed_path == '/api/checkin':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                client_id = data.get("client_id")
                status = data.get("status", "unknown")
                timestamp = data.get("timestamp") or datetime.now().isoformat()

                if not client_id:
                    raise ValueError("Missing client_id")

                entry = {
                    "client_id": client_id,
                    "status": status,
                    "timestamp": timestamp
                }
                checkins.append(entry)

                with open(DATA_FILE, "w") as f:
                    json.dump(checkins, f, indent=2)

                self._set_headers(201, 'application/json')
                self.wfile.write(json.dumps({"message": "Check-in recorded"}).encode('utf-8'))

            except Exception as e:
                self._set_headers(400, 'application/json')
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

        else:
            self._set_headers(404)
            self.wfile.write(b"404 Not Found")

# Start the server
server_address = ('0.0.0.0', PORT)
httpd = HTTPServer(server_address, MyHandler)
print(f"🚀 Serving on http://localhost:{PORT}")
httpd.serve_forever()
