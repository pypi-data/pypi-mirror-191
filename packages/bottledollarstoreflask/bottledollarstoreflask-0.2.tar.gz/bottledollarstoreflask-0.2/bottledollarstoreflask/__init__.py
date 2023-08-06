### BOTTLE / DOLLAR STORE FLASK ###

from http.server import BaseHTTPRequestHandler, HTTPServer
import os.path
import json

class Bottle:
    paths = []
    posts = []
    class path:                
        def __init__(self, path, content):
            Bottle.paths.append([path, content])
    def renderPage(fileName):
        f = open(os.path.dirname(__file__) + "\..\pages\\" + fileName)
        return f.read()

    class requestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            for i in range(len(Bottle.paths)):
                if(self.path == Bottle.paths[i][0]):
                    self.wfile.write(bytes(Bottle.paths[i][1], "utf-8"))
        def do_POST(self):            
            Bottle.posts.append(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))


    def run(host = "localhost", port = 80):
        server = HTTPServer((host, port), Bottle.requestHandler)
        server.serve_forever()