from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from cgi import parse_header
import time
import json
import socket
import os

hostName = "0.0.0.0"
serverPort = 8888
api_success = True
api_key = ""
redis_password = ""

class MyServer(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _set_headers(self, response_code=200):
        self.send_response(response_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,HEAD,PUT,PATCH,POST,DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_HEAD(self):
        global api_success
        match self.path:
            case "/":
                self._set_headers()
            case "/application/health":
                self._set_headers()
            case "/api":
                if api_success :
                  self._set_headers(200)
                else :
                  self._set_headers(500)
            case "/api/switch" :
                self._set_headers(200)
                api_success = not api_success
            case "/hostname":
                self._set_headers(200)
                response = "{ 'hostname' : '" + str(socket.gethostname()) + "'  }"
                self.wfile.write(json.dumps(response).encode('utf-8'))
            case _:
                self._set_headers(404)

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        global api_success
        match self.path:
            case "/":
                self._set_headers()
            case "/application/health":
                self._set_headers()
            case "/api":
                if api_success :
                  self._set_headers(200)
                else :
                  self._set_headers(500)
            case "/api/switch" :
                self._set_headers(200)
                api_success = not api_success
            case "/hostname":
                self._set_headers(200)
                response = "{ 'hostname' : '" + str(socket.gethostname()) + "'  }"
                self.wfile.write(json.dumps(response).encode('utf-8'))
            case "/env":
                self._set_headers(200)
                response = "{ 'app_name' : '" + str(os.environ["APP_NAME"]) + "', 'app_env' : '" + str(os.environ["APP_ENV"]) + "'}"
                self.wfile.write(json.dumps(response).encode('utf-8'))
            case "/secret":
                self._set_headers(200)
                global api_key
                global redis_password
                response = "{ 'api_key' : '" + api_key + "', 'redis_password' : '" + redis_password + "'}"
                self.wfile.write(json.dumps(response).encode('utf-8'))
            case "/header":
                self._set_headers(200)
                response = {}
                for header in self.headers :
                  response[header] = self.headers[header]
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

    try:
        f = open('/secret/secret.json')
    except FileNotFoundError:
        print('secret.json not found')
    else:
        with f:
            d = json.load(f)
            api_key = d["API_KEY"]
            redis_password =  d["REDIS_PASSWORD"]
      
    
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
# Testing tag
