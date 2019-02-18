import random
import time
from googlevoice import Voice
import datetime
import keyring

MinIncriment=10
MaxIncriment=90

ListOfNumbers="PhoneNumbers.txt"
ListofSayings="Sayings.txt"
LogFile="MotivationLog.txt"

voice = Voice()
parka=keyring.get_password('1','1')
shmarka=keyring.get_password('2','2')
voice.login(shmarka,parka)

PhoneList=open(ListOfNumbers, "r")
PhoneNumbers=PhoneList.read().splitlines()

def randomtexter():
    while True:
        timer= random.randint((MinIncriment*60),(MaxIncriment*60))
             
        Myfile=open(ListofSayings, "r")
        sayings=Myfile.readlines()
        count=int(len(sayings)-1)
        randomizer=random.randint(0,count)
        randomstring = sayings[randomizer]

        nextrun=str(timer/60)
        now=datetime.datetime.now().time()
        logtime = str(now)
        with open(LogFile, "a") as Log:
                Log.write(logtime + "  next run is in " + nextrun + " minutes..." + randomstring)
                
        time.sleep(timer)
      
        if now > datetime.time(8) and now < datetime.time(22):
            for PhoneNumber in PhoneNumbers:
                voice.send_sms(PhoneNumber, randomstring)

            now=datetime.datetime.now().time()
            logtime = str(now)
            with open(LogFile, "a") as Log:
                Log.write(logtime+"  completed \n")

randomtexter()











