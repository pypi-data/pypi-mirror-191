import argparse
import os
from ssh import SSH

parser = argparse.ArgumentParser()
parser.add_argument('--user', required=True)
parser.add_argument('--project', required=True)
parser.add_argument('--path', required=True, help='e.g) /path/to/neural-quant')

args = parser.parse_args()


def main():
    SCHEDULER_IP = "54.180.160.135"
    SCHEDULER_USER = "seilna"
    SCHEDULER_PORT = 22

    os.system(f"ssh-copy-id -f {SCHEDULER_USER}@{SCHEDULER_IP} -p {SCHEDULER_PORT}")

    ssh = SSH(SCHEDULER_IP, SCHEDULER_PORT, SCHEDULER_USER)

    if ssh.is_exists(f"/home/{SCHEDULER_USER}/workspace/{args.project}"):
        print(f"Project {args.project} already exists.")
        exit(1)

    else:
        ssh.ssh_copy(args.path, f"/home/{SCHEDULER_USER}/workspace/{args.project}")
        print(f"[Submit Project] {args.project}")

if __name__ == '__main__':
    main()