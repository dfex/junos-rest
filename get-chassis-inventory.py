import requests

get_chassis_inventory = requests.get('http://10.0.0.81:8080/rpc/get-chassis-inventory', auth=('root', 'juniper1'))

print get_system_information.text