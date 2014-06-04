# minimal HTTP server serving both files
# and JSONP request/responses

import SocketServer
import SimpleHTTPServer
import urllib

PORT = 8000

class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def _set_headers(self, theContentType = 'text/html'):
        self.send_response(200)
        self.send_header('Content-type', theContentType)
        self.end_headers()

    def do_GET(self):
        theFile = self.path
        theFile = theFile[1:] # first character is a slash, we take that away

        print "requested ", self.path

        if "jsonp/" in theFile:
        	# extract the callback name
        	callbackName = theFile.split("?callback=",1)[1].split("&",1)[0]
        	self._set_headers('application/json')
        	self.wfile.write(callbackName + "({'firstName':'John' , 'lastName':'Doe'})")

        elif "index" in theFile:
            self._set_headers()
            self.copyfile(urllib.urlopen(theFile), self.wfile)

        else:
            self._set_headers()
            self.wfile.write("")

httpd = SocketServer.ForkingTCPServer(('', PORT), Proxy)
print "serving at port", PORT
httpd.serve_forever()