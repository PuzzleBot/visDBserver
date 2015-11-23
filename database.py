import MySQLdb
import host_site

db = MySQLdb.connect(host="131.104.49.67:80", # our host, do not modify
                     user="sysadmin", # your username
                     passwd="DenotedSundials", # your password
                     db="PositiveFish") # name of the data base

initCur = db.cursor()
initCur.execute("CREATE TABLE IF NOT EXISTS users {username VARCHAR(40), password VARCHAR(40), firstname VARCHAR(40), lastname VARCHAR(40), email VARCHAR(80), teamcaptain BOOLEAN, accessible BOOLEAN}")
initCur.execute("CREATE TABLE IF NOT EXISTS routes {name VARCHAR(40), lattitudeStart FLOAT, longitudeStart FLOAT, lattitudeEnd FLOAT, longitudeEnd FLOAT, accessible BOOLEAN, transport VARCHAR(40)}")
initCur.execute("CREATE TABLE IF NOT EXISTS users {docname VARCHAR(40), contents VARCHAR(8000)}")
initCur.close()


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

    return valid
