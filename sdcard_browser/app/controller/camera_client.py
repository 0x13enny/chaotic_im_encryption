import paramiko, os, subprocess
from paramiko.ssh_exception import SSHException, BadHostKeyException, NoValidConnectionsError

class Camera():
    def __init__(self,jumboID):
        self.camera_host = os.environ["CAMUSERID"]
        self.camera_pwd = os.environ["CAMPASSWORD"]
        self.camera_config = os.environ["CONFIG_INI"]
        self.jumboID = jumboID
        self.status = ""
        self.dir_structure={}
    def create_ssh_client(self):
        c = paramiko.SSHClient()
        try:
            # print('Connecting to camera...')
            c.load_system_host_keys()
            c.connect(self.jumboID+".umbocv.local", username=self.camera_host, password=self.camera_pwd)
            # print(self.jumboID, 'Camera is connected.')
            # logger.info("ssh client created")
            self.status = "Online"
            self.client = c
        except SSHException:
            try:
                # print('Add missing host key...')
                c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                c.connect(self.jumboID+".umbocv.local", username=self.camera_host, password=self.camera_pwd)
                # print(self.jumboID, 'Camera is connected.')
                # logger.info("ssh client created")
                self.status = "Online"
                self.client = c
            except BadHostKeyException:
                # print('Deleting unknown key...')
                subprocess.Popen('ssh-keygen -R {}'.format(self.jumboID), shell=True)
                c.connect(self.jumboID+".umbocv.local", username=self.camera_host, password=self.camera_pwd)
                # print(self.jumboID, 'Camera is connected.')
                # logger.info("ssh client created")
                self.status = "Online"
                self.client = c
        except NoValidConnectionsError:
            # print('Camera is currently offline.')
            # logger.info("Offline")
            self.status = "Offline"
            sys.exit(1)
        finally:
            return self.status
    def command(self,cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        result = [stdout.read().decode("ascii"),stderr.read().decode("ascii")]
        return result

    def get_dir_structure(self):
        
        dates=[]
        for date in self.command('ls /mnt/sdcard')[0].split('\n'):
            if date[0:2]=="20":
                dates.append(date)
        for date in dates:
            hour = self.command('ls /mnt/sdcard/{}'.format(date))[0].split('\n')
            del hour[hour.index("")]
            self.dir_structure.update({date:hour})
        return self.dir_structure

    def exit(self):
        self.client.close()