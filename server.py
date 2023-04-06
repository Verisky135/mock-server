from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from cgi import parse_header
import time
import json

hostName = "0.0.0.0"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def _set_headers(self, response_code=200):
        self.send_response(response_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,HEAD,PUT,PATCH,POST,DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        match self.path:
            case "/":
                self._set_headers()
    
    def do_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        match self.path:
            case "/sleep": 
                self._set_headers()
                request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                sleep = request["sleep"]
                time.sleep(sleep)
                response = "{ 'sleep' : '" + str(sleep) + "'  }"
                self.wfile.write(json.dumps(response).encode('utf-8'))
            case _:
                self._set_headers(404)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == "__main__":
    # Start server
    webServer = ThreadedHTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")