from ssh import SSH
from nokia import Nokia
from datetime import date
from huawei import Huawei
from pfsense import Pfsense
from proxmox import Proxmox
from freenas import Freenas
from secrets import Secrets
from esxi import ESXI
import shutil
import argparse
def get_date():
    '''gets today's date, and formats it as MMDDYY'''
    today = date.today()
    today_format = today.strftime("%m/%d/%Y").replace("/", "")
    return today_format

def main(*args):

    '''Arg parser to define what the user would like to backup. This is for use with CLI running '''
    parser = argparse.ArgumentParser(description='Program to run backups across multiple platforms')
    parser.add_argument('--pfsense', action='store_true',help='run backup for pfsense')
    parser.add_argument('--proxmox', action='store_true',help='run backup for proxmox')
    parser.add_argument('--proxmox-multi', action='store_true',help='run backup for more than 1 proxmox node')
    parser.add_argument('--nokia',action='store_true',help='run backup for Nokia devices')
    parser.add_argument('--nokia_multi',action='store_true',help='run backup for more than 1 Nokia device')
    parser.add_argument('--huawei',action='store_true',help='run backup for Huawei devices')
    parser.add_argument('--freenas',action='store_true',help='run backup for freenas devices')
    parser.add_argument('--location',action='store',help='Location for saving backup files')
    parser.add_argument('--esxi',action='store_true',help='run backup for Esxi devices')
    argsparse, unknown = parser.parse_known_args()
    
    today_format = get_date() #Get today's date, so this can be used to save files in the future
    '''File names are setup as blank, so for moving function it does not error out if the var doesn't exist'''
    nokia_backup_filename = ''
    huawei_backup_filename = ''
    proxmox_backup_filename = ''
    freenas_backup_filename = ''
    pfsense_backup_filename = ''
    esxi_backup_filename = ''
    if argsparse.nokia:
        print ('running Nokia backup')
        nokia_backup_filename = 'nokiabackup%s.cfg' % (today_format) #prep name to open txt file with
        nokia_backup_file = open(nokia_backup_filename, "w") #write to text file with nokia backup name
        nokia_ssh = Nokia(Secrets.nokia['username'],Secrets.nokia['password']) #Setup the Nokia object
        nokia_ssh.nokia_ssh_session(Secrets.nokia['device_ip']) #SSH into device, with secrets from secret file
        nokia_ssh.nokia_backup() #Run the backup
        nokia_backup_file.write(nokia_ssh.nokia_config) #Take the output, and save this to the file
        nokia_backup_file.close()
    if argsparse.nokia_multi:
        print ('running Nokia multi backup')
        for router in Secrets.nokia_multi.keys():
            nokia_backup_filename = 'nokiabackup%s.cfg' % (today_format+router) #prep name to open txt file with
            nokia_backup_file = open(nokia_backup_filename, "w") #write to text file with nokia backup name
            nokia_ssh = Nokia(Secrets.nokia_multi[router]['username'],Secrets.nokia_multi[router]['password']) #Setup the Nokia object
            nokia_ssh.nokia_ssh_session(Secrets.nokia_multi[router]['device_ip']) #SSH into device, with secrets from secret file
            nokia_ssh.nokia_backup() #Run the backup
            nokia_backup_file.write(nokia_ssh.nokia_config) #Take the output, and save this to the file
            nokia_backup_file.close()
    if argsparse.huawei:
        print ('running Huawei backup')
        huawei_backup_filename = 'huaweibackup%s.txt' %(today_format) #prep name to open txt file with
        huawei_backup_file = open(huawei_backup_filename,"w") #write to file with huawei name
        huawei_ssh = Huawei(Secrets.huawei['username'],Secrets.huawei['password']) #Setup the Huawei object
        huawei_ssh.huawei_ssh_session(Secrets.huawei['device_ip']) #start an SSH session to device defined in screts
        huawei_ssh.huawei_backup() #run the backup
        huawei_backup_file.write(huawei_ssh.huawei_config) #save the output to a file
        huawei_backup_file.close()
    if argsparse.pfsense:
        print ('running pfsense backup')
        #Create the pfsense object. Needs local creds and also API parameters
        pfsense = Pfsense(Secrets.pfsense['username'],Secrets.pfsense['password'],Secrets.pfsense['device_ip'],Secrets.pfsense['apikey'],Secrets.pfsense['apivalue'])
        pfsense.get_pfsense_config() #Run API with pfsense to generate config file
        pfsense_backup_filename = pfsense.copy_pfsense_config(today_format) #Copy the configuration from pfsense, to local disk
    if argsparse.proxmox:
        print ('running Proxmox backup')
        #Create proxmox object
        proxmox_backup = Proxmox(Secrets.proxmox['username'],Secrets.proxmox['password'],Secrets.proxmox['device_ip'],Secrets.proxmox['hostname'])
        proxmox_backup.connect_to_proxmox() #Create ssh session to proxmox
        proxmox_backup.create_proxmox_backup_folder(today_format) #create a new folder for the various backup files
        proxmox_backup.tar_proxmox_config() #tar/zip the folder up, so this can be downloaded
        proxmox_backup_filename = proxmox_backup.copy_proxmox_backup() #SCP the files to local machine
    if argsparse.proxmox_multi:
        print ('running Proxmox backup')
        #Create proxmox object and loop through secrets that has multiple hosts in it
        for server in Secrets.proxmox_multi.keys():
            proxmox_backup = Proxmox(Secrets.proxmox_multi[server]['username'],Secrets.proxmox_multi[server]['password'],Secrets.proxmox_multi[server]['device_ip'],server)
            proxmox_backup.connect_to_proxmox() #Create ssh session to proxmox
            proxmox_backup.create_proxmox_backup_folder(today_format) #create a new folder for the various backup files
            proxmox_backup.tar_proxmox_config() #tar/zip the folder up, so this can be downloaded
            proxmox_backup_filename = proxmox_backup.copy_proxmox_backup() #SCP the files to local machine
    if argsparse.freenas:
        print ('running Freenas backup')
        #Setup freenas object
        freenas_backup = Freenas(Secrets.freenas['username'],Secrets.freenas['password'],Secrets.freenas['device_ip'])
        freenas_backup.paramiko_connect_to_freenas() #setup paramiko session to freenas as it is better supported
        freenas_backup.paramiko_copy_configuration(today_format) #prep folder for freenas backup on freenas machine
        freenas_backup_filename = freenas_backup.copy_freenas_backup() #scp backup files locally
    if argsparse.esxi:
        print ('running esxi backup')
        esxi_backup = ESXI(Secrets.esxi['username'],Secrets.esxi['password'],Secrets.esxi['device_ip'])
        esxi_backup.paramiko_connect_to_esxi()
        esxi_backup.esxi_run_backup_command()
        esxi_backup_filename = esxi_backup.copy_esxi_configuration()
    '''If the --location flag is specified, we are now assuming path is correct and will move the files from the local directory
    to the destination.'''
    if argsparse.location:
        if nokia_backup_filename:
            shutil.move(nokia_backup_filename,argsparse.location)
        if huawei_backup_filename:
            shutil.move(huawei_backup_filename,argsparse.location)
        if proxmox_backup_filename:
            shutil.move(proxmox_backup_filename,argsparse.location)
        if freenas_backup_filename:
            shutil.move(freenas_backup_filename,argsparse.location)
        if pfsense_backup_filename:
            shutil.move(pfsense_backup_filename,argsparse.location)
        if esxi_backup_filename:
            shutil.move(esxi_backup_filename,argsparse.location)
if __name__ == '__main__':
    import argparse
    main()