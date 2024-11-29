import sys
import random
import csv
import time

from PySide6 import QtWidgets
from program_codes.login_response_codes import LoginResponseCodes
from PySide6 import QtCore, QtWidgets



class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # self.stack_view = stack_view
        # self.user_commands = user_commands
        self.username_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.message_label = QtWidgets.QLabel()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(QtWidgets.QLabel("Username"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(QtWidgets.QLabel("Password"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.message_label)

    def login(self):
        # read the input fields
        username = self.usernameField.text()
        password = self.passwordField.text()

        # call login from UserCommands
        try:
            self.login(username, password)
        except Exception as e:
            self.message_label.setText(f"Error initiating login: {str(e)}")
            return

        # sleep(5) "Please wait"
        self.message_label.setText("Please wait:)")
        time.sleep(5)

        # check the login response using csv file and convert it to enum using string_to_enum
        try:
            with open("../mqtt_responses_cached/login_authorized.csv", "r") as file:
                response = file.read().strip()
                login_code = LoginResponseCodes.string_to_enum(response)

                if login_code == LoginResponseCodes.OK:
                    self.message_label.setText("Login successful!")
                    self.stack_view.push("mainPage")
                elif login_code == LoginResponseCodes.FAILED:
                    self.message_label.setText("Login failed!")
                else:
                    self.message_label.setText("Please try again")

        except Exception as e:
            raise e

    def register(self):
        # read the input fields
        username = self.registerUsernameField.text()
        password = self.registerPasswordField.text()
        repeat_password = self.repeatPasswordField.text()

        # call register from UserCommands
        try:
            self.register(username, password, repeat_password)
        except Exception as e:
            self.message_label.setText(f"Error initiating register: {str(e)}")
            return

        # sleep(5) "Please wait"
        self.message_label.setText("Please wait:)")
        time.sleep(5)

        # check the login response using csv file and convert it to enum using string_to_enum



    def forgot_password(self):
        pass

    def new_member(self):
        pass

    def edit_member(self):
        pass

    def delete_member(self):
        pass

    def list_all_members(self):
        pass

    def list_active_members(self):
        pass
    # TODO: to check the functions