import json
import mqtt as mqtt
from PySide6.QtWidgets import QMessageBox

from UserCommands import UserCommands
from data_operations import data
from data_operations.data import FileTransfer
from mqtt import MQTTServer


class SmartLockSystem:
    BROKER_ADDRESS = "localhost"  # Change this to your broker address
    LOGIN_TOPIC = "smartlock/login"
    REGISTER_TOPIC = "smartlock/register"
    STATUS_TOPIC = "smartlock/status"

    def __init__(self):
        self.client = mqtt.MQTTServer()
        self.client.run()
        self.user_commands = UserCommands(self.client)

#---------------------------------------------------------------------
# Handle functions to process incoming requests, perform specific actions
# and send appropriate responses back to the system

    def handle_lock(self, payload):
        try:
            lock_data = json.loads(payload)
            command = lock_data.get("Command")

            if command == "lock":
                self.lock_door()  # Implement this method to lock the door
                response = {"status": "success", "message": "Door locked"}
            elif command == "unlock":
                self.unlock_door()  # Implement this method to unlock the door
                response = {"status": "success", "message": "Door unlocked"}
            else:
                response = {"status": "failure", "message": "Invalid command"}

                # Publish the response to the status topic
            self.client.publish(self.STATUS_TOPIC, json.dumps(response))

        except Exception as e:
            print(f"Error handling lock command: {e}")

    def handle_status_update(self, payload):
        try:
            # Implement your logic to gather the current status of the system
            status = self.get_system_status()  # This method should return the system status
            response = {"status": "success", "system_status": status}

            # Publish the response to the status topic
            self.client.publish(self.STATUS_TOPIC, json.dumps(response))
        except Exception as e:
            print(f"Error handling status update: {e}")

    def handle_user_update(self, payload):
        try:
            user_data = json.loads(payload)
            username = user_data.get("Username")
            new_username = user_data.get("NewUsername")

            # Implement your logic to update user information
            if self.update_user(username, new_username):
                response = {"status": "success", "message": "User updated successfully"}
            else:
                response = {"status": "failure", "message": "Failed to update user"}

            # Publish the response to the status topic
            self.client.publish(self.STATUS_TOPIC, json.dumps(response))
        except Exception as e:
            print(f"Error handling user update: {e}")


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
    #
    mqtt = MQTTServer()
    mqtt.run()
    user_data = {"username":"root", "password":"1a6719fc847f299114cc00a430549c272fa8cab7aa8ae3e55d9c6f84c62ba102"}
    mqtt.send_message(json.dumps(user_data), "login")


    # #test for file transfer
    # file_tr = FileTransfer(name="test", surname="test2", file_path="/Users/anastasiaananyeva/Downloads/pics/austin-curtis-YVY61lIO_gw-unsplash.jpg")
    # value = file_tr.file_transfer()
    # if value:
    #     print(value)

    #test for login data



