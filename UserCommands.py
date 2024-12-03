import json

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
        self._topic_ask_lock_unlock = "lock_status"
        self._topic_ask_all_members = "all_members"
        self._topic_ask_active_members = "active_members"
        self._topic_delete_member = "delete_member"
        self._topic_edit_member = "change_member_data"


    @classmethod
    def hash_password(cls, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def get_current_username(self):
        if self.current_user:
            return self.current_user
        else:
            QMessageBox.information(None, "Error", "User not logged in")
            return None

# ------------------------------------------------------------------------------
    def login(self, username, password):
        try:
            if not username or not password:
                raise Exception("Username and password cannot be empty")

            hashed_password = self.hash_password(password)
            self._stored_password = hashed_password
            login_data = {
                "username": username,
                "password": hashed_password
            }
            login_json = json.dumps(login_data)
            self._mqtt_client.send_message(login_json, self._topic_ask_login)

        except Exception as e:
            raise e

    # ------------------------------------------------------------------------------

    def forgot_password(self):
        try:
            self._mqtt_client.send_message(ResetPassword.RESET, self._topic_ask_press_button)
        except Exception as e:
            raise e

    #------------------------------------------------------------------------------
    def register(self, username, password, repeat_password):
        try:
            if not username or not password:
                raise Exception("Username and password cannot be empty")

            if password != repeat_password:
                raise Exception("Passwords do not match")

            # if len(password) < 8:
            #     raise Exception("Password must be at least 8 characters")
            #
            # if not re.search(r'[A-Z]', password):
            #     raise Exception("Password must contain at least one uppercase letter")
            #
            # if "ndl" not in password:
            #     raise Exception("Password must contain the substring ndl")


            hashed_password = self.hash_password(password)

            register_data = {
                "username": username,
                "password": hashed_password,
            }

            register_json = json.dumps(register_data)

            self._mqtt_client.send_message(register_json, self._topic_ask_reg)

        except Exception as e:
            raise e

#------------------------------------------------------------------------------
    def create_new_member(self, member_name, member_surname, pictures):
        try:

            if len(pictures) != 6:
                raise Exception("Exactly 6 pictures required")

            member_data = {
                "Name": member_name,
                "Pictures": pictures,
                "Command": "create_member"
            }

            member_json = json.dumps(member_data)
            self._mqtt_client.send_message(member_json, self._topic_ask_new_member)

        except Exception as e:
            raise e


    #------------------------------------------------------------------------------

    def change_password(self, username, old_password, new_password):
        try:

            if self.hash_password(old_password) != self.get_stored_password():
                raise Exception("Old password is incorrect")

            # if len(new_password) < 8:
            #     raise Exception("Password should be at least 8 characters")
            #
            # if not re.search(r'[A-Z]', new_password):
            #     raise Exception("Password must contain at least one uppercase letter")
            #
            # if "ndl" not in new_password:
            #     raise Exception("Password must contain the substring ndl")

            hashed_new_password = self.hash_password(new_password)

            new_password_data = {
                "username": username,
                "password": hashed_new_password
            }

            new_password_json = json.dumps(new_password_data)

            self._mqtt_client.send_message(new_password_json, self._topic_ask_change_password)

        except Exception as e:
            raise e

    #------------------------------------------------------------------------------
    #TODO how?
    def lock_unlock(self, current_state):
        try:
            self.intended_state = current_state
            command = "lock" if current_state else "unlock"
            self._mqtt_client.send_message(json.dumps({"command": "lock_ask"}), self._topic_ask_lock_unlock)
        except Exception as e:
            raise e

    #------------------------------------------------------------------------------
    #TODO: how do I do it here?

    def active_members(self):
        try:
            self._mqtt_client.send_message("list_active", self._topic_ask_active_members)
        except Exception as e:
            raise e

    #------------------------------------------------------------------------------

    def all_members(self):
        try:
            self._mqtt_client.send_message("list_all", self._topic_ask_all_members)

        except Exception as e:
            raise e


    #------------------------------------------------------------------------------

    def delete_member(self, member_name):
        try:
            delete_data = {
                "name": member_name
            }

            delete_json = json.dumps(delete_data)

            self._mqtt_client.send_message(delete_json, self._topic_delete_member)

        except Exception as e:
            raise e


    #------------------------------------------------------------------------------

    @Slot(str, str, bool)
    def change_member(self, member_name, new_member_name, member_status):
        try:
          if new_member_name.strip():

            change_data = {
                "name": member_name,
                "new_member_name": new_member_name
            }

            change_json = json.dumps(change_data)
            self._mqtt_client.send_message(change_json, self._topic_edit_member)

          else:

              change_data = {
                  "name": member_name,
                  "member_status": member_status
              }

              change_json = json.dumps(change_data)
              self.member_name = member_name
              self.member_has_access = member_status

              self._mqtt_client.send_message(change_json, self._topic_edit_member)

        except Exception as e:
            raise e
    #------------------------------------------------------------------------------

    def new_member(self, name, surname, pictures):
        try:
            new_data = {
                "name": name,
                "surname": surname,
                "pictures": pictures
            }
            request = {"value": new_data, "session_token": token}

            new_json = json.dumps(request)

            self._mqtt_client.send_message(new_json, self._topic_ask_new_member)

        except Exception as e:
            raise e


