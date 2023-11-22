# satellite_dr
La solution Red Hat Satellite n'offre pas de solution native de DR.  
Le serveur Satellite est une VM tournant la version 6.12 sour RHEL 8, par dessus ESX.  

## La methode recommandée par RHEL: ACTIVE/PASSIVE
1. prendre un backup full/incremental sur le primary
2. restorer le backup sur le secondary  
!! ATTN !! make sure you use the very same IP/FQDN on both primary and secondary

## We have an F5, can we leverage on that ?  
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





