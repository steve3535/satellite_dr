import requests  
import time
import sys
from colorama import Fore,Style
import signal 

def signal_handler(signal,frame):
    print(Style.RESET_ALL+"Interrupted by user ...")
    sys.exit(2)

def check_status():
    # set to your backend service name
    URL="http://backend.satellite-dr.svc.cluster.local:9001/status"
    res=requests.get(URL)
    
    return res.json()

def monitor():
    while True:
        x,y = check_status()[0]['live'],check_status()[1]['live']
        if not(x or y):
            print(Fore.RED+time.strftime('%Y-%m-%d-%H:%M:%S')+' CRIT: both sites are down')
            print(Fore.YELLOW+time.strftime('%Y-%m-%d-%H:%M:%S')+' WARN: Trying failover to DR ...')
            print(Style.RESET_ALL)
            URL="http://backend.satellite-dr.svc.cluster.local:9001/switchon/VSL-PRO-SAT-002_LU712_DC3"
            requests.get(URL)
        elif x and y:
            print(Fore.RED+time.strftime('%Y-%m-%d-%H:%M:%S')+' CRIT both sites are up')
            print(Fore.YELLOW+time.strftime('%Y-%m-%d-%H:%M:%S')+' WARN: Try shutting down DR ...')
            print(Style.RESET_ALL)
            URL="http://backend.satellite-dr.svc.cluster.local:9001/switchoff/VSL-PRO-SAT-002_LU712_DC3"
            requests.get(URL)
        else:
            print(Fore.GREEN+time.strftime('%Y-%m-%d-%H:%M:%S')+' STATUS OK'+Style.RESET_ALL)
        time.sleep(60)


if __name__ == "__main__":
    signal.signal(signal.SIGINT,signal_handler)
    monitor()
    
