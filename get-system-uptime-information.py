import requests

get_system_information = requests.get('http://10.0.0.81:8080/rpc/get-system-uptime-information', auth=('root', 'juniper1'))

print get_system_information.text