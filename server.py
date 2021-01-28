#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        data = self.data.split()
        print(data[1])
        #f = read_index_html("./www")
        #self.request.sendall(f)
        if data[1].decode("utf-8").split('.')[1] == '.csv':
            self.good_request_css()
        else:
            self.good_request_html()

    def good_request_html(self):
        data = self.data.split()
        f = read_index(data[1])
        self.request.sendall(bytearray('HTTP/1.1 200 OK\n','utf-8'))
        self.request.sendall(bytearray('Content-Type: text/html\n','utf-8'))
        self.request.sendall(bytearray(f,'utf-8'))

    def good_request_css(self):
        data = self.data.split()
        f = read_index(data[1])
        self.request.sendall(bytearray('HTTP/1.1 200 OK\n','utf-8'))
        self.request.sendall(bytearray('Content-Type: text/css\n','utf-8'))
        self.request.sendall(bytearray(f,'utf-8'))

def read_index(location):
    location = '.'+location.decode("utf-8") #append ./www later I think
    f = open(location, 'r')
    html = f.read()
    f.close()
    return html

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
