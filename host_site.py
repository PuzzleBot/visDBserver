from flask import Flask
from flask import jsonify
import json


app = Flask(__name__)

@app.route('/')
def indexPage():
    return 'Please use a path to access one of the provided methods.'


@app.route('/accounts/<username>/validateLogin', methods=['GET'])
def validateLogin(username):
    validityString = 'false'
    
    # Database queries

    return jsonify(valid=validityString)


@app.route('/accounts/<username>/createAccount', methods=['POST'])
def createAccount(username):
    # Outcomes: success, error_exists, error_invalid
    outcome = 'success'

    return jsonify(status=outcome)


@app.route('/routes/<routeName>/addRoute', methods=['POST'])
def addRoute(routeName):
    # Outcomes: success, error_exists, error_invalid
    outcome = 'success'
    
    return jsonify(status=outcome)


@app.route('/routes/<routeName>/deleteRoute', methods=['POST'])
def deleteRoute(routeName):
    outcome = 'success'
    
    return jsonify(status=outcome)


@app.route('/routes', methods=['GET'])
def getRouteList():
    routeArraySTring = ''

    return jsonify(routeList=routeArrayString)

@app.route('/routes/<routeName>', methods=['GET'])
def getRoute():
    routeInfo = ''

    return jsonify(info=routeInfo)


@app.route('/docs/<docName>', methods=['GET'])
def getDoc(docName):
    docString = ''
    
    return jsonify(doc=docString)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
