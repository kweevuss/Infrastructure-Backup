'''THIS FILE IS FOR AN EXAMPLE ONLY. PARAMETERS MUST BE ENTERED BELOW, AND THEN SAVE AS secrets.py'''

class Secrets():
    proxmox = {'username':'[username]',
               'password':'[password]',
               'device_ip': '[IP]'}
    freenas = {'username':'[username]',
               'password':'[password]',
               'device_ip': '[IP]'}
    nokia = {'username':'[username]',
             'password':'[password]',
             'device_ip': '[IP]'}
    huawei = {'username':'[username]',
              'password':'[password]',
              'device_ip' : '[IP]'}
    #Based on https://github.com/ndejong/pfsense_fauxapi which is for older versions and not tested recently on pfsense CE 2.6+
    pfsense = {'username':'[username]',
               'password':'[password]',
               'apikey': '[API KEY - Starts with PPF]',
               'apivalue': '[API value]',
               'device_ip': '[IP]'
               }
    #These can be expanded as much as you want with new dictionary entries
    proxmox_multi={'[hypervisor_1_name]': {'username':'[username]', 'password':'[password]','device_ip':'[IP]'},'[hypervisor_2_name]': {'username':'[username]', 'password':'[password]','device_ip':'[IP]'}}
    nokia_multi = {'[router_1_name]' : {'username': '[username]', 'password': '[password]', 'device_ip' : '[IP]'}, '[router_2_name]' : {'username': '[username]', 'password': '[password]', 'device_ip' : '[IP]'}}
