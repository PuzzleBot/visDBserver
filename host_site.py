from flask import Flask
from flask import jsonify
import json
import database


app = Flask(__name__)

@app.route('/')
def indexPage():
    return 'Please use a path to access one of the provided methods.'


@app.route('/test')
def testPage():
    return render_template('testFiles/test.html')


@app.route('/accounts/validateLogin', methods=['GET', 'PUT'])
def validateLogin():
    validityString = 'false'
    # Input: json
    # username: string, password: string
    # set cookie: username, session hash

    inputJsonLib = request.view_args
    print inputJsonLib['username']
    
    validityString = database.valLogin(inputJsonLib['username'], inputJsonLib['password'])

    return jsonify(valid=validityString)


@app.route('/accounts/createAccount', methods=['PUT'])
def createAccount():
    # Outcomes: success, error_exists, error_invalid
    # firstName, surname, email, password, teamCaptain, accessibility
    outcome = 'success'
    
    return jsonify(status=outcome)


@app.route('/accounts/<username>/getDetails', methods=['GET'])
def getDetails(username):
    # firstName, surname, email, teamCaptain, accessibility
    outcome = 'success'
    
    return jsonify(status=outcome)


@app.route('/routes/addRoute', methods=['POST'])
def addRoute(routeName):
    # Outcomes: success, error_exists, error_invalid
    outcome = 'success'
    
    return jsonify(status=outcome)


@app.route('/routes/deleteRoute', methods=['POST'])
def deleteRoute(routeName):
    outcome = 'success'
    
    return jsonify(status=outcome)


@app.route('/routes', methods=['GET'])
def getRouteList():
    # filters:
    # general public: return all, recieve ()
    # participant: recieve (accessibility)
    routeArrayString = ''

    return jsonify(routeList=routeArrayString)

# Cities, provinces, countries

@app.route('/routes/<routeName>', methods=['GET'])
def getRoute():
    routeInfo = ''

    return jsonify(info=routeInfo)


@app.route('/docs/faq', methods=['GET'])
def getDoc(docName):
    # faq / terms (terms and conditions)
    # faq: 2D array of questions and answers [row][0 = question, 1 = answer]
    faqArray = database.getFaq()
    docString = json.dumps(faqArray)
    
    return jsonify(doc=docString)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
