import pandas as pd
import mysql.connector
import hashlib,binascii,os
class authenticationController:
    dfUsers = pd.DataFrame()
    def __init__(self):
        #Get dfUsers from MYSQL database
        #Connection
        self.refreshDatabase()

    def openConnection(self):
        con = mysql.connector.connect(host="instanciatesis.cxoxdn88fwms.us-east-1.rds.amazonaws.com",user="bromeroTesis",passwd="passTesis!")
        return con

    def refreshDatabase(self):
        con = self.openConnection()
        self.dfUsers = pd.read_sql_query("SELECT idUsuario,email,password FROM Usuarios",con)
        con.close()
    
    def hashPassword(self,password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def authenticate(self,email,password):
        if (email in self.dfUsers['email']):
            hashedPassword = self.hashPassword(password)
            if (hashedPassword in self.dfUsers['password']):
                return {'state': True,'message': "Success"}
            return {'state': False,'message': "Incorrect Password"}
        return {'state': False,'message': "Incorrect Email"}

    def registerUser(self,email,password):
        hashedPassword = self.hashPassword(password)
        con = self.openConnection()
        mycursor = con.cursor()
        sql = "INSERT INTO Users (email, password) VALUES (%s, %s)"
        val = (email, hashedPassword)
        mycursor.execute(sql, val)
        con.commit()
        self.refreshDatabase()