import datetime
from datetime import timedelta
import mysql.connector
#import re
import random
import time
import datetime
import keyring
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#MotivaionLog
LogFile="MotivationLog.txt"

#Database settings
dbuser=keyring.get_password("dbuser","dbuser")
dbpass=keyring.get_password("dbpass","dbpass")
dbhost=keyring.get_password("dbhost","dbhost")
dbname=keyring.get_password("dbname","dbname")

#smtp settings
user=keyring.get_password('4','4')
passwd=keyring.get_password('1','1')


#Functions
def logger (Message):
    now=datetime.datetime.now().time()
    logtime = str(now)
    with open(LogFile, "a") as Log:
        Log.write(logtime +"  "+ Message)

def TimeChecker(MinHourOfDay,MaxHourOfDay):
   now=datetime.datetime.now().time()
   if now > datetime.time(int(MinHourOfDay)) and now < datetime.time(int(MaxHourOfDay)):
      return True
   else:
      return False

def sql(query):
   mydb = mysql.connector.connect(user=dbuser, password=dbpass, host=dbhost,database=dbname,connect_timeout=43200)
   mycursor = mydb.cursor()
   mycursor.execute(query)
   sql.result = mycursor.fetchall()
   mycursor.close()

def sqlupdate(query):
   mydb = mysql.connector.connect(user=dbuser, password=dbpass, host=dbhost,database=dbname,connect_timeout=43200)
   mycursor = mydb.cursor()
   mycursor.execute(query)
   mydb.commit()
   mycursor.close()

def GetUserSettings():
   sql("SELECT TU_ID, TU_NAME, TU_PHONE, TU_MIN_HOUR_OF_DAY, TU_MAX_HOUR_OF_DAY, TU_MIN_INCREMENT, TU_MAX_INCREMENT, TU_CARRIER from TEXT_USERS")
   return sql.result

def GetMessages():
   sql("select TM_MESSAGES from TEXT_MESSAGES order by TM_ID")
   return sql.result

def RandomMessage():
   count=int(len(Messages)-1)
   randomizer=random.randint(0,count)
   randomized =Messages[randomizer]
   return (randomized[0])

def send_mail(SMSEmail,randomstring,Name):
    server = smtplib.SMTP('smtp.gmail.com:587')
    username = user
    password = passwd
    from_addr = user
    to_addr = SMSEmail
    text = randomstring+"     "

    msg = MIMEMultipart()

    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = 'RandomFatter'
    msg.attach(MIMEText(text))

    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password)
    server.sendmail(from_addr,to_addr,msg.as_string())
    time.sleep(3)
    server.quit()
    logger(Name+ ': just sent email \n')

def NextRun(userID):
   sql("Select TU_NEXT_SEND from TEXT_USERS where TU_ID="+ str(userID))
   return sql.result

def GetMinRunTime():
   sql("SELECT min(TU_MIN_INCREMENT) from TEXT_USERS")
   return sql.result

#Run Everything
Messages=GetMessages()
UserSettings=GetUserSettings()
#Sleeper=GetMinRunTime()[0][0]
Sleeper=5
logger ("-------------Starting up------------------\n")
logger ("Checking eligibility every "+ str(Sleeper) +" minutes \n")

while True:
    for userinfo in UserSettings:
        userID=userinfo[0]
        userName=userinfo[1]
        Phone=userinfo[2]
        MinHour=userinfo[3]
        MaxHour=userinfo[4]
        MinInc=userinfo[5]
        MaxInc=userinfo[6]
        PhoneCarrier=userinfo[7]
        SMSEmail=Phone+"@"+PhoneCarrier
        Cansend = TimeChecker(MinHour,MaxHour)
        userNextRun=(NextRun(userID)[0][0])
        logger (userName+": Checking eligibility\n")
        if str(userNextRun) < str(datetime.datetime.now()):
            if Cansend == True:
                 randomstring=RandomMessage()
                 logger (userName+": sending "+randomstring +"\n")
                 send_mail(SMSEmail,randomstring,userName)
            else:
                 randomstring=RandomMessage()
                 logger (userName+": They are not wanting messages at this time.\n")
            randomtimer= random.randint((int(MinInc)*60),(int(MaxInc)*60))
            userNextRun=datetime.datetime.now()+timedelta(seconds=randomtimer)
            sqlupdate ("update TEXT_USERS set TU_NEXT_SEND=\'"+str(userNextRun)+"\' where TU_ID="+str(userinfo[0]))
        else:
            userNextRun=(NextRun(userID)[0][0])
            logger (userName+ ": Not sending until " +userNextRun +"\n")
    time.sleep(int(Sleeper)*60)
