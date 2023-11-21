from ssh import SSH

class Freenas():

    def __init__(self,username,password,device_ip):
        self.username = username
        self.password = password
        self.device_ip = device_ip

    def connect_to_freenas(self):
        self.freenas_ssh = SSH(self.username, self.password)
        self.freenas_ssh.connect_to_device(self.device_ip, 'linux')

    def paramiko_connect_to_freenas(self):
        self.freenas_ssh = SSH(self.username,self.password)
        self.freenas_ssh.paramiko_connect(self.device_ip)

    def copy_configuration(self,date):
        self.date = date
        self.freenas_ssh.run_command('cp /data/freenas-v1.db /root/freenasconfig%s.db' % (self.date))

    def paramiko_copy_configuration(self, date):
        self.date = date
        self.freenas_ssh.paramiko_send_command('cp /data/freenas-v1.db /root/freenasconfig%s.db' % (self.date))

    def copy_freenas_backup(self):
        self.freenas_ssh.paramiko_connect(self.device_ip)
        freenas_backup_file_name = 'freenasconfig%s.db' % (self.date)
        self.freenas_ssh.paramiko_sftp(freenas_backup_file_name,freenas_backup_file_name)
        return freenas_backup_file_name