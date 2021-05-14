from paramiko import (SSHClient)
from paramiko.config import SSH_PORT

from pysecube.wrapper import Wrapper

import time

# import logging
# logging.basicConfig()
# logging.getLogger("paramiko").setLevel(logging.DEBUG)

PYSECUBE_PIN = b"test"
HOSTNAME = "192.168.37.136"
USERNAME = "user"
PASSWORD = "password"
COMMAND = "uname"

def main() -> int:
    pysecube = Wrapper(PYSECUBE_PIN)
    pysecube.crypto_set_time_now()

    client = SSHClient()
    client.load_system_host_keys()

    print(f"Connecting with {HOSTNAME}:{SSH_PORT}")
    client.connect(HOSTNAME, SSH_PORT, USERNAME, PASSWORD, disabled_algorithms={
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
    }, pysecube=pysecube)
    print("Connected successfully")

    channel = client.get_transport().open_channel("session")
    channel.exec_command("uname -a")
    stdout = channel.makefile("r", -1)

    # Wait for an EOF to be received
    while not channel.eof_received:
        time.sleep(1)

    channel.close()
    print(stdout.read().decode())
    stdout.close()

    client.close()
    pysecube.destroy()
    return 0

if __name__ == "__main__":
    exit(main())
