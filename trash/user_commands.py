import json
import os
import re
import threading

import paramiko

from domains.user import check_login_response, User

class UserCommands:
    def __init__(self, user):
        self.user = user  # Reference to the User instance

    def ssh(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname='192.168.1.74', username='pi', password='<PASSWORD>')

    @classmethod
    def user_login(cls, username, password):
        try:
            login_data = {
                "Username": username,
                "Password": password,
                "Command": "login"
            }

            login_data = json.dumps(login_data)

            aes_security = AESecurity()
            encrypted_data, nonce = aes_security.encrypt(login_data)

            with open(f'/home/pi/login_data.enc', 'wb') as file:
                file.write(encrypted_data)

            # SSH connection to Raspberry Pi
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname='192.168.1.74', username='pi', password='<PASSWORD>')

            # sending the encrypted login data
            sftp = ssh_client.open_sftp()
            sftp.put(f'/home/pi/login_data.enc', f'/home/pi/{username}_login_data.enc')
            sftp.close()

            response = check_login_response(ssh_client, username)

            ssh_client.close()
            return response

        except Exception as e:
            print(f"Error during login: {e}")

    @classmethod
    def user_registration(cls, username, password, password_confirm, pictures):
        try:
            if password != password_confirm:
                print("Passwords do not match")
                return

            if len(password) < 8:
                print("Password must be at least 8 characters")
                return

            if not re.search(r'[A-Z]', password):
                print("Password must contain at least one capital letter.")
                return

            if "ndl" not in password:
                print('Password must contain the substring "ndl".')
                return

            if len(pictures) != 6:
                print("Exactly 6 pictures are required")
                return

            user = User(username=username, password=password, pictures=pictures, path='/local/picture/folder')

            aes_key = os.urandom(32)
            aes_security = AESecurity(aes_key)

            upload_thread = threading.Thread(target=user.upload_data_to_pi, args=(aes_security,))
            upload_thread.start()

        except Exception as e:
            print(f"Error during registration: {e}")

    def create_new_member(member_name, pictures):
        try:
            if len(pictures) != 6:
                print("Exactly 6 pictures are required")
                return

            member_data = {
                "Name": member_name,
                "Pictures": pictures,
                "Command": "create_member"
            }

            member_json = json.dumps(member_data)

            aes_security = AESecurity()
            encrypted_data, nonce = aes_security.encrypt(member_json)

            # asyncio.run(websocket_connection.send(ciphertext))

        except Exception as e:
            print(f"Error during create_member: {e}")


    def change_password(username, new_password, confirm_password):
        try:
            if confirm_password != new_password:
                print("Passwords do not match")
                return

            if len(new_password) < 8:
                print("Password must be at least 8 characters")
                return

            if not re.search(r'[A-Z]', new_password):
                print("Password must contain at least one capital letter.")
                return

            if "ndl" not in new_password:
                print('Password must contain the substring "ndl".')
                return

            password_data = {
                "Username": username,
                "NewPassword": new_password,
                "Command": "change_password"
            }

            pasword_json = json.dumps(password_data)

            # aes_security = AESecurity(aes_key)  # Use your AES security class
            # ciphertext, nonce = aes_security.encrypt(password_json)

        except Exception as e:
            print(f"Error changing password: {e}")
    @classmethod
    def user_login(username, password):
        try:
            login_data = {
                "Username": username,
                "Password": password,
                "Command": "login"
            }

            login_data = json.dumps(login_data)

            aes_security = AESecurity()
            encrypted_data, nonce = aes_security.encrypt(login_data)

            with open(f'/home/pi/login_data.enc', 'wb') as file:
                file.write(encrypted_data)

            # SSH connection to Raspberry Pi
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname='192.168.1.74', username='pi', password='<PASSWORD>')

            # sending the encrypted login data
            sftp = ssh_client.open_sftp()
            sftp.put(f'/home/pi/login_data.enc', f'/home/pi/{username}_login_data.enc')
            sftp.close()

            response = check_login_response(ssh_client, username)

            ssh_client.close()
            return response

        except Exception as e:
            print(f"Error during login: {e}")

