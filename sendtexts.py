import random
import time
from googlevoice import Voice
import datetime
import keyring

#Time of day to run. Which hours to start submitting texts and which hours to finish. 
MinHourOfDay=8
MaxHourOfDay=22

#How frequently do you want it to send texts in minutes. It will be a random number of minutes betweemn these two settings
MinIncriment=30
MaxIncriment=180

#Files Used
ListOfNumbers="PhoneNumbers.txt"
ListofSayings="Sayings.txt"
LogFile="MotivationLog.txt"

#open Files
PhoneList=open(ListOfNumbers, "r")
PhoneNumbers=PhoneList.read().splitlines()

Myfile=open(ListofSayings, "r")
sayings=Myfile.readlines()
count=int(len(sayings)-1)

#Google voice Login
voice = Voice()
usr=keyring.get_password('2','2')
pwd=keyring.get_password('1','1')
voice.login(usr,pwd)

#Functions
def Submitter():
    logger("----------Starting Up-------------\n")
    while True:
        timer= random.randint((MinIncriment*60),(MaxIncriment*60))
        now=datetime.datetime.now().time()

        logger("next message going out in " + str(round(timer/60)) + " minutes\n")
        time.sleep(timer)        
              
        if now > datetime.time(MinHourOfDay) and now < datetime.time(MaxHourOfDay):
            for PhoneNumber in PhoneNumbers:
                ListRandomizer(PhoneNumber)


def ListRandomizer(PhoneNumber):
    randomizer=random.randint(0,count)
    randomstring = sayings[randomizer]
    Texter(PhoneNumber, randomstring)

def Texter(PhoneNumber, randomstring):
    voice.send_sms(PhoneNumber, randomstring)
    logger("Just sent " + PhoneNumber + " this: " + randomstring)

def logger (Message):
    now=datetime.datetime.now().time()
    logtime = str(now)
    with open(LogFile, "a") as Log:
        Log.write(logtime +"  "+ Message)
 
#Run Main Loop
Submitter()
