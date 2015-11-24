from flask import Flask
from flask import jsonify
from flask import make_response
from flask import render_template
from flask import url_for
from flask import request
import json
import random
import string
import os

dir = os.getcwd()
app = Flask(__name__, template_folder=dir)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route('/')
def testPage():
    return render_template(url_for('static', filename='test.html'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug='true')