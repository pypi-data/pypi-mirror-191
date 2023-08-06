import paramiko
import os

class SSH(object):
    def __init__(self, ip, port, user):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(ip, port, user)

        self.ip = ip 
        self.port = port
        self.user = user
    
    def ssh_exec_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode()
    
    def ssh_copy(self, src, dst):
        os.system(
            f"rsync -qrve 'ssh -p {self.port}' --include='*/' --include='*.sh' --include='*.py' --include='*.json' --exclude='*' {src}/ {self.user}@{self.ip}:{dst}"
        )
    
    def is_exists(self, path):
        out = self.ssh_exec_command(f"ls {path}")
        return out != ""
        

def ssh_exec_command(ip, port, user, command: str):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip, port, user)
    except:
        from IPython import embed; embed()
    stdin, stdout, stderr = ssh.exec_command(command)
    
    return stdout.read().decode()

def ssh_copy(ip, port, user, src, dst):
    os.system(f"rsync -qrve 'ssh -p {port}' --include='*/' --include='*.sh' --include='*.py' --include='*.json' --exclude='*' {src}/ {user}@{ip}:{dst}")
    
    
if __name__ == "__main__":
    import json
    workers = json.load(open('workers.json'))
    r = ssh_exec_command(workers["s1"]["ip"], workers["s1"]["port"], workers["s1"]["user"],
                            "docker ps --format '{{.Names}},{{.Status}}' --filter 'status=exited'")
    
    from IPython import embed; embed(header='')
