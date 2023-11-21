import paramiko
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi
import json
from ssh import SSH
class Pfsense:

    def __init__(self,username,password,device_ip,api_key,api_secret):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.api_secret = api_secret
        self.device_ip = device_ip
        self.PfsenseFauxapi = PfsenseFauxapi(self.device_ip, self.api_key,self.api_secret)

    def get_pfsense_config(self):
        config = self.PfsenseFauxapi.config_get()
        rawoutput = json.dumps(
            self.PfsenseFauxapi.config_backup())

        jsonObject = json.loads(rawoutput)
        self.pfsense_config_name = jsonObject['data']['backup_config_file']

    def copy_pfsense_config(self,today_format):
        self.pfsense_ssh = SSH(self.username,self.password)
        self.pfsense_ssh.paramiko_connect(self.device_ip)
        pfsense_config_file_name = 'pfsense-config%s.xml' % (today_format)
        self.pfsense_ssh.paramiko_sftp(self.pfsense_config_name,'pfsense-config%s.xml' % (today_format))
        return pfsense_config_file_name




