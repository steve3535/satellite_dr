import ssl
from pyVim.connect import SmartConnect,Disconnect
from pyVmomi import vim
import getpass
from colorama import Fore,Back,Style

MAX_DEPTH = 10
servers = []
def status(vm, depth=1):
    server = {}
    live_flag = "**[LIVE]**"
    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > MAX_DEPTH:
            return
        vmlist = vm.childEntity
        for child in vmlist:
            status(child, depth+1)
        return
    if vm.summary.config.name in ("VSL-PRO-SAT-002_LU712_DC3","VSL-PRO-SAT-001_LU712_BKP1.1_D_PRO"):
       if vm.summary.runtime.powerState == "poweredOn":
           print(Fore.YELLOW+f"{live_flag:12}"+Style.RESET_ALL+f"{vm.summary.config.name:40}"+Fore.GREEN+f"{vm.summary.runtime.powerState:10}")
           server['name']=vm.summary.config.name
           server['state']=vm.summary.runtime.powerState
           server['live']=1
           servers.append(server)
       else:
           live_flag=""
           print(f"{live_flag:12}{vm.summary.config.name:40}"+Fore.RED+f"{vm.summary.runtime.powerState:10}")
           server['name']=vm.summary.config.name
           server['state']=vm.summary.runtime.powerState
           server['live']=0
           servers.append(server)

def switch():
    pass

def main():
    print("\n")
    try:
      context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
      context.verify_mode = ssl.CERT_NONE
      si = SmartConnect(host="lu309.lalux.local", user="mk417@lalux.local", pwd="MyFirstSonIsShine$$")
    except Exception as e:
        print("an err occured while connecting to ESX")

    content = si.RetrieveContent()
    for dc in content.rootFolder.childEntity:
      for vm in dc.vmFolder.childEntity:
          status(vm)
    print(Style.RESET_ALL)
    print(servers)

# Start program
if __name__ == "__main__":
    main()
