# Infrastructure-Backup

Tool to centralize backup across multiple services. Most of the backups are acoomplished via SSH and gathering config files and copying them to your local/remote machine for backup. 

**Usage**

1.  Edit Secrets-EXAMPLE file with the appropriate values  
2.  Save file as secrets.py  
3.  run program with python3 backuputil.py --h to see all possible parameters  

python3 backuputil.py -h  
usage: backuputil.py [-h] [--pfsense] [--proxmox] [--proxmox-multi] [--nokia] [--nokia_multi] [--huawei] [--freenas] [--location LOCATION] [--esxi]  

Program to run backups across multiple platforms  

optional arguments:  
  -h, --help           show this help message and exit  
  --pfsense            run backup for pfsense  
  --proxmox            run backup for proxmox  
  --proxmox-multi      run backup for more than 1 proxmox node  
  --nokia              run backup for Nokia devices  
  --nokia_multi        run backup for more than 1 Nokia device  
  --huawei             run backup for Huawei devices  
  --freenas            run backup for freenas devices  
  --location LOCATION  Location for saving backup files  
  --esxi               run backup for Esxi devices  

  Pick from the list to run on the services that should be backed up, and have valid entires in secrets.py. These will by default copy to the same directory, or to a location you choose with --location
