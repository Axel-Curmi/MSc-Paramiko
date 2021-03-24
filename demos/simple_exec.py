from paramiko import (SSHClient)
from paramiko.config import SSH_PORT

PYSECUBE_PIN = b"test"

def main() -> int:
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="Execute command on remote host with SSH")
    parser.add_argument("--host", "-H", type=str, required=True)
    parser.add_argument("--username", "-u", type=str, required=True)
    parser.add_argument("--password", "-p", type=str, required=True)
    parser.add_argument("--command", "-c", type=str, required=True)
    args = parser.parse_args()

    with SSHClient() as client:
        client.load_system_host_keys()
        client.connect(args.host, SSH_PORT, args.username, args.password,
                       pysecube_pin = PYSECUBE_PIN)
        print(f"Connected with {args.host}")

        _, stdout, _ = client.exec_command(args.command)
        print(stdout.read().decode())

    return 0

if __name__ == "__main__":
    exit(main())
