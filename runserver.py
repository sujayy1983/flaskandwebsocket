#!/usr/bin/env python
# coding: utf-8

import os
import io
import json
import time
import subprocess

from flask import Flask, render_template, Response
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

myapp = Flask(__name__)
myapp.secret_key = os.urandom(24)
myapp.debug = True


def handle_websocket(ws, path=None):
    while True:
        message = ws.receive()
        print("Message rx: {}".format(message))
        if not message:
            break
        elif message == "lshomedir": #Any required feature let's say - Feature 1
           ws.send(subprocess.getoutput('ls -lrt')) 
        elif message == "processinfo": #Any required feature let's say - Feature 2 
           ws.send(subprocess.getoutput('ps -ef')) 
        else:
            ws.send("Unknown message received: {}".format(message))

def my_app(environ, start_response):
    """ The app """
    path = environ["PATH_INFO"]
    if not path.startswith("/websocket"):
        return myapp(environ, start_response)
    else:
        handle_websocket(environ["wsgi.websocket"], path=path)

@myapp.route('/')
@myapp.route('/home')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0',5000), my_app, handler_class=WebSocketHandler)
    http_server.serve_forever()
