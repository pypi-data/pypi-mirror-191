from http.server import BaseHTTPRequestHandler, HTTPServer
import os.path

class Bottle:
    paths = []
    def path(path, content):
        Bottle.paths.append([path, content])
    def renderPage(fileName):
        f = open(os.path.dirname(__file__) + "\..\pages\\" + fileName)
        return f.read()
    class requestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            print("GET request \nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            for i in range(len(Bottle.paths)):
                if(self.path == Bottle.paths[i][0]):
                    self.wfile.write(bytes(Bottle.paths[i][1], "utf-8"))
        def do_POST(self):
            print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
    def run(host, port):
        server = HTTPServer((host, port), Bottle.requestHandler)
        server.serve_forever()