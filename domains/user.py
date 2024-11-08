import os
import json
import paramiko

from dataclasses import dataclass
from typing import List
from enum import Enum

# class Command(Enum):
#     REGISTER_USER = "register_user"
#     LOCK = "lock"
#     UNLOCK = "unlock"
#     REMOVE_USER = "remove_user"
#     CHANGE_PASSWORD = "change_password"
#     LOGIN_USER = "login_user"

class Role(Enum):
    ROOT = "root"
    MEMBER = "member"

@dataclass
class User:
    username: str
    password: str
    pictures: List[str]
    path: str = '/home/ndl/images'

    def ssh(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname='ndl@192.168.1.75', key_filename='/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/security/id_ed25519')
        print("SSH connection established successfully.")

    def to_json(self):
        user_data = {
            "Username": self.username,
            "Password": self.password,
            "Pictures": self.pictures,
            "Command": "register"
        }
        return json.dumps(user_data)

    def encrypt_data(self, aes_security):
        user_json = self.to_json()
        ciphertext, nonce = aes_security.encrypt(user_json)
        return ciphertext, nonce



    def upload_pictures(self, ssh_client):
        ssh_client = self.ssh()
        if ssh_client is None:
            print("SSH client not available. Exiting picture upload.")
            return
        try:
            sftp = ssh_client.open_sftp()
            remote_dir = f"/home/ndl/images/{self.username.replace(' ', '_')}"

            try:
                sftp.mkdir(remote_dir)
                print(f"Directory {remote_dir} created successfully.")
            except IOError:
                print(f"Directory {remote_dir} already exists.")

            for picture in self.pictures:
                local_path = f"{self.path}/{picture}"  # Local path of the picture
                remote_path = f"{remote_dir}/{os.path.basename(picture)}"  # Remote path

                print(f"Uploading {local_path} to {remote_path}")
                sftp.put(local_path, remote_path)

            sftp.close()
            print("All pictures uploaded successfully.")

        except Exception as e:
            print(f"Error during picture upload: {e}")
        finally:
            ssh_client.close()
            print("SSH connection closed.")

