from http.server import *

import _socket


class HTTPServerException(Exception):
    # HTTPServer Exception Class
    pass


class UploadCurrentDirectory(object):
    def Create(self, host: str, port: int):
        try:
            self.Server = HTTPServer((host, port), SimpleHTTPRequestHandler)
        except HTTPServerException as ex:
            print(str(ex))

    def get_all_req(self):
        try:
            return self.Server.get_request()
        except HTTPServerException as ex:
            print(str(ex))

    def run_forever(self):
        try:
            self.Server.serve_forever()
        except HTTPServerException as ex:
            print(str(ex))

    def getServerByPort(self):
        try:
            return self.Server.server_port
        except HTTPServerException as ex:
            print(str(ex))

    def close_server(self):
        try:
            self.Server.server_close()
        except HTTPServerException as ex:
            print(str(ex))