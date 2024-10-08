from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from cgi import parse_header
import time
import json
import socket

hostName = "0.0.0.0"
serverPort = 8888
api_success_count = 5

class MyServer(BaseHTTPRequestHandler):
    def _set_headers(self, response_code=200):
        self.send_response(response_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,HEAD,PUT,PATCH,POST,DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_HEAD(self):
        global api_success_count
        match self.path:
            case "/":
                self._set_headers()
            case "/application/health":
                self._set_headers()
            case "/api":
                if api_success_count == 0 :
                  self._set_headers(500)
                else :
                  api_success_count = api_success_count - 1
                  self._set_headers(200)
            case "/api/reset" :
                self._set_headers(200)
                api_success_count = 5
            case _:
                self._set_headers(404)

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        global api_success_count
        match self.path:
            case "/":
                self._set_headers()
            case "/application/health":
                self._set_headers()
            case "/api":
                if api_success_count == 0 :
                  self._set_headers(500)
                else :
                  api_success_count = api_success_count - 1
                  self._set_headers(200)
            case "/api/reset" :
                self._set_headers(200)
                api_success_count = 5
            case "/hostname":
                self._set_headers(200)
                response = "{ 'hostname' : '" + str(socket.gethostname()) + "'  }"
                self.wfile.write(json.dumps(response).encode('utf-8'))
            case _:
                self._set_headers(404)
    
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

# Testing
