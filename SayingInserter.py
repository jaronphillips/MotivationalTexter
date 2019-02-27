import mysql.connector
import keyring

dbuser=keyring.get_password("dbuser","dbuser")
dbpass=keyring.get_password("dbpass","dbpass")
dbhost=keyring.get_password("dbhost","dbhost")
dbname=keyring.get_password("dbname","dbname")

mydb = mysql.connector.connect(user=dbuser, password=dbpass, host=dbhost,database=dbname,connect_timeout=43200)
mycursor = mydb.cursor()


def writecrap(message):
    with open("NewSayings.txt", "a") as NewSayings:
            NewSayings.write(message+"\n")

Myfile=open("NewSayings.txt", "r")
sayings=Myfile.read().splitlines()

for saying in sayings:
    try:
        mycursor.execute("insert into TEXT_MESSAGES (TM_MESSAGES) VALUES (\'"+saying+"\')")
        print ("insert into TEXT_MESSAGES (TM_MESSAGES) VALUES (\'"+saying+"\')")
        mydb.commit()
        writecrap(saying)
    except:
        pass



