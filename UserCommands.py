import json
import csv
import os
import re
from datetime import datetime
from multiprocessing.util import debug
from venv import logger

from paramiko.util import parse_ssh_config

from data_operations.data import FileTransfer
import paramiko
from urllib3 import request

from util.program_codes import ResetPassword
from PySide6.QtCore import Slot

from mqtt import MQTTServer
import hashlib
from PySide6.QtWidgets import QMessageBox

class UserCommands:
    def __init__(self, mqtt_client: MQTTServer):
        self._mqtt_client = mqtt_client
        self._current_user = None
        self._stored_password = None
        # main mqtt topics
        self._topic_ask_login = "login_ask"
        self._topic_ask_reg = "register"
        self._topic_ask_press_button = "press_button_ask"
        self._topic_ask_new_member = "add_member"
        self._topic_ask_change_password = "change_password"
        self._topic_ask_lock_unlock = "magnetic_lock"
        self._topic_ask_all_members = "all_members"
        self._topic_ask_active_members = "active_members"
        self._topic_delete_member = "delete_member"
        self._topic_edit_member = "edit_member_status"
        self._topic_delete_user = "delete_user"



        with open("/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/mqtt_responses_cached/session_token", "r") as file:
            self._token = file.readline().strip()


    #helper function for hashing the given password
    @classmethod
    def hash_password(cls, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def get_username(self):
        if self._current_user:
            return self._current_user
        else:
            logger.debug("No username found")

    def get_current_password(self):
        if self._stored_password:
            return self._stored_password
        else:
            logger.debug("There is no password stored")

    def read_file_to_variable(self, file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read().strip()  # Read the file and strip any trailing newlines
            return content
        except FileNotFoundError:
            logger.debug(f"File not found: {file_path}")
            return None
        except Exception as e:
            logger.debug(f"An error occurred while reading the file: {e}")
            return None

    def login(self, username, password):
        try:
            if not username or not password:
                raise Exception("Username and password cannot be empty")

            hashed_password = self.hash_password(password)
            self._stored_password = hashed_password
            self._current_user = username
            login_data = {
                "username": username,
                "password": hashed_password
            }

            login_json = json.dumps(login_data)
            self._mqtt_client.send_message(login_json, self._topic_ask_login)

        except Exception as e:
            raise e

    def register(self, username, password, repeat_password):
        try:
            if not username or not password or not repeat_password:
                raise Exception("Username and password cannot be empty")

            if password != repeat_password:
                raise Exception("Passwords do not match")

            if len(password) < 8:
                raise Exception("Password must be at least 8 characters")

            if not re.search(r'[A-Z]', password):
                raise Exception("Password must contain at least one uppercase letter")

            if "ndl" not in password:
                raise Exception("Password must contain the substring ndl")


            hashed_password = self.hash_password(password)

            register_data = {
                "username": username,
                "password": hashed_password,
            }

            register_data_json = json.dumps(register_data)

            register_request = {"value": register_data_json, "session_token": self._token}

            register_json = json.dumps(register_request)

            self._mqtt_client.send_message(register_json, self._topic_ask_reg)

            self._stored_password = hashed_password

        except Exception as e:
            raise e

    def create_new_member(self, member_name, path_pictures, path_pictures_server, status):
        try:
            if len(os.listdir(path_pictures)) != 6:
                raise Exception("Exactly 6 pictures are required.")

            if status.lower() == "temporary":
                date = self.read_file_to_variable("/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/date/selected_datetime.txt")
            else:
                date = ""

            member_data = {
                "name": member_name,
                "images_path": path_pictures_server,
                "authorization": status,
                "access_remaining_date_time": date
            }
            member_data_json = json.dumps(member_data)

            member_request = {"value": member_data_json, "session_token": self._token}

            member_json = json.dumps(member_request)
            self._mqtt_client.send_message(member_json, self._topic_ask_new_member)
            print(f"New member {member_name} added with status {status}.")

        except Exception as e:
            print(f"Error in create_new_member: {e}")
            raise

    def change_password(self, new_password):
        try:
            hashed_new_password = self.hash_password(new_password)

            new_password_data = {
                "username": self._current_user,
                "old_password": self._stored_password,
                "new_password": hashed_new_password
            }

            new_password_request = {"value": new_password_data, "session_token": self._token}

            new_password_json = json.dumps(new_password_request)
            # print(new_password_json)

            self._mqtt_client.send_message(new_password_json, self._topic_ask_change_password)

        except Exception as e:
            raise e

    def lock_unlock(self, current_state):
        pass

    def active_members(self):
        try:
            active_members_request = {"value": "", "session_token": self._token}
            active_members_data_json = json.dumps(active_members_request)
            self._mqtt_client.send_message(active_members_data_json, self._topic_ask_active_members)
        except Exception as e:
            raise e


    def all_members(self):
        try:
            all_members_request = {"value": "", "session_token": self._token}
            all_members_data_json = json.dumps(all_members_request)
            self._mqtt_client.send_message(all_members_data_json, self._topic_ask_all_members)

        except Exception as e:
            raise e

    #TODO
    def delete_member(self, member_id):
        try:
            # delete_data = {
            #     "id": member_id
            # }
            # delete_data_json = json.dumps(delete_data)

            delete_request = {"value": member_id, "session_token": self._token}

            delete_json = json.dumps(delete_request)
            print(delete_json)
            self._mqtt_client.send_message(delete_json, self._topic_delete_member)

        except Exception as e:
            raise e

    #TODO
    def change_member(self, member_id, member_status):
        try:
            # if member_status.lower() == "temporary":
            #     date = self.read_file_to_variable("/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/date/selected_datetime.txt")
            # else:
            #     date = ""

            change_data = {
                "id": member_id,
                "new_status": member_status,
                # "date": date
            }
            change_request = {"value": change_data, "session_token": self._token}
            change_json = json.dumps(change_request)
            print(change_json)
            self._mqtt_client.send_message(change_json, self._topic_edit_member)

        except Exception as e:
            raise e




