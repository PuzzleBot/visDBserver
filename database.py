import host_site

db = MySQLdb.connect(host="131.104.49.67", # our host, do not modify
                     user="sysadmin", # your username
                     passwd="DenotedSundials", # your password
                     db="PositiveFish") # name of the data base

initCur = db.cursor()
initCur.execute("CREATE TABLE IF NOT EXISTS users {username VARCHAR(40), password VARCHAR(40)}")
initCur.execute("CREATE TABLE IF NOT EXISTS routes {name VARCHAR(40), lattitude FLOAT, longitude FLOAT, accessible BOOLEAN, transport VARCHAR(40)}")
initCur.execute("CREATE TABLE IF NOT EXISTS users {docname VARCHAR(40), contents VARCHAR(8000)}")
initCur.close()
