from ssh import SSH

class Huawei():
    def __init__(self,username,password):
        self.username = username
        self.password = password
    '''Creates ongoing SSH session. Uses SSH class to actually form this'''
    def huawei_ssh_session(self,device_ip):
        self.device_ip = device_ip
        self.device_type = "huawei"
        self.huawei_device = SSH(self.username, self.password)
        self.huawei_device.connect_to_device(self.device_ip, self.device_type)
    '''Specific commands used to backup huawei device'''
    def huawei_backup(self):
        self.huawei_device.run_command("screen-length 0 temporary")
        self.huawei_config = self.huawei_device.run_command("display saved-configuration")
