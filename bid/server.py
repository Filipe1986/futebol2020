# -*- coding: UTF-8 -*-

from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import requests
import logging
import sys
import json
from lxml import html
from requests_toolbelt.utils import dump




# Create the application instance
app = Flask(__name__, template_folder="templates")

# Create a URL route in our application for "/"
@app.route('/')
def home():

    print(request)
    return jsonify({'ip': request.remote_addr}), 200

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
