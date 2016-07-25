#! /usr/bin/env python

# Needs to run the server on the port provided
# Need a get request on the /ping url that response with pong
# Need a get request on the /exit url that kills the python process

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
from ansible.module_utils.basic import *
from subprocess import call
6
class CheckRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith('/check'):
            self.send_response(200)
        if self.path.endswith('/done'):
            print("Test server has been shutdown.")
            os._exit(0)


def run(ip, port):
    server_address = (ip, port)
    httpd = HTTPServer(server_address, CheckRequestHandler)
    httpd.serve_forever()


def main(port):
    module = AnsibleModule(
            argument_spec = dict(
                    port  = dict(required=True, type='str')
            )
    )
    port = module.params['port']
    run('127.0.0.1', port)



def test():
    run('127.0.0.1', 8000)
    # server_address = ('127.0.0.1', 8000)
    # request_handler = CheckRequestHandler
    # httpd = HTTPServer(server_address, request_handler)
    # httpd.serve_forever(0.2)

if __name__ == '__main__':
    port = sys.argv[1]
    main(port)
