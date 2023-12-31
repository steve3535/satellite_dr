import ssl
from pyVim.connect import SmartConnect,Disconnect
from pyVmomi import vim
import getpass
from flask import Flask, request, jsonify
import sys
import os 

MAX_DEPTH = 10

app = Flask(__name__)

host=os.environ['host']
user=os.environ['user']
pwd=os.environ['pwd']
primary=os.environ['primary']
secondary=os.environ['secondary']

servers = [{'name':primary,'state':""},{'name':secondary,'state':""}]

def connect():
    try:
      context = ssl._create_unverified_context() #ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
      context.verify_mode = ssl.CERT_NONE # disable ssl verification 
      si = SmartConnect(host=host, user=user, pwd=pwd,sslContext=context)
    except Exception as e:
        print("an err occured while connecting to ESX")
        print(e) 
        sys.exit(1)
    content = si.RetrieveContent()
    return content

def powerup(vm, vmname, depth=1):
        if hasattr(vm, 'childEntity'):
          if depth > MAX_DEPTH:
             return
          vmlist = vm.childEntity
          for child in vmlist:
            powerup(child, vmname, depth+1)
          return
        if vm.summary.config.name == vmname:
           print(vmname)
           if vm.summary.runtime.powerState == "poweredOff":
             print(f"Starting {vm.summary.config.name} ...")
             vm.PowerOn()
           else:
             print("VM is already up")

def poweroff(vm, vmname, depth=1):
        if hasattr(vm, 'childEntity'):
          if depth > MAX_DEPTH:
             return
          vmlist = vm.childEntity
          for child in vmlist:
            poweroff(child, vmname, depth+1)
          return
        if vm.summary.config.name == vmname:
           print(vmname)
           if vm.summary.runtime.powerState == "poweredOn":
             print(f"Shutting down {vm.summary.config.name} ...")
             vm.PowerOff()
           else:
             print("VM is already down")

def check(vm, depth=1):
    if hasattr(vm, 'childEntity'):
        if depth > MAX_DEPTH:
            return
        vmlist = vm.childEntity
        for child in vmlist:
            check(child, depth+1)
        return
    if vm.summary.config.name == secondary:
        servers[1]['state']=vm.summary.runtime.powerState
        if servers[1]['state'] == "poweredOn":
            servers[1]['live']=True
        else:
            servers[1]['live']=False 
                          
    if vm.summary.config.name == primary:
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
    if vm.summary.config.name in (primary,secondary):
       if vm.summary.runtime.powerState == "poweredOn":
           print(f"Shuting down {vm.summary.config.name} ...")
           vm.PowerOff()
                      
       else:
           print(f"Powering on {vm.summary.config.name} ...")
           vm.PowerOn()           

def verify():
    content = connect()
    for dc in content.rootFolder.childEntity:
      for vm in dc.vmFolder.childEntity:
          check(vm)

@app.route('/status',methods=['GET'])
def status():
    verify()
    return jsonify(servers)


@app.route('/switchon/<vmname>')
def switchon(vmname):
    content = connect()
    for dc in content.rootFolder.childEntity:
      for vm in dc.vmFolder.childEntity:
          powerup(vm,vmname)
    return ""

@app.route('/switchoff/<vmname>')
def switchoff(vmname):
    content = connect()
    for dc in content.rootFolder.childEntity:
      for vm in dc.vmFolder.childEntity:
          poweroff(vm,vmname)
    return ""

@app.route('/switch')
def switch():
    content = connect()
    for dc in content.rootFolder.childEntity:
      for vm in dc.vmFolder.childEntity:
          swap(vm)
    return "\nSwicthed!\n"

# Start program
if __name__ == "__main__":    
    app.run(host="0.0.0.0",debug=True,port=9001)   

    
