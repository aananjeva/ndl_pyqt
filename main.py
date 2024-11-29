import json
import sys

import gui
import mqtt as mqtt
from PySide6.QtWidgets import QMessageBox, QApplication, QWidget
from PySide6 import QtWidgets
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from UserCommands import UserCommands
from data_operations import data
from data_operations.data import FileTransfer
from mqtt import MQTTServer
from gui import GuiBackend

class SmartLockSystem:
    BROKER_ADDRESS = "localhost"  # Change this to your broker address
    LOGIN_TOPIC = "smartlock/login"
    REGISTER_TOPIC = "smartlock/register"
    STATUS_TOPIC = "smartlock/status"

    def __init__(self):
        self.client = mqtt.MQTTServer()
        self.client.run()
        self.user_commands = UserCommands(self.client)


# ---------------------------------------------------------------------
    # Functions for buttons

    def on_login_button_click(self, username, password):
        self.user_commands.login(username, password)

    def on_default_login_button_click(self, username, password):
        UserCommands.default_login(username, password)

    def on_registration_button_click(username, password, repeat_password, pictures):
        if password != repeat_password:
            QMessageBox.information(None, "Error", "Passwords do not match")
            return

        UserCommands.register(username, password, repeat_password, pictures)

    def on_forgot_password_button_click(self):
        UserCommands.forgot_password(self)

    def on_lock_unlock_button_click(self, current_state):
        if current_state:
            print("Locking the door...")
        else:
            print("Unlocking the door...")

        self.lock_unlock(current_state)

    def on_change_password_button_click(self, current_password, new_password, repeat_new_password):
        if repeat_new_password != new_password:
            QMessageBox.information(None, "Error", "Passwords do not match")
            return

        username = self.get_current_username()  # Retrieve the current username
        # Call the change_password method with all the required parameters
        UserCommands.change_password(username, current_password, new_password)

    def on_create_member_button_click(self, username, pictures):
        UserCommands.new_member(username, pictures)

if __name__ == "__main__":
    # smart_lock_system = SmartLockSystem()
    # try:
    #     while True:
    #         pass
    # except KeyboardInterrupt:
    #     print("Exiting...")
    #     smart_lock_system.client.loop_stop()


    # ---------------------------------------------------------------------------------------------------

    # trying to run the app
    # Create the QApplication instance
    # Initialize the MQTT server
    mqtt_server = MQTTServer()
    mqtt_server.run()  # Start the MQTT server
    # Initialize UserCommands with the MQTT server
    gui = GuiBackend(mqtt_server)
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    engine.rootContext().setContextProperty("python", gui)  # Expose `MyWidget` to QML
    engine.loadFromModule("Main", "Main")
    # engine.load("/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/Main/Main.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()

    del engine
    sys.exit(exit_code)


    # ---------------------------------------------------------------------------------------------------

    #test for login
    # mqtt = MQTTServer()
    # mqtt.run()
    # user_data = {"username":"root", "password":"1a6719fc847f299114cc00a430549c272fa8cab7aa8ae3e55d9c6f84c62ba102"}
    # mqtt.send_message(json.dumps(user_data), "login")

    # ---------------------------------------------------------------------------------------------------

    # #test for file transfer
    # file_tr = FileTransfer(name="test", surname="test2", file_path="/Users/anastasiaananyeva/Downloads/pics/austin-curtis-YVY61lIO_gw-unsplash.jpg")
    # value = file_tr.file_transfer()
    # if value:
    #     print(value)




