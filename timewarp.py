#!/usr/bin/python
# Timewarp.py - bulk NTP and timezone adjustment for Junos devices
# ben.dale@gmail.com
# curl http://10.0.0.81:8080/rpc?stop-on-error=1 -u ":" -H "Content-Type: application/xml" -H "Accept: application/xml" -d "<rpc> <edit-config> <target> <candidate/> </target> <config> <configuration> <system> <host-name>HOTWINGS-BABY</host-name> </system> </configuration> </config> </edit-config> </rpc>"


import re
from requests import Request, Session

CONST_REST_PROTOCOL = 'http'
CONST_REST_PORT = '8080'
CONST_TIMEZONE = 'Australia/Brisbane'
CONST_TIMEZONE_RPC = '<rpc> <edit-config> <target> <candidate/> </target> <config> <configuration> <system> <time-zone>' + CONST_TIMEZONE + '</host-name> </system> </configuration> </config> </edit-config> </rpc>'
CONST_NTP_SERVERS = '1.2.3.4'
CONST_TIME_HEADER = 'rpc?stop-on-error=1 -u ":" -d 
CONST_HEADERS = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}


sys.stdout.write("Timewarp\n\n")
if len(sys.argv) != 2:
	sys.stdout.write("Error: Missing parameter\n")
	sys.stdout.write("Usage: timewarp <hostlist.csv>\n")
	sys.exit()
	
username = raw_input('Username: ')
password = getpass('Password: ')
sys.stdout.write(". - success\n")
sys.stdout.write("x - error\n")

deviceInventory = []

# Regex for routable IP addresses (1.0.0.0-223.255.255.255)
inetRegex = re.compile("^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-1][0-9]|22[0-3])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$") 

sys.stdout.write("Reading device list: ")
sys.stdout.flush()
hostsfile = open(str(sys.argv[1]),'r')
for hostAddress in hostsfile:
	if inetRegex.match(str(hostAddress)):
		sys.stdout.write('.')
		sys.stdout.flush()
		
        device_url = CONST_REST_PROTOCOL + '://' + str(hostAddress) + ':' + CONST_REST_PORT + '/rpc/' + CONST_COMMAND
	else:	
		sys.stdout.write("x")
		sys.stdout.flush()
		deviceInventory.append({"IP Address":str(hostAddress).rstrip('\n'),"Serial Number":"IP Address Error","Model":"N/A"})


get_system_information = requests.get('http://10.0.0.81:8080/rpc/get-system-information', auth=('root', 'juniper1'))

print get_system_information.text



sys.stdout.write('\n')
for device in deviceInventory:
	line = device["IP Address"] + ',' + device["Serial Number"] + ',' + device ["Model"] + '\n'
	sys.stdout.write(line)
	sys.stdout.flush()