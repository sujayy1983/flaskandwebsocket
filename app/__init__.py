# coding: utf-8
import os

from flask import Flask, render_template, Response

from app.websocket import handle_websocket

myapp = Flask(__name__)
myapp.secret_key = os.urandom(24)
myapp.debug = True

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

#-----------------------------------------------#
# Note: Not sure if it is a good practice       #
# This lets us have custom paths for css and js #
#-----------------------------------------------#
@myapp.route('/css/<filename>')
def readcss(filename):
    data = open("{}/css/{}".format(os.getcwd(), filename)).read() 
    return Response(data, mimetype='text/css')

@myapp.route('/js/<filename>')
def readjs(filename):
    return open("{}/js/{}".format(os.getcwd(), filename)).read()
