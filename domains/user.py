import os
import json
import paramiko

from dataclasses import dataclass
from typing import List
from enum import Enum

class Command(Enum):
    REGISTER_USER = "register_user"
    LOCK = "lock"
    UNLOCK = "unlock"
    REMOVE_USER = "remove_user"
    CHANGE_PASSWORD = "change_password"
    LOGIN_USER = "login_user"

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
        try:
            sftp = ssh_client.open_sftp()
            remote_dir = f"/home/ndl/images/{self.username.replace(' ', '_')}"

            try:
                sftp.mkdir(remote_dir)
            except IOError:
                pass

            for picture in self.pictures:
                local_path = f"{self.path}/{picture}"  # Local path of the picture
                remote_path = f"{remote_dir}/{os.path.basename(picture)}"  # Remote path

                print(f"Uploading {local_path} to {remote_path}")
                sftp.put(local_path, remote_path)

            sftp.close()

        except Exception as e:
            print(e)

    #do I need this?
    def check_login_response(ssh_client, username):
        response_file = f"/home/pi/{username}_response.txt"

        try:
            with ssh_client.open_sftp() as sftp:
                with sftp.file(response_file, 'r') as file:
                    response = file.read()
                    print("Response from server:", response)
                    return response.strip()
        except Exception as e:
            print(f"Error checking response: {e}")
            return None

