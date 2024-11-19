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
        self._topic_ask = "login_ask"

        # Subscribe to all relevant topics
        self.mqtt_client.response_listener("mqtt_responses_cached", self.handle_login_response)
        self.mqtt_client.response_listener("press_button_response", self.handle_press_button_response)
        self.mqtt_client.response_listener("register_response", self.handle_register_response)
        self.mqtt_client.response_listener("lock_response", self.handle_lock_response)
        self.mqtt_client.response_listener("active_users_response", self.handle_active_users_response)
        self.mqtt_client.response_listener("all_users_response", self.handle_all_users_response)
        self.mqtt_client.response_listener("delete_member_response", self.handle_delete_member_response)
        self.mqtt_client.response_listener("change_member_response", self.handle_change_member_response)
        self.mqtt_client.response_listener("change_member_status_response", self.handle_change_member_status_response)
        self.mqtt_client.response_listener("new_member_response", self.handle_new_member_response)

    @classmethod
    def hash_password(cls, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def get_stored_password(self):
        return self._stored_password_hash

    def get_current_username(self):
        if self.current_user:
            return self.current_user
        else:
            QMessageBox.information(None, "Error", "User not logged in")
            return None

# ------------------------------------------------------------------------------
    def login(self, username, password):
        # topic_response = "mqtt_responses_cached"
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
            self._mqtt_client.send_message(login_json, self._topic_ask)

        except Exception as e:
            raise e

    # ------------------------------------------------------------------------------

    def forgot_password(self):
        topic_ask = "press_button_ask"
        topic_response = "press_button_response"

        try:

            press_button_data = {
                "command": "press_button_ask"
            }

            press_button_json = json.dumps(press_button_data)
            self._mqtt_client.send_to_topic(topic_ask, press_button_json)

            QMessageBox.information(None, "Forgot Password", "Please press the button on the lock manually.")

        except Exception as e:
            raise e

        def on_press_button_response(client, userdata, msg):
            try:
                response = msg.payload.decode()

                if response == "ok":
                    self.ui_reference.stack.setCurrentWidget(self.ui_reference.defaultPasswordPage)
                else:
                    raise Exception("Please press the button again")

                self.mqtt_client.response_listener(topic_response, on_press_button_response)

            except Exception as e:
                raise e

        # ------------------------------------------------------------------------------
        # def default_login(self, username, password):
        #     topic_ask = "default_login_ask"
        #     topic_response = "default_login_response"
        #
        #     hashed_password = self.hash_password(password)
        #
        #     default_login_data = {
        #         "username": username,
        #         "password": hashed_password
        #     }
        #
        #     default_login_json = json.dumps(default_login_data)
        #
        #     self.mqtt_client.send_to_topic(topic_ask, default_login_json)
        #
        #     def on_default_login_response(client, userdata, msg):
        #         response = msg.payload.decode()
        #         if response == "ok":
        #             self.ui_reference.stack.setCurrentWidget(self.ui_reference.main_page)
        #         else:
        #             QMessageBox.information(None, "Default Login Failed", "Please try again")
        #
        #     self.mqtt_client.response_listener(topic_response, on_default_login_response)

    #------------------------------------------------------------------------------
    def register(self, username, password, repeat_password, pictures):
        topic_ask = "register_ask"
        topic_response = "register_response"

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

            self.mqtt_client.send_to_topic(topic_ask, register_json)

        except Exception as e:
            raise e


        def on_register_response(client, userdata, msg):
            try:
                response = msg.payload.decode()
                if response == "ok":
                    raise Exception("Registration successful")
                    self.ui_reference.stack.setCurrentWidget(self.ui_reference.main_page)
                else:
                    raise Exception("Registration failed, please try again")

                self.mqtt_client.response_listener(topic_response, on_register_response)

            except Exception as e:
                raise e

#------------------------------------------------------------------------------
    def create_new_member(self, member_name, pictures):

        topic_ask = "new_member_ask"
        topic_response = "new_member_response"

        try:

            if len(pictures) != 6:
                raise Exception("Exactly 6 pictures required")

            member_data = {
                "Name": member_name,
                "Pictures": pictures,
                "Command": "create_member"
            }

            member_json = json.dumps(member_data)
            self.mqtt_client.send_to_topic(topic_ask, member_json)

        except Exception as e:
            raise e

        def on_new_member_response(client, userdata, msg):
            response = msg.payload.decode()
            if response == "ok":
                QMessageBox.information(None, "Success", "New member was created")
                self.ui_reference.stack.setCurrentWidget(self.ui_reference.main_page)
            else:
                QMessageBox.information(None, "Error", "Failed to create new member")

        self.mqtt_client.response_listener(topic_response, on_new_member_response)

    #------------------------------------------------------------------------------

    def change_password(self, username, old_password, new_password):
        topic_ask = "change_password_ask"
        topic_response = "change_password_response"

        try:

            hashed_old_password = self.hash_password(old_password)

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

            self.mqtt_client.send_to_topic(topic_ask, new_password_json)

        except Exception as e:
            raise e

        def on_new_password_response(client, userdata, msg):
            response = msg.payload.decode()
            if response == "ok":
                QMessageBox.information(None, "Success", "The password was changed")
                self.ui_reference.stack.setCurrentWidget(self.ui_reference.main_page)
            else:
                QMessageBox.information(None, "Error", "Failed to change the password")

        self.mqtt_client.response_listener(topic_response, on_new_password_response)

    #------------------------------------------------------------------------------

    def lock_unlock(self, current_state):
        topic_ask = "lock_ask"
        topic_response = "lock_response"

        self.intended_state = current_state
        command = "lock" if current_state else "unlock"
        self.mqtt_client.send_to_topic(topic_ask, json.dumps({"command": "lock_ask"}))

        def on_lock_response(client, userdata, msg):
            response = msg.payload.decode()

            if response == "ok":
                self.door_locked = self.intended_state
                self.ui_reference.root_context.setContextProperty(
                    "doorSwitchChecked", self.door_locked
                )
            else:
                QMessageBox.information(None, "Error", "Failed to change the door status.")
                self.ui_reference.root_context.setContextProperty(
                    "doorSwitchChecked", not self.intended_state
                )

        self.mqtt_client.response_listener(topic_response, on_lock_response)


    #------------------------------------------------------------------------------

    def active_members(self):
        topic_ask = "active_members_ask"
        topic_response = "active_members_response"

        self.mqtt_client.send_to_topic(topic_ask, json.dumps({"command": "active_users_ask"}))

        def on_active_users_ask_response(client, userdata, msg):
            response = msg.payload.decode()
            if response == "ok":
                active_users = response.get("users", [])
                self.update_active_users_list(active_users)
            else:
                QMessageBox.information(None, "Error", "Active users list is empty")

        self.mqtt_client.response_listener(topic_response, on_active_users_ask_response)

        @Slot(list)
        def update_active_users_list(self, active_users):
            # Clear the existing model
            self.ui_reference.root_context.setContextProperty("activeUsersModel", [])

            # Add each user to the model
            for user in active_users:
                self.ui_reference.root_context.setContextProperty("activeUsersModel", {
                    "name": user["name"]
                })

    #------------------------------------------------------------------------------

    def all_members(self):
        topic_ask = "all_members_ask"
        topic_response = "all_members_response"

        self.mqtt_client.send_to_topic(topic_ask, json.dumps({"command": "all_members_ask"}))

        def on_all_members_ask_response(client, userdata, msg):
            response = msg.payload.decode()
            if response.get("status") == "ok":
                members = response.get("members", [])

                self.ui_reference.root_context.setContextProperty("membersModel", [])

                for member in members:
                    self.ui_reference.root_context.setContextProperty("membersModel", {
                        "name": member["name"],
                        "status": member["status"]
                    })
            else:
                QMessageBox.information(None, "Error", "Failed to retrieve members list")

            self.mqtt_client.response_listener(topic_response, on_all_members_ask_response)


    #------------------------------------------------------------------------------

    def delete_member(self, member_name):
        topic_ask = "delete_member_ask"
        topic_response = "delete_member_response"


        delete_data = {
            "name": member_name
        }

        delete_json = json.dumps(delete_data)

        self.mqtt_client.send_to_topic(topic_ask, delete_json)

        def on_delete_response(client, userdata, msg):
            response = msg.payload.decode()
            if response == "ok":
                QMessageBox.information(None, "Success", "The member has been deleted.")
                self.ui_reference.remove_member_from_list()
            else:
                QMessageBox.information(None, "Error", "Failed to delete the member")

        self.mqtt_client.response_listener(topic_response, on_delete_response)

    #------------------------------------------------------------------------------
    # I need to combine two functions below, so that if the string is empty we change the status,
    # and if the string is not empty we change the name

    @Slot(str, str, bool)
    def change_member(self, member_name, new_member_name, member_status):
      if new_member_name.strip():
        topic_ask = "change_member_ask"
        topic_response = "change_member_response"

        change_data = {
            "name": member_name,
            "new_member_name": new_member_name
        }

        change_json = json.dumps(change_data)
        self.mqtt_client.send_to_topic(topic_ask, change_json)

        def on_change_member_response(client, userdata, msg):
            response = msg.payload.decode()
            if response == "ok":
                QMessageBox.information(None, "Success", "The member has been changed.")
                self.ui_reference.update_member_name_in_list()
            else:
                QMessageBox.information(None, "Error", "The name was not changed.")

        self.mqtt_client.response_listener(topic_response, on_change_member_response)
      else:
          topic_ask = "change_member_status_ask"
          topic_response = "change_member_status_response"

          change_data = {
              "name": member_name,
              "member_status": member_status
          }

          change_json = json.dumps(change_data)
          self.member_name = member_name
          self.member_has_access = member_status

          self.mqtt_client.send_to_topic(topic_ask, change_json)

          def on_change_member_status_response(client, userdata, msg):
              response = msg.payload.decode()
              if response == "ok":
                  if self.member_has_access:
                      QMessageBox.information(None, "Success", "The member cannot unlock the door.")
                      self.ui_reference.update_member_status(self.member_name, False)
                  else:
                      QMessageBox.information(None, "Success", "The member now can unlock the door.")
                      self.ui_reference.update_member_status(self.member_name, True)
              else:
                  if self.member_has_access:
                      QMessageBox.information(None, "Error", "The member can still unlock the door.")
                  else:
                      QMessageBox.information(None, "Error", "The member still cannot unlock the door.")

          self.mqtt_client.response_listener(topic_response, on_change_member_status_response)

    #------------------------------------------------------------------------------

    def new_member(self, name, pictures):
        topic_ask = "new_member_ask"
        topic_response = "new_member_response"

        new_data = {
            "name": name,
            "pictures": pictures
        }

        new_json = json.dumps(new_data)

        self.mqtt_client.send_to_topic(topic_ask, new_json)

        def on_new_member_response(client, userdata, msg):
            response = msg.payload.decode()
            if response == "ok":
                QMessageBox.information(None, "Success", "The member has been created.")
                self.ui_reference.update_member_name_in_list()
            else:
                QMessageBox.information(None, "Error", "Failed to create the member")

        self.mqtt_client.response_listener(topic_response, on_new_member_response)

    #------------------------------------------------------------------------------

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
