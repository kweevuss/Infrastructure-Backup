from ssh import SSH
import os

class Proxmox():

    def __init__(self,username,password,device_ip,hostname):
        self.username = username
        self.password = password
        self.device_ip = device_ip
        self.hostname = hostname

    def connect_to_proxmox(self):
        self.proxmox_ssh = SSH(self.username, self.password)
        self.proxmox_ssh.connect_to_device(self.device_ip, 'linux')

    def create_proxmox_backup_folder(self,date):
        self.date = date
        self.proxmox_ssh.run_command('mkdir proxmoxbackup%s' %(self.date+self.hostname))

    def tar_proxmox_config(self):
        self.proxmox_ssh.run_command('tar -cz /etc/pve | tar -xz -C proxmoxbackup%s' %(self.date+self.hostname))
        self.proxmox_ssh.run_command('tar -cz /etc/apt | tar -xz -C proxmoxbackup%s' %(self.date+self.hostname))
        self.proxmox_ssh.run_command('tar -cz /etc/network | tar -xz -C proxmoxbackup%s' % (self.date+self.hostname))
        self.proxmox_ssh.run_command('cp /etc/fstab /root/proxmoxbackup%s/fstab' % (self.date+self.hostname))
        self.proxmox_ssh.run_command('tar -czf proxmoxbackup%s.tar.gz proxmoxbackup%s/' % (self.date+self.hostname,self.date+self.hostname))
    def copy_proxmox_backup(self):
        self.proxmox_ssh.paramiko_connect(self.device_ip)
        proxmox_backup_folder_name = 'proxmoxbackup%s.tar.gz' % (self.date+self.hostname)
        self.proxmox_ssh.paramiko_sftp(proxmox_backup_folder_name,proxmox_backup_folder_name)
        return proxmox_backup_folder_name

