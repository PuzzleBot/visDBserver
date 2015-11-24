from flask import Flask
from flask import jsonify
from flask import make_response
from flask import response
import json
import database
import random


app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route('/')
def indexPage():
    return 'Please use a path to access one of the provided methods.'


@app.route('/test')
def testPage():
    return render_template('testFiles/test.html')


@app.route('/test/validateLogin')
def testValidLogin():
    validityString = database.valLogin('user1', 'pass1')
    return jsonify(valid=validityString)


@app.route('/accounts/validateLogin', methods=['GET', 'PUT', 'OPTIONS'])
def validateLogin():
    validityString = 'false'
    # Input: json
    # username: string, password: string
    # set cookie: username, session hash

    inputJsonLib = request.view_args
    print inputJsonLib['username']
    
    validityString = database.valLogin(inputJsonLib['username'], inputJsonLib['password'])
    
    responseObj = make_response(jsonify(valid=validityString))
    
    randomCookie = ''
    
    if validityString == 'true':
        responseObj.set_cookie(inputJsonLib['username'], randomCookie)

    return responseObj


@app.route('/accounts/createAccount', methods=['PUT'])
def createAccount():
    # Outcomes: success, error_exists, error_invalid
    # firstName, surname, email, password, teamCaptain, accessibility
    outcome = 'success'
    
    inputJsonLib = request.view_args
    
    email = inputJsonLib['email']
    username = inputJsonLib['username']
    password = inputJsonLib['password']
    firstname = inputJsonLib['firstName']
    lastname = inputJsonLib['surname']
    teamcaptain = inputJsonLib['teamCaptain']
    accessibility = inputJsonLib['accessibility']
    
    outcome = database.createAccount(username, password, firstname, lastname, email, teamcaptain, accessibilityNeeds)
    
    return jsonify(status=outcome)


@app.route('/accounts/<username>/getDetails', methods=['GET'])
def getDetails(username):
    # firstName, surname, email, teamCaptain, accessibility
    inputJsonLib = request.view_args
    firstname, surname, email, teamCaptain, accessibility = database.getDets(inputJsonLib['username'])
    return jsonify(firstName=firstname, surname=surname, email=email, teamCaptain=teamCaptain, accessibility=accessibility)


@app.route('/routes/addRoute', methods=['POST'])
def addRoute(routeName):
    # Outcomes: success, error_exists, error_invalid
    outcome = 'success'
    inputJsonLib = request.view_args
    outcome = database.addRoutes(inputJsonLib['name'],inputJsonLib['lattitudeStart'],inputJsonLib['longitudeStart'],
                                 inputJsonLib['lattitudeEnd'],inputJsonLib['longitudeEnd'],inputJsonLib['isAccessible'],inputJsonLib['transport'])
    return jsonify(status=outcome)


@app.route('/routes/deleteRoute', methods=['POST'])
def deleteRoute(routeName):
    # Outcomes: success, error_not_exists
    outcome = 'success'
    inputJsonLib = request.view_args
    outcome = database.addRoutes(inputJsonLib['name'])
    return jsonify(status=outcome)


@app.route('/routes', methods=['GET'])
def getRouteList():
    # filters:
    # general public: return all, recieve ()
    # participant: recieve (accessibility)
    inputJsonLib = request.view_args
    isAccessible = inputJsonLib['isAccessible']
    routeArray = database.getAllRoutes(isAccessible)

    return jsonify(routeList=routeArray)

# Cities, provinces, countries

@app.route('/routes/<routeName>', methods=['GET'])
def getRoute():
    routeInfo = ''

    return jsonify(info=routeInfo)


@app.route('/docs/faq', methods=['GET'])
def getFAQ():
    # faq / terms (terms and conditions)
    # faq: 2D array of questions and answers [row][0 = question, 1 = answer]
    faqArray = database.getFaq()
    docString = json.dumps(faqArray)
    
    return jsonify(doc=docString)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
