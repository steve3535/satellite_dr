import ssl
from pyVim.connect import SmartConnect,Disconnect
from pyVmomi import vim
import getpass
from flask import Flask, request, jsonify
import sys

from colorama import Fore,Style

MAX_DEPTH = 10
servers = [{'name':"VSL-PRO-SAT-001_LU712_BKP1.1_D_PRO",'state':""},{'name':"VSL-PRO-SAT-002_LU712_DC3",'state':""}]

app = Flask(__name__)

def check(vm, depth=1):
    live_flag = "**[LIVE]**"
    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > MAX_DEPTH:
            return
        vmlist = vm.childEntity
        for child in vmlist:
            check(child, depth+1)
        return
    if vm.summary.config.name == "VSL-PRO-SAT-002_LU712_DC3":
       #if vm.summary.runtime.powerState == "poweredOn":
           #print(Fore.YELLOW+f"{live_flag:12}"+Style.RESET_ALL+f"{vm.summary.config.name:40}"+Fore.GREEN+f"{vm.summary.runtime.powerState:10}")
        servers[1]['state']=vm.summary.runtime.powerState
        if servers[1]['state'] == "poweredOn":
            servers[1]['live']=True
        else:
            servers[1]['live']=False 
                          
       #else:
       #    live_flag=""
       #    print(f"{live_flag:12}{vm.summary.config.name:40}"+Fore.RED+f"{vm.summary.runtime.powerState:10}")
        
    if vm.summary.config.name == "VSL-PRO-SAT-001_LU712_BKP1.1_D_PRO":
        servers[0]['state']=vm.summary.runtime.powerState
        if servers[0]['state'] == "poweredOn":
            servers[0]['live']=True
        else:
            servers[0]['live']=False              
                
def swap(vm, depth=1):
    if hasattr(vm, 'childEntity'):
        if depth > MAX_DEPTH:
            return
        vmlist = vm.childEntity
        for child in vmlist:
            swap(child, depth+1)
        return
    if vm.summary.config.name in ("VSL-PRO-SAT-002_LU712_DC3","VSL-PRO-SAT-001_LU712_BKP1.1_D_PRO"):
       if vm.summary.runtime.powerState == "poweredOn":
           print(f"Shuting down {vm.summary.config.name} ...")
           vm.PowerOff()
                      
       else:
           print(f"Powering on {vm.summary.config.name} ...")
           vm.PowerOn()           

def verify():
    print("\n")
    try:
      context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
      context.verify_mode = ssl.CERT_NONE
      si = SmartConnect(host="lu309.lalux.local", user="mk417@lalux.local", pwd="XXXXXXXXXXXXXXXXX")
    except Exception as e:
        print("an err occured while connecting to ESX")
        sys.exit(1)
    content = si.RetrieveContent()
    for dc in content.rootFolder.childEntity:
      for vm in dc.vmFolder.childEntity:
          check(vm)
    print(Style.RESET_ALL)


@app.route('/status')
def status():
    #mdp = getpass.getpass(f"password for {getpass.getuser()}: ")
    verify()
    return jsonify(servers)

@app.route('/switch')
def switch():
    print("\n")
    try:
      context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
      context.verify_mode = ssl.CERT_NONE
      si = SmartConnect(host="lu309.lalux.local", user="mk417@lalux.local", pwd="MyFirstSonIsShine$$")
    except Exception as e:
        print("an err occured while connecting to ESX")
        sys.exit(1)
    content = si.RetrieveContent()
    for dc in content.rootFolder.childEntity:
      for vm in dc.vmFolder.childEntity:
          swap(vm)
    print(Style.RESET_ALL)
    return "\nSwicthed!\n"

# Start program
if __name__ == "__main__":    
    app.run(host="0.0.0.0",debug=True,port=9001)   
    
