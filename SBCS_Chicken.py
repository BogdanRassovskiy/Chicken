
import glob, os 
import time
import shutil
from datetime import date
import threading
import logging
import traceback
import requests


#logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'mylog.log')
OS = "linux"

if OS == "windows":
    OS = ""
elif OS == "linux":
    OS = "python3 "

def start_bot1(val):
    try:
        os.system(OS+val+".py")
    except Exception as e:
        print(e)


def circle():
    while True:
        try:
            valide = ["IceCream"]
            for i in range(len(valide)):
                if "desktop." not in valide[i]:
                    #print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< "+str(valide[i])+" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    file = open("token","r")
                    token = file.read().replace("\n","")
                    file.close()
                    URL = "https://api.telegram.org/bot"+str(token)+"/getupdates"
                    result = requests.get(URL)
                    if result.status_code == 200:
                        result = result.json()
                        if "'result': []" in str(result):
                            print("ok "+valide[i])
                        else:
                            try:
                                file = open("err.txt","w")
                                file.write("1")
                                file.close()
                                pritn("ok "+result['result'][0]['message']['chat']['id'])
                            except:
                                print("not ok "+valide[i])
                    else:
                        print("ERROR")
                    try:
                        file = open("err.txt","r")
                        err = file.read()
                        file.close()
                    except:
                        file = open("err.txt","w")
                        file.write("0")
                        file.close()  
                        err = "0"
                    if "1" in err:
                        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< "+str(valide[i])+" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        print("we have a proplem")
                        os.system("kill $(pgrep -f 'python3 "+str(valide[i])+".py')")
                        print("old bot was killed")
                        x = threading.Thread(target=start_bot1, args=(valide[i],))
                        x.start()  
                        file = open("err.txt","w")
                        file.write("0")
                        file.close()     
                        print("bot has repaired")
                        time.sleep(1)
                    
                    
            time.sleep(5)
        except Exception as e:
            time.sleep(5)
            print(e)


circle()
