from paramiko import (SSHClient)
from paramiko.config import SSH_PORT

import logging

from pysecube.wrapper import Wrapper

logging.basicConfig()
logging.getLogger("paramiko").setLevel(logging.DEBUG)

# logging.basicConfig()
# logging.getLogger("pysecube").setLevel(logging.DEBUG)

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

    pysecube = Wrapper(b"test")
    pysecube.crypto_set_time_now()

    try:
        with SSHClient() as client:
            client.load_system_host_keys()

            client.connect(args.host, SSH_PORT, args.username, args.password,
                        disabled_algorithms={
                            # Force KEX engine to use DH Group 14 with SHA256
                            "kex": [
                                    "curve25519-sha256@libssh.org",
                                    "ecdh-sha2-nistp256",
                                    "ecdh-sha2-nistp384",
                                    "ecdh-sha2-nistp521",
                                    "diffie-hellman-group16-sha512",
                                    "diffie-hellman-group-exchange-sha256",
                                    "diffie-hellman-group-exchange-sha1",
                                    "diffie-hellman-group14-sha1",
                                    "diffie-hellman-group1-sha1",
                            ]
                        },
                        pysecube=pysecube
            )
            # client.connect(args.host, SSH_PORT, args.username, args.password)
            print(f"Connected with {args.host}")

            _, stdout, _ = client.exec_command(args.command)
            print(stdout.read().decode())
    finally:
        pass
    return 0

if __name__ == "__main__":
    exit(main())
