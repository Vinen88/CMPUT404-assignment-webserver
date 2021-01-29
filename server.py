#  coding: utf-8 
import socketserver
import os.path

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
        if data[0].decode("utf-8") != 'GET':
            self.bad_request_method()
        elif data[1].decode("utf-8")[-1] == '/':
            self.good_request_html(data[1]+(b'index.html'))
        elif '.css' not in data[1].decode("utf-8") and '.html' not in data[1].decode("utf-8") and data[1].decode("utf-8")[-1] != '/':
            self.redirect_request(data)
        elif data[1].decode("utf-8") == "favicon.ico": #need to do this better
            self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n','utf-8'))
        elif ".css" in data[1].decode("utf-8"):
            self.good_request_css(data[1])
        elif ".html" in data[1].decode("utf-8"):
            self.good_request_html(data[1])
        else:
            self.bad_request()

    def redirect_request(self,data):
        #check if request is valid dir somewhere
        #add / at the end of whatever dir
        #send 30- code and correct address
        f = read_index(data[1]+b'/index.html')
        if f == False:
            self.bad_request()
            return
        self.request.sendall(bytearray('HTTP/1.1 302 Found\r\n','utf-8'))
        self.request.sendall(data[6]+data[1]+b'/')
        self.request.sendall(bytearray('Content-Type: text/html\r\n','utf-8'))
        self.request.sendall(bytearray(f,'utf-8'))

        
    def bad_request_method(self):
        self.request.sendall(bytearray('HTTP/1.1 405 Method not allowed\r\n','utf-8'))
        self.request.sendall(bytearray('Connection: close\r\n', 'utf-8'))

    def good_request_html(self,data):
        f = read_index(data)
        if f == False:
            self.bad_request()
            return
        self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n','utf-8'))
        self.request.sendall(bytearray('Content-Type: text/html\r\n','utf-8'))
        self.request.sendall(bytearray(f,'utf-8'))

    def good_request_css(self,data):
        f = read_index(data)
        if f == False:
            self.bad_request()
            return
        self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n','utf-8'))
        self.request.sendall(bytearray('Content-Type: text/css\r\n','utf-8'))
        self.request.sendall(bytearray(f,'utf-8'))
    
    def bad_request(self):
        print("BAD REQUEST")
        self.request.sendall(bytearray('HTTP/1.1 404 Not Found\r\n','utf-8'))
        self.request.sendall(bytearray('Connection: close\r\n', 'utf-8'))

def read_index(location):
    location = './www'+location.decode("utf-8")
    if '..' in location:
        return False
    print(location)
    if os.path.isfile(location):
        f = open(location, 'r')
        html = f.read()
        f.close()
        return html
    else:
        print("BAD REQUEST IN READ INDEX")
        return False

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
