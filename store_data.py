import pprint
import datetime
import mysql.connector
from decouple import config
from get_mail import GetMail

class StoreData:
    def __init__(self):
        DB_NAME = 'MailDB'
        try:
            self.mydb = mysql.connector.connect(host="localhost", user=config('DB_USER'), passwd=config('DB_PASSWORD'))
        except mysql.connector.Error as err:
            if(1045 == err.errno):
                print("Invalid credentials, Access denied")
            else:
                print(err)
            return None
        self.cursor = self.mydb.cursor()

        tries = 5

        for x in range(tries):
            try:
                self.cursor.execute("USE {}".format(DB_NAME))
                break
            except mysql.connector.Error as err:
                if(1049 == err.errno):
                    self.cursor.execute("CREATE DATABASE {}".format(DB_NAME))
                    print(DB_NAME + " Created")
                else:
                    print(err)
                    return None

        if(5 == x):
            print("Error connecting DB")
            return None


        TABLE = (
            "CREATE TABLE `Emails` ("
            "  `mail_id` VARCHAR(20) NOT NULL,"
            "  `received` DATETIME NOT NULL,"
            "  `labels` VARCHAR(256),"
            "  `subject` VARCHAR(500),"
            "  `from_address` VARCHAR(256) NOT NULL,"
            "  `to_address` VARCHAR(256) NOT NULL,"
            "  `message` TEXT NOT NULL,"
            "  PRIMARY KEY (`mail_id`)"
            ") ")

        try:
            self.cursor.execute(TABLE)
            print("Creating table Emails")
        except mysql.connector.Error as err:
            if (1050 == err.errno):
                print("Table exists")
            else:
                print(err)

    def add_data(self,*args):
        GMobj = GetMail()
        if(len(args) == 0):
            mails = GMobj.get_mail_id()
        elif(len(args) == 1):
            mails = GMobj.get_mail_id(args[0])
        add_mail = "INSERT INTO Emails (mail_id, received, labels, subject,from_address ,to_address, message) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        for mail in mails:
            try:
                mail['date'] = datetime.datetime.strptime(mail['date'], '%a, %d %b %Y %H:%M:%S %z')
            except ValueError as err:
                mail['date'] = mail['date'][:-6]
                mail['date'] = datetime.datetime.strptime(mail['date'], '%a, %d %b %Y %H:%M:%S %z')
            mail['date'].strftime('%Y-%m-%d %H:%M:%S')
            value = (mail['id'],mail['date'],mail['labels'],mail['subject'],mail['from'],mail['to'],mail['message'])
            try:
                self.cursor.execute(add_mail, value)
            except mysql.connector.Error as err:
                if(1062 == err.errno):
                    print("Duplicate Entry, Updating labels")
                    self.cursor.execute("UPDATE `Emails` SET labels='%s' WHERE mail_id='%s'" % (mail['labels'],mail['id']))

        self.mydb.commit()
        self.cursor.close()
        self.mydb.close()

if __name__ == '__main__':
    obj = StoreData()
    obj.add_data()
