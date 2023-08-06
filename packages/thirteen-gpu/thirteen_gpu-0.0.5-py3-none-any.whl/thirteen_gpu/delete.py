import argparse
from .ssh import SSH

parser = argparse.ArgumentParser()
parser.add_argument('--user', required=True)
parser.add_argument('--project', required=True)

args = parser.parse_args()

def main():
    SCHEDULER_IP = "54.180.160.135"
    SCHEDULER_USER = "seilna"
    SCHEDULER_PORT = 22

    ssh = SSH(SCHEDULER_IP, SCHEDULER_PORT, SCHEDULER_USER)
    
    if ssh.is_exists(f"/home/{SCHEDULER_USER}/workspace/{args.project}"):
        ssh.ssh_exec_command(
            f"rm -rf /home/{SCHEDULER_USER}/workspace/{args.project}"
        )
        print(f"[Delete Project] {args.project}")

    else:
        print(f"[Delete Project] {args.project} is not exists")

if __name__ == "__main__":
    main()
