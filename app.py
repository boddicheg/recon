import os
import json
from bottle import route, run, request, response

from modules.SyncScanUtils import *

ROOT = os.path.dirname(os.path.abspath(__file__))
ALLOWED_ACTIONS = ["ip", "waf", "geo", "dirs", "os", "ports"]

#-----------------------------------------------
class Server:
    def __init__(self) -> None:
        self.is_busy = False
        self.config = {}
        self.data = {}
    
    def go(self, config):
        self.config = config
    
    def status(self):
        return {
            "finished": True,
            "data": self.data
        }
    
    def worker(self):
        pass
    
g_server = Server()

#-----------------------------------------------
@route('/', method='GET')
def index():
    response.content_type = 'application/json'
    return "{}"

@route('/go', method='POST')
def go():
    global g_server
    response.content_type = 'application/json'
    config = json.loads(request.body.readline())
    g_server.go(config)
    return "{}"

@route('/example', method='GET')
def example():
    response.content_type = 'application/json'
    return "{}"

#-----------------------------------------------
if __name__ == '__main__':
    run(host='0.0.0.0', port=1337, debug=True)
