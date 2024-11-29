import sys
import random
import csv
import time

from PySide6 import QtWidgets
from PySide6.QtCore import QObject, Slot

from mqtt import MQTTServer
from program_codes.login_response_codes import LoginResponseCodes
from PySide6 import QtCore, QtWidgets

from program_codes.new_member_response_codes import NewMemberResponseCodes
from program_codes.register_response_codes import RegisterResponseCodes
from UserCommands import UserCommands


class GuiBackend(QObject):
    def __init__(self, mqtt: MQTTServer):
        super().__init__()
        self._user_commands = UserCommands(mqtt)


    @Slot(str, str)
    def login(self, username, password):
        # call login from UserCommands
        try:
            self._user_commands.login(username, password)
        except Exception as e:
            print(f"Error initiating login: {str(e)}")
            return

        # sleep(5) "Please wait"
        # self.message_label.setText("Please wait:)")
        time.sleep(5)

        # check the login response using csv file and convert it to enum using string_to_enum
        try:
            with open("../mqtt_responses_cached/login_authorized.csv", "r") as file:
                response = file.read().strip()
                login_code = LoginResponseCodes.string_to_enum(response)

                if login_code == LoginResponseCodes.OK:
                    print("Login successful!")
                    # self.stack_view.push("mainPage")
                elif login_code == LoginResponseCodes.FAILED:
                    print("Login failed!")
                else:
                    print("Please try again!")


        except Exception as e:
            raise e


    def register(self):
        # read the input fields
        username = self.registerUsernameField.text()
        password = self.registerPasswordField.text()
        repeat_password = self.repeatPasswordField.text()

        # call register from UserCommands
        try:
            self._user_commands.register(username, password, repeat_password)
        except Exception as e:
            self.message_label.setText(f"Error initiating register: {str(e)}")
            return

        # sleep(5) "Please wait"
        self.message_label.setText("Please wait:)")
        time.sleep(5)

        # check the register response using csv file and convert it to enum using string_to_enum
        try:
            with open("../mqtt_responses_cached/register_authorized.csv", "r") as file:
                response = file.read().strip()
                register_code = RegisterResponseCodes.string_to_enum(response)

                if register_code == RegisterResponseCodes.OK:
                    self.message_label.setText("Register successful!")
                    self.stack_view.push("mainPage")
                elif register_code == RegisterResponseCodes.FAILED:
                    self.message_label.setText("Register failed!")
                else:
                    self.message_label.setText("Please try again")

        except Exception as e:
            raise e


    def forgot_password(self):
        pass

    def new_member(self):
        name = self.newUsernameField.text()
        pics = self.picturesArray

        try:
            self.new_member(name, pics)
        except Exception as e:
            self.message_label.setText(f"Error creating a new member")
            return

        self.message_label.setText("Please wait:)")
        time.sleep(5)

        try:
            with open("../mqtt_responses_cached/new_member_authorized.csv", "r") as file:
                response = file.read().strip()
                new_member_code = NewMemberResponseCodes.string_to_enum(response)

                if new_member_code == NewMemberResponseCodes.OK:
                    self.message_label.setText("New member was created!")
                    # I need to update the list here???
                elif new_member_code == NewMemberResponseCodes.FAILED:
                    self.message_label.setText("Failed to create a new member")
                else:
                    self.message_label.setText("Please try again")

        except Exception as e:
            raise e


    def edit_member(self):
        pass

    def delete_member(self):
        pass

    def list_all_members(self):
        pass

    def list_active_members(self):
        pass
    # TODO: to check the functions