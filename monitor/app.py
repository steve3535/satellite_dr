from flask import Flask, request
import requests  
import time
import sys
from colorama import Fore,Style
import signal 

app = Flask(__name__)


def signal_handler(signal,frame):
    print(Style.RESET_ALL+"Interrupted by user ...")
    sys.exit(2)

def check_status():
    url="http://127.0.0.1:9001/status"
    res=requests.get(url)
    
    return res.json()

def monitor():
    print(Style.RESET_ALL)
    while True:
        x,y = check_status()[0]['live'],check_status()[1]['live']
        if not(x or y):
            print(Fore.RED+'!! CRIT !!'+Style.RESET_ALL+' >> both sites are down')
        elif x and y:
            print(Fore.RED+'!! CRIT !!'+Style.RESET_ALL+' >> both sites are up')
        else:
            print(Fore.GREEN+'STATUS OK')
        time.sleep(5)



if __name__ == "__main__":
    #app.run(host="0.0.0.0",debug=True,port=9002)
    signal.signal(signal.SIGINT,signal_handler)
    monitor()
    
