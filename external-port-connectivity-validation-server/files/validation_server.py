#! /usr/bin/env python

# Needs to run the server on the port provided
# Need a get request on the /ping url that response with pong
# Need a get request on the /exit url that kills the python process

import os
import sys
try:
    from ansible.module_utils.basic import *
except:
    pass

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

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
    print("Test server ready; use /check to test connection; use /done to shutdown.")
    httpd.serve_forever()


def main():
    module = AnsibleModule(
        argument_spec = dict(
            port = dict(required = True, type='str'),
            ip = dict(required = True, type='str')
        )
    )

    run(module.param['ip'], int(module.params['port']))

    module.exit_json(changed =  True)


if __name__ == '__main__':
    if sys.argv[1] != None and sys.argv[2] != None:
        port = int(sys.argv[2])
        ip = sys.argv[1]
        run(ip, port)
    else:
        main()
