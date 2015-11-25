import MySQLdb
import host_site
import re

#db = MySQLdb.connect(host="131.104.49.67:80", # our host, do not modify
#user="sysadmin", # your username
#passwd="DenotedSundials", # your password
#db="PositiveFish") # name of the data base

db = MySQLdb.connect(host="206.248.176.247", # our host, do not modify
                     user="root", # your username
                     passwd="taco#taco", # your password
                     db="visdb") # name of the data base

initCur = db.cursor()
initCur.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(40), password VARCHAR(40), firstname VARCHAR(40), lastname VARCHAR(40), email VARCHAR(80), teamcaptain BOOLEAN, accessibilityNeeds BOOLEAN, teamname VARCHAR(40))")
initCur.execute("CREATE TABLE IF NOT EXISTS routes (name VARCHAR(40), city VARCHAR(40), lattitudeStart FLOAT, longitudeStart FLOAT, lattitudeEnd FLOAT, longitudeEnd FLOAT, isAccessible BOOLEAN, transport VARCHAR(40))")
initCur.execute("CREATE TABLE IF NOT EXISTS faq (question VARCHAR(8000), answer VARCHAR(8000))")
initCur.execute("CREATE TABLE IF NOT EXISTS terms (content VARCHAR(8000))")

initCur.execute("CREATE TABLE IF NOT EXISTS sessions (username VARCHAR(40), cookieVal VARCHAR(40))")
initCur.execute("CREATE TABLE IF NOT EXISTS teams (teamname VARCHAR(40), teamcaptainname VARCHAR(40))")

initCur.execute("CREATE TABLE IF NOT EXISTS provinces_in_country (country VARCHAR(40), province VARCHAR(40))")
initCur.execute("CREATE TABLE IF NOT EXISTS cities_in_province (province VARCHAR(40), city VARCHAR(40))")

initCur.execute("INSERT INTO faq (question, answer) VALUES ('What is Meal Exchange?', 'Meal Exchange is a charitable organization that is trying to reduce food insecurity and give to the less fortunate.')")
initCur.execute("INSERT INTO faq (question, answer) VALUES ('What is Trick-or-eat?', 'Trick-or-eat is a charitable event about collecting food from donors on Halloween instead of candy in order to provide to the less fortunate.')")
initCur.execute("INSERT INTO terms (content) VALUES ('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')")


initCur.close()


def getFaq():
    cur = db.cursor()
    cur.execute("SELECT DISTINCT * FROM faq")
    
    faqArray = cur.fetchall()
    faqString = ''
    
    for i in faqArray:
        faqString = faqString + '<h3>'
        faqString = faqString + i[0]
        faqString = faqString + '</h3><br>'
    
        faqString = faqString + '<p class = "lead">'
        faqString = faqString + i[1]
        faqString = faqString + '</p><br>'
    cur.close()
    return faqString

def getTerms():
    cur = db.cursor()
    cur.execute("SELECT DISTINCT * FROM terms")
    
    data = cur.fetchall()
    dataString = data[0][0]
    cur.close()
    
    return dataString

def valLogin(username, password):
    valid = 'false'
    
    # Sanitize input
    cleanUsername = str(MySQLdb.escape_string(username))
    
    cur = db.cursor()
    cur.execute("SELECT password FROM users WHERE username = '" + cleanUsername + "'")
    
    if cur.rowcount == 0:
        valid = 'false'
    else:
        rows = cur.fetchall()
        if rows[0][0] == password:
            valid = 'true'
        else:
            valid = 'false'

    cur.close()
    return valid

def storeSession(username, cookieVal):
    cleanUsername = str(MySQLdb.escape_string(username))
    cleanCookie = str(MySQLdb.escape_string(cookieVal))
    
    cur = db.cursor()
    cur.execute("SELECT * FROM sessions WHERE username = '" + cleanUsername + "'")
    if cur.rowcount > 0:
        cur.execute("DELETE FROM sessions WHERE username = '" + cleanUsername + "'")
        
    cur.execute("INSERT INTO sessions (username, cookieVal) VALUES ('" + cleanUsername + "', '" + cleanCookie + "')")
    cur.close()

