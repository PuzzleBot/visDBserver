import MySQLdb
import host_site

#db = MySQLdb.connect(host="131.104.49.67:80", # our host, do not modify
#user="sysadmin", # your username
#passwd="DenotedSundials", # your password
#db="PositiveFish") # name of the data base

db = MySQLdb.connect(host="206.248.176.247", # our host, do not modify
                     user="root", # your username
                     passwd="taco#taco", # your password
                     db="visdb") # name of the data base

initCur = db.cursor()
initCur.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(40), password VARCHAR(40), firstname VARCHAR(40), lastname VARCHAR(40), email VARCHAR(80), teamcaptain BOOLEAN, accessibilityNeeds BOOLEAN)")
initCur.execute("CREATE TABLE IF NOT EXISTS routes (name VARCHAR(40), city VARCHAR(40), lattitudeStart FLOAT, longitudeStart FLOAT, lattitudeEnd FLOAT, longitudeEnd FLOAT, isAccessible BOOLEAN, transport VARCHAR(40))")
initCur.execute("CREATE TABLE IF NOT EXISTS faq (question VARCHAR(8000), answer VARCHAR(8000))")
initCur.execute("CREATE TABLE IF NOT EXISTS sessions (username VARCHAR(40), cookieVal VARCHAR(40))")

initCur.execute("INSERT INTO faq (question, answer) VALUES ('What is Trick-or-eat?', 'Trick-or-eat is a charitable organization about collecting food from donors on Halloween instead of candy in order to provide to the less fortunate.')")

initCur.close()


def getFaq():
    cur = db.cursor()
    cur.execute("SELECT * FROM faq")
    
    faqArray = cur.fetchall()
    cur.close()
    return faqArray


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
        if rows[0][1] == password:
            valid = 'true'
        else:
            valid = 'false'

    cur.close()
    return valid

def createAccount(username, password, firstname, lastname, email, teamcaptain, accessibilityNeeds):
    cleanUsername = str(MySQLdb.escape_string(username))
    cleanPassword = str(MySQLdb.escape_string(password))
    cleanFirst = str(MySQLdb.escape_string(firstname))
    cleanLast = str(MySQLdb.escape_string(lastname))
    cleanEmail = str(MySQLdb.escape_string(email))
    cleanTeam = str(MySQLdb.escape_string(teamcaptain))


    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE username = '" + cleanUsername + "'")
    if cur.rowcount == 0:
        cur.execute("INSERT INTO users VALUES('" + cleanUsername + "','" + cleanPassword + "','" + cleanFirst
                    + "','" + cleanLast + "','" + cleanEmail + "'," + cleanTeam + "," + accessibilityNeeds
                    + ")")
        return 'success'
    else:
        return 'error_exists'

def getDets(username):
    user = str(MySQLdb.escape_string(username))
    cur = db.cursor()
    cur.execute("SELECT firstname, lastname, email, teamcaptain, accessibilityNeeds FROM users WHERE username = '" + user + "'")

    detArray = cur.fetchall()
    cur.close()
    return detArray[0][0], detArray[0][1], detArray[0][2], detArray[0][3], detArray[0][4]

def addRoutes(name, lattitudeStart, longitudeStart , lattitudeEnd , longitudeEnd, isAccessible, transport):
    cleanName = str(MySQLdb.escape_string(name))
    cleanTransport = str(MySQLdb.escape_string(transport))

    cur = db.cursor()
    cur.execute("SELECT * FROM routes WHERE name = '" + cleanName + "'")
    if cur.rowcount == 0:
        cur.execute("INSERT INTO routes VALUES('"+cleanName+"',"+lattitudeStart+","+longitudeStart+","+lattitudeEnd+","+
                                                longitudeEnd+","+isAccessible+",'"+cleanTransport+"')")
        return 'success'
    else:
        return 'error_exists'
