import json

import cv2
from PySide6.QtCore import Slot
from shiboken6.Shiboken import delete

from mqtt import MQTTServer
import hashlib
import re
from PySide6.QtWidgets import QMessageBox

class UserCommands:
    def __init__(self, mqtt_client: MQTTServer, ui_reference):
        self._mqtt_client = mqtt_client
        self._ui_reference = ui_reference
        self._current_user = None
        self._stored_password = None
        # main mqtt topics
        self._topic_ask_login = "login_ask"
        self._topic_ask_reg = "register_ask"
        self._topic_ask_press_button = "press_button_ask"
        self._topic_ask_new_member = "new_member_ask"
        self._topic_ask_change_password = "change_password_ask"
        self._topic_ask_lock_unlock = "lock_unlock_ask"
        self._topic_ask_all_members = "all_members_ask"
        self._topic_ask_active_members = "active_members_ask"
        self._topic_delete_member = "delete_member_ask"


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
    #TODO: do I need to json the command or can I just send it?

    def forgot_password(self):
        try:
            press_button_data = {
                "command": "press_button_ask"
            }
            press_button_json = json.dumps(press_button_data)
            self._mqtt_client.send_message(press_button_json, self._topic_ask_press_button)

        except Exception as e:
            raise e

    #------------------------------------------------------------------------------
    def register(self, username, password, repeat_password, pictures):
        try:
            if password == repeat_password:
                raise Exception("Passwords do not match")

            if len(password) < 8:
                raise Exception("Password must be at least 8 characters")

            if not re.search(r'[A-Z]', password):
                raise Exception("Password must contain at least one uppercase letter")

            if "ndl" not in password:
                raise Exception("Password must contain the substring ndl")


            if len(pictures) != 6:
                raise Exception("Pictures must contain 6 images")

            hashed_password = self.hash_password(password)

            register_data = {
                "username": username,
                "password": hashed_password,
                "pictures": pictures
            }

            register_json = json.dumps(register_data)

            self._mqtt_client.send_message(register_json, self._topic_ask_reg)

        except Exception as e:
            raise e


#------------------------------------------------------------------------------
    def create_new_member(self, member_name, pictures):
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

            if len(new_password) < 8:
                raise Exception("Password should be at least 8 characters")

            if not re.search(r'[A-Z]', new_password):
                raise Exception("Password must contain at least one uppercase letter")

            if "ndl" not in new_password:
                raise Exception("Password must contain the substring ndl")


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
    #TODO: should I do the same for forgor password?

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
            self._mqtt_client.send_message(json.dumps({"command": "active_users_ask"}), self._topic_ask_active_members)
        except Exception as e:
            raise e

    #------------------------------------------------------------------------------

    def all_members(self):
        try:
            self._mqtt_client.send_message(json.dumps({"command": "all_members_ask"}), self._topic_ask_all_members)

        except Exception as e:
            raise e


        # def on_all_members_ask_response(client, userdata, msg):
        #     response = msg.payload.decode()
        #     if response.get("status") == "ok":
        #         members = response.get("members", [])
        #
        #         self.ui_reference.root_context.setContextProperty("membersModel", [])
        #
        #         for member in members:
        #             self.ui_reference.root_context.setContextProperty("membersModel", {
        #                 "name": member["name"],
        #                 "status": member["status"]
        #             })
        #     else:
        #         QMessageBox.information(None, "Error", "Failed to retrieve members list")
        #
        #     self.mqtt_client.response_listener(topic_response, on_all_members_ask_response)


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
    # I need to combine two functions below, so that if the string is empty we change the status,
    # and if the string is not empty we change the name

    @Slot(str, str, bool)
    def change_member(self, member_name, new_member_name, member_status):
      if new_member_name.strip():
        topic_ask = "change_member_ask"

        change_data = {
            "name": member_name,
            "new_member_name": new_member_name
        }

        change_json = json.dumps(change_data)
        self.mqtt_client.send_to_topic(topic_ask, change_json)


      else:
          topic_ask = "change_member_status_ask"

          change_data = {
              "name": member_name,
              "member_status": member_status
          }

          change_json = json.dumps(change_data)
          self.member_name = member_name
          self.member_has_access = member_status

          self.mqtt_client.send_to_topic(topic_ask, change_json)


    #------------------------------------------------------------------------------

    def new_member(self, name, pictures):
        try:
            new_data = {
                "name": name,
                "pictures": pictures
            }

            new_json = json.dumps(new_data)

            self._mqtt_client.send_message(new_json, self._topic_ask_new_member)

        except Exception as e:
            raise e


    #------------------------------------------------------------------------------
    # TODO: I am not sure I need this
    def open_camera_and_take_pictures(self):
        pictures = []
        cap = cv2.VideoCapture(0)

        for i in range(6):
            ret, frame = cap.read()
            if ret:
                file_path = f"/path/to/save/picture_{i}.jpg"
                cv2.imwrite(file_path, frame)
                pictures.append(file_path)
            cv2.waitKey(1000)  # Wait 1 second between captures

        cap.release()
        cv2.destroyAllWindows()
        return pictures
