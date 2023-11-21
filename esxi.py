from ssh import SSH
import re

class ESXI():

    def __init__(self,username,password,device_ip):
        self.username = username
        self.password = password
        self.device_ip = device_ip

    '''Esxi SSH does not work with netmiko, setup SSH with paramiko'''
    def paramiko_connect_to_esxi(self):
        self.esxi_ssh = SSH(self.username,self.password)
        self.esxi_ssh.paramiko_connect(self.device_ip)
    '''SSH into ESXI host, and run commands
    This will gather the output which the ESXI host provides for a location of the backup. This will then call another 
    method to parse the data'''
    def esxi_run_backup_command(self):
        self.esxi_ssh.paramiko_send_command('vim-cmd hostsvc/firmware/sync_config')
        self.esxi_file_location_raw = self.esxi_ssh.paramiko_send_command('vim-cmd hostsvc/firmware/backup_config')
        self.parse_esxi_config()

    '''Regex both the file folder location, which by default looks like:
    'Bundle can be downloaded at : http://*/downloads/52cb3cd1-fed5-65dd-f869-faa18557f727/configBundle-localhost.tgz\n
    We only want the crazy number/config-bundle and hostname '''
    def parse_esxi_config(self):
        #Because stdout which is the esxi_file_location_raw - is a list, not the greatest way, but getting it to look at the first entry
        #because we know that there will only be one item in the stdout list when running agaisnt esxi
        self.esxi_file_location = re.findall('http://\*/downloads/(.+)',self.esxi_file_location_raw[0]) #find the name of the file after downloads
        self.esxi_file_location_hostname = re.findall('http://\*/downloads/.+/(configBundle-.+)',self.esxi_file_location_raw[0]) #find the name of the host which is after configBundle-
    '''Copy configuration over SFTP, and store it locally. Then return the file name incase we want to copy this to another location'''
    def copy_esxi_configuration(self):
        self.esxi_ssh.paramiko_sftp_setup()
        self.esxi_ssh.paramiko_sftp('/scratch/downloads/'+self.esxi_file_location[0],self.esxi_file_location_hostname[0])
        return self.esxi_file_location_hostname[0]
