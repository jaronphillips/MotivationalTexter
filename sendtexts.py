import random
import time
from googlevoice import Voice
import datetime
import keyring

#Time of day to run. Which hours to start submitting texts and which hours to finish. 
MinHourOfDay=8
MaxHourOfDay=23

#How frequently do you want it to send texts in minutes. It will be a random number of minutes betweemn these two settings
MinIncriment=10
MaxIncriment=90

#Files Used
ListOfNumbers="PhoneNumbers.txt"
ListofSayings="Sayings.txt"
LogFile="MotivationLog.txt"

PhoneList=open(ListOfNumbers, "r")
PhoneNumbers=PhoneList.read().splitlines()

#Google voice Login
voice = Voice()
usr=keyring.get_password('2','2')
pwd=keyring.get_password('1','1')
voice.login(usr,pwd)


#Functions
def Submitter():
    while True:
        timer= random.randint((MinIncriment*60),(MaxIncriment*60))
        now=datetime.datetime.now().time()
        
        if now > datetime.time(MinHourOfDay) and now < datetime.time(MaxHourOfDay):
            for PhoneNumber in PhoneNumbers:
                ListReader(PhoneNumber,timer)
        time.sleep(timer)

def ListReader(PhoneNumber,timer):
    Myfile=open(ListofSayings, "r")
    sayings=Myfile.readlines()
    count=int(len(sayings)-1)
    randomizer=random.randint(0,count)
    randomstring = sayings[randomizer]
    Texter(PhoneNumber, randomstring, timer)

def Texter(PhoneNumber, randomstring, timer):
    voice.send_sms(PhoneNumber, randomstring)
    nextrun=str(timer/60)
    now=datetime.datetime.now().time()
    logtime = str(now)
    with open(LogFile, "a") as Log:
        Log.write(logtime + "  Just sent this: "+ randomstring)
        Log.write(logtime + "  next run is in " + nextrun + " minutes \n")


#Run Main Loop
Submitter()
