import mysql.connector
from mysql.connector import errorcode


#connect to mysql db
def connect():
    database = mysql.connector.connect(user='username',
                                       password='password',
                                       host='db host',
                                       database='database name'
                                       )
    return database

#Function for testing connection
def testConn():
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        conn.commit()
        statement.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Username/password issue')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('databse not found')
    else:
        print("Other Error")
        return False

#Get all video ids from db
def getVidIDs():
    query = "SELECT VideoID FROM PublishTimes"
    idList = []
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(
            query)
        ids = statement.fetchall()
        conn.commit()
        statement.close()
        conn.close()
        for id in ids:
            idList.append(id[0])

        return idList

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Username/password issue')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('databse not found')
    else:
        return False

#insert new video and time into db
def insertVid(YouTuber, vidId, pubTime):
    query = "INSERT INTO PublishTimes(YouTuber, VideoID, PubTime ) VALUES(%s,%s,%s);"

    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(query, (YouTuber, vidId, pubTime,))
        conn.commit()

        statement.close()
        conn.close()

        return True

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Username/password issue')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('database not found')
    else:
        return False