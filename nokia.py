from ssh import SSH
'''Class used for Nokia based SROS devices'''

class Nokia:
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def nokia_ssh_session(self,device_ip):
        self.device_ip = device_ip
        self.device_type = "alcatel_sros"
        self.nokia_device = SSH(self.username, self.password)
        self.nokia_device.connect_to_device(self.device_ip, self.device_type)

    def nokia_backup(self):
        self.nokia_device.run_command("environment no more")
        self.nokia_config = self.nokia_device.run_command("admin display-config")



