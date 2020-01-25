#  coding: utf-8 
import socketserver
import os

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
        redirect = False

        self.data = self.request.recv(1024).strip().decode("utf-8")
        if self.data != "":
            print("Got a request of: %s\n" % self.data)

            try:
                request, _ = self.data.split('\r\n', 1)
            except ValueError:
                pass

            try:
                method, path, protocol = request.split()
            except AttributeError:
                pass

            header = protocol + " "

            if method == "GET":

                if path[-1] == "/":
                    path += "index.html"
                elif path[-1] != "/" and '.' not in path:
                    path += "/index.html"
                    redirect = True

                extension = path.split(".")[-1]
                if extension == "html":
                    mimetype = 'text/html'
                elif extension == "css":
                    mimetype = 'text/css'

                try:
                    f = open("./www" + path, "r").read()
                    if redirect:
                        header += "301 Moved Permanently\r\n" + path 
                    else:
                        header += "200 OK\r\n" + "Content-Type: " + mimetype + "\r\nContent Length: " + str(len(f))
                    header += "\r\n"

                    self.request.sendall(bytearray(header + f,'utf-8'))
                except FileNotFoundError:
                    header += "404 Not Found"
                    header += "\r\n"

                    self.request.sendall(bytearray(header,'utf-8'))
            
            else:
                header += "405 Method Not Allowed"
                header += "\r\n"

                self.request.sendall(bytearray(header,'utf-8'))

            redirect = False


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()