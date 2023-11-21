from netmiko import Netmiko
import paramiko
import socket
import os
'''This class is resonsible for creating the actual ongoing SSH sessions used for other classes'''
class SSH:
    def __init__(self,username,password):
        self.username = username
        self.password = password
    '''Netmiko SSH session setup'''
    def ssh_session(self):
        self.net_connect = Netmiko(**self.device)
    '''Netmiko ssh parameter gathering '''
    def connect_to_device(self,host,device_type):
        self.host = host
        self.device_type = device_type
        self.device = {
            'device_type' : self.device_type,
            'host' : self.host,
            'username' : self.username,
            'password' : self.password
        }
        self.ssh_session()
    '''Run a command agaisnt setup netmiko SSH session'''
    def run_command(self,command):
        self.command = command
        self.output = self.net_connect.send_command(self.command)
        return self.output #is this needed? could I try to access this variable from the regular program?
    '''Create a paramiko ssh session'''
    def paramiko_connect(self,host):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=host, username=self.username, password=self.password)
    '''Using SSH session, copy a server file, locally'''
    def paramiko_sftp(self,server_file,local_file):
        self.server_file = server_file
        self.local_file = local_file
        ftp_client = self.ssh_client.open_sftp()
        ftp_client.get(self.server_file, self.local_file)
        ftp_client.close()
    '''Setup sftp session'''
    def paramiko_sftp_setup(self):
        self.ftp_client = self.ssh_client.open_sftp()
    '''Send command through paramiko ssh session'''
    def paramiko_send_command(self,command):
        self.paramiko_command = command
        stdin, stdout, stderr = self.ssh_client.exec_command(self.paramiko_command)
        stdout = stdout.readlines()
        #stout, will return a list with each line in it. Used for if we only need data back from paramko
        return stdout