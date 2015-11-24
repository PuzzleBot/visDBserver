from flask import Flask
from flask import jsonify
from flask import make_response
from flask import render_template
from flask import url_for
from flask import request
import json
import database
import random
import string
import os

asciiCharset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

dir = os.getcwd()
app = Flask(__name__, template_folder=dir)



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
    return render_template(url_for('static', filename='test.html'))


@app.route('/accounts/validateLogin', methods=['GET', 'PUT', 'OPTIONS'])
def validateLogin():
    validityString = 'false'
    # Input: json
    # username: string, password: string
    # set cookie: username, session hash
    
    if request.method == 'OPTIONS':
        return "Access-Control-Allow-Origin: '*'"
    else:
        inputJsonLib = request.get_json()
        print inputJsonLib
    
        validityString = database.valLogin(inputJsonLib['username'], inputJsonLib['password'])
    
        responseObj = make_response(jsonify(valid=validityString))
    
        randomCookie = ''
    
    
        if validityString == 'true':
            for i in range(0, 7):
                randomCookie = randomCookie + random.choice(asciiCharset)
            print randomCookie
            responseObj.set_cookie(inputJsonLib['username'], randomCookie)
        
            database.storeSession(inputJsonLib['username'], randomCookie)

        return responseObj


@app.route('/accounts/createAccount', methods=['PUT', 'OPTIONS'])
def createAccount():
    # Outcomes: success, error_exists, error_invalid
    # firstName, surname, email, password, teamCaptain, accessibility
    outcome = 'success'
    
    if request.method == 'OPTIONS':
        return "Access-Control-Allow-Origin: '*'"
    else:
    
        inputJsonLib = request.get_json()
    
        email = inputJsonLib['email']
        username = inputJsonLib['username']
        password = inputJsonLib['password']
        firstname = inputJsonLib['firstName']
        lastname = inputJsonLib['surname']
        teamcaptain = inputJsonLib['teamCaptain']
        accessibility = inputJsonLib['accessibility']
    
        outcome = database.createAccount(username, password, firstname, lastname, email, teamcaptain, accessibility)
    
        return jsonify(status=outcome)


@app.route('/accounts/<username>/getDetails', methods=['GET', 'OPTIONS'])
def getDetails(username):
    # firstName, surname, email, teamCaptain, accessibility
    userCookie = request.cookies.get(username)
    outcome = 'success'
    
    sessionIsValid = database.validateSession(username, userCookie)
    
    if sessionIsValid == 'true':
        firstname, surname, email, teamCaptain, accessibility = database.getDets(username)
        print firstname
        print surname
        return jsonify(firstName=firstname, surname=surname, email=email, teamCaptain=teamCaptain, accessibility=accessibility, status=outcome)
    else:
        print 'Bad cookie'
        outcome = 'error_accessDenied'
        return jsonify(status=outcome)


@app.route('/routes/addRoute', methods=['POST', 'OPTIONS'])
def addRoute(routeName):
    # Outcomes: success, error_exists, error_invalid
    outcome = 'success'
    
    if request.method == 'OPTIONS':
        return "Access-Control-Allow-Origin: '*'"
    else:
        inputJsonLib = request.get_json()
        outcome = database.addRoutes(inputJsonLib['name'],inputJsonLib['lattitudeStart'],inputJsonLib['longitudeStart'], inputJsonLib['lattitudeEnd'],inputJsonLib['longitudeEnd'],inputJsonLib['isAccessible'],inputJsonLib['transport'])
        return jsonify(status=outcome)


@app.route('/routes/deleteRoute', methods=['POST', 'OPTIONS'])
def deleteRoute(routeName):
    # Outcomes: success, error_not_exists
    outcome = 'success'
    
    if request.method == 'OPTIONS':
        return "Access-Control-Allow-Origin: '*'"
    else:
        inputJsonLib = request.get_json()
        outcome = database.delRoute(inputJsonLib['name'])
        return jsonify(status=outcome)


@app.route('/routes', methods=['GET', 'OPTIONS'])
def getRouteList():
    # filters:
    # general public: return all, recieve ()
    # participant: recieve (accessibility)
    inputJsonLib = request.get_json()
    isAccessible = inputJsonLib['isAccessible']
    routeArray = database.getAllRoutes(isAccessible)

    return jsonify(routeList=json.dumps(routeArray))

# Cities, provinces, countries

@app.route('/routes/<routeName>', methods=['GET', 'OPTIONS'])
def getRoute():
    routeInfo = ''

    return jsonify(info=routeInfo)


@app.route('/docs/faq', methods=['GET', 'OPTIONS'])
def getFAQ():
    # faq / terms (terms and conditions)
    # faq: 2D array of questions and answers [row][0 = question, 1 = answer]
    faqArray = database.getFaq()
    docString = json.dumps(faqArray)
    
    return jsonify(doc=docString)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug='true')
