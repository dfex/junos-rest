#!/usr/bin/python
# Timewarp.py - bulk NTP and timezone adjustment for Junos devices
# ben.dale@gmail.com
# curl http://10.0.0.81:8080/rpc?stop-on-error=1 -u ":" -H "Content-Type: application/xml" -H "Accept: application/xml" -d "<rpc> <edit-config> <target> <candidate/> </target> <config> <configuration> <system> <host-name>HOTWINGS-BABY</host-name> </system> </configuration> </config> </edit-config> </rpc>"
# curl http://10.0.0.81:8080/rpc/commit/ -u ":" -H "Content-Type: application/xml" -H "Accept: application/xml" -d ""


import re
import sys
import json
import requests
from getpass import getpass


REST_PROTOCOL = 'http'
REST_PORT = '8080'
TIME_ZONE = 'Australia/Brisbane'
NTP_SERVER = '10.0.254.10'

TIMEZONE_RPC = '<rpc> <edit-config> <target> <candidate/> </target> <config> <configuration> <system> <time-zone>' + TIME_ZONE + '</time-zone> </system> </configuration> </config> </edit-config> </rpc>'
NTP_RPC =      '<rpc> <edit-config> <target> <candidate/> </target> <config> <configuration> <system> <ntp> <server> <name>' + NTP_SERVER + '</name> </server> </ntp> </system> </configuration> </config> </edit-config> </rpc>'
SET_DATE_NTP_RPC = '/request-set-date-ntp'
HEADERS = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
COMMIT_RPC = '/commit'

sys.stdout.write("Timewarp\n\n")
if len(sys.argv) != 2:
    sys.stdout.write("Error: Missing parameter\n")
    sys.stdout.write("Usage: timewarp <hostlist.csv>\n")
    sys.exit()

username = raw_input('Username: ')
password = getpass('Password: ')

deviceInventory = []

# Regex for routable IP addresses (1.0.0.0-223.255.255.255)
inetRegex = re.compile("^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-1][0-9]|22[0-3])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$") 

sys.stdout.flush()
hostsfile = open(str(sys.argv[1]),'r')
for hostAddress in hostsfile:
    hostIP = hostAddress.rstrip('\n')
    if inetRegex.match(hostIP):
        device_rpc_url = REST_PROTOCOL + '://' + hostIP + ':' + REST_PORT + '/rpc'
        if requests.post(device_rpc_url, auth=(username, password), headers=HEADERS, data=TIMEZONE_RPC).status_code==200:
            print "Applied Timezone Configuration to " + hostIP
        else:
            print "Timezone configuration failed on " + hostIP
        if requests.post(device_rpc_url, auth=(username, password), headers=HEADERS, data=NTP_RPC).status_code==200:
            print "Applied NTP Configuration to " + hostIP
        else:
            print "NTP Configuration failed on " + hostIP
        if requests.post(device_rpc_url + COMMIT_RPC, auth=(username, password), headers=HEADERS).status_code==200:
            print "Committed configuration to " + hostIP
        else:
            print "Configuration commit failed on " + hostIP
        if requests.post(device_rpc_url + SET_DATE_NTP_RPC, auth=(username, password), headers=HEADERS).status_code==200:
            print "Synchronised NTP on node " + hostIP
        else:
            print "NTP synchronisation failed on node " + hostIP
        print "\n"
    else:
        print "Invalid host IP address: "+ hostIP