def validateSession(username, cookieVal):
    validString = 'false'
    
    if (username == None) or (cookieVal == None):
        return validString
    
    cleanUsername = str(MySQLdb.escape_string(username))
    cleanCookie = str(MySQLdb.escape_string(cookieVal))

    cur = db.cursor()
    cur.execute("SELECT cookieVal FROM sessions WHERE username = '" + cleanUsername + "'")
    if cur.rowcount > 0:
        for i in cur.fetchall():
            if i[0] == cleanCookie:
                validString = 'true'
    
    else:
        validString = 'false'

    cur.close()
    return validString

def createAccount(username, password, firstname, lastname, email, teamcaptain, accessibilityNeeds):
    cleanUsername = str(MySQLdb.escape_string(username))
    cleanPassword = str(MySQLdb.escape_string(password))
    cleanFirst = str(MySQLdb.escape_string(firstname))
    cleanLast = str(MySQLdb.escape_string(lastname))
    cleanEmail = str(MySQLdb.escape_string(email))
    cleanTeam = str(MySQLdb.escape_string(teamcaptain))
    accessibilityNeeds = str(MySQLdb.escape_string(accessibilityNeeds)).upper()
    
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE username = '" + cleanUsername + "'")
    if cur.rowcount == 0:
        cur.execute("INSERT INTO users (username, password, firstname, lastname, email, teamcaptain, accessibilityNeeds, teamname) VALUES('" + cleanUsername + "','" + cleanPassword + "','" + cleanFirst
                    + "','" + cleanLast + "','" + cleanEmail + "'," + cleanTeam + "," + accessibilityNeeds
                    + ", 'no_team')")
        cur.close()
        return 'success'
    else:
        cur.close()
        return 'error_exists'

def getDets(username):
    user = str(MySQLdb.escape_string(username))
    cur = db.cursor()
    cur.execute("SELECT firstname, lastname, email, teamcaptain, accessibilityNeeds FROM users WHERE username = '" + user + "'")

    detArray = cur.fetchall()
    
    if cur.rowcount > 0:
        cur.close()
        return detArray[0][0], detArray[0][1], detArray[0][2], detArray[0][3], detArray[0][4]
    else:
        return 'null', 'null', 'null', 'false', 'false'


def addRoutes(name, lattitudeStart, longitudeStart , lattitudeEnd , longitudeEnd, isAccessible, transport):
    cleanName = str(MySQLdb.escape_string(name))
    cleanTransport = str(MySQLdb.escape_string(transport))
    isAccessible = str(MySQLdb.escape_string(isAccessible)).upper()
    cur = db.cursor()
    cur.execute("SELECT * FROM routes WHERE name = '" + cleanName + "'")
    if cur.rowcount == 0:
        cur.execute("INSERT INTO routes VALUES('"+ cleanName +"',"+lattitudeStart+","+longitudeStart+","+lattitudeEnd+","+
                                                longitudeEnd+","+isAccessible+",'"+cleanTransport+"')")
        cur.close()
        return 'success'
    else:
        cur.close()
        return 'error_exists'

def delRoute(name):
    cleanName =str(MySQLdb.escape_string(name))

    cur = db.cursor()
    cur.execute("SELECT * FROM routes WHERE name = '" + cleanName + "'")
    if cur.rowcount==0:
        cur.close()
        return 'error_not_exists'
    else:
        cur.close()
        cur.execute("DELETE FROM routes WHERE name = '" + cleanName + "'")
        return 'success'

def getAllRoutes(username):
    cur = db.cursor()

    if isAccessible == 'true':
        cur.execute("SELECT * FROM routes WHERE accessibilityNeeds = TRUE")
    else:
        cur.execute("SELECT * FROM routes")
    routeList = cur.fetchall()
    cur.close()
    return routeList