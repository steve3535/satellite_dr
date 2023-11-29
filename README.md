# sudo su - SRE #Ep001
# Disaster Recovery solution for Red Hat Satellite
Chapter 10 of the system administration manual implies there is no native DR solution for Satellite:  
https://access.redhat.com/documentation/en-us/red_hat_satellite/6.12/html/administering_red_hat_satellite/backing-up-satellite-server-and-capsule_admin   
Whats recommended is the old good backup/restore.  
!! Keep in mind that only one instance of Satellite should be active at anytime.  

## Step 0: Traditional & Manual

0. Topology
   
   ![](images/topo1.PNG)
   
2. backup primary  
3. restore seondary
   
**PS:** 
1) both primary and secondary must use same IP/FQDN
2) We have an F5, can we leverage on that ?
   
I setup a second VM in our DR site with the same IP , but powered off.  
I wanted to use F5. but the fact that the two servers should use same IP was somehow problematic ...  
I tought 1 VIP on top two real different IPs, and the F5 will present the VIP/FQDN to the clients, which also meman in that case that both servers remain up and F5 will load balance on either ... 
I dont know a bit about F5 ...  
Now that I am thinking I will test it with HAPROXY as well ...   
Ok, this option being out, door suddenly opened for an opprotunity to code :)   

## BYOS: Build Your Own Solution   
Idea:  
1. have python connect to ESX and regularly check powerstate of the two VMs
2. if both VM are down or both are up: this is not a healthy situation:
   * if both are up: we shutdown DR
   * if both are down: we up the Live
3. In other case the code should return OK
4. the code should be split into two components: backend and frontend - the backend is a REST api listening to requests and performing switch actions, the frontend is a CLI looping in checking the current sattus
5. all components will be containerized and eventually deployed as pods in a k8s cluster - for HA & ease of deployment

Improvements later on:
1. check should not only be limited to powerstate but retrieve via hammer api the actual state of Satellite
2. possibly integrate backup/restore routines for a true failover/switchover
3. Develop a web frontend to allow more actions and to kickstart a kind of platform engineering   

## Let the journeny begin !





