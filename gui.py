import csv
import json
import os
import re
import time
from lib2to3.fixes.fix_input import context
from shutil import move

import cv2
from PySide6.QtCore import QObject, Slot, QAbstractListModel, QModelIndex, Qt, Property
from PySide6.QtMultimedia import QMediaCaptureSession, QImageCapture
from PySide6.QtWidgets import QMessageBox
from data_operations.data import FileTransfer
from mqtt import MQTTServer
from program_codes.login_response_codes import LoginResponseCodes
from PySide6.QtMultimedia import QCamera
from program_codes.register_response_codes import RegisterResponseCodes
from program_codes.general_commands_response_codes import ResponseCodes
from UserCommands import UserCommands
from PySide6.QtCore import Signal
from datetime import datetime
from loguru import logger


class MembersModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    StatusRole = Qt.UserRole + 2
    AccessRemaining = Qt.UserRole + 3

    def __init__(self, members=None):
        super().__init__()
        self._members = members or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._members)

    def add_member(self, member):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._members.append(member)
        self.endInsertRows()

    # def update_members(self, members):
    #     self.beginResetModel()
    #     self._members = members
    #     self.endResetModel()

    def data(self, index, role):
        if not index.isValid() or index.row() >= len(self._members):
            return None

        member = self._members[index.row()]
        if role == self.NameRole:
            return member.get("name")
        if role == self.StatusRole:
            return member.get("status")
        if role == self.AccessRemainingRole:
            return member.get("access_remaining")
        return None

    def roleNames(self):
        return {
            self.NameRole: b"name",
            self.StatusRole: b"status",
            self.AccessRemainingRole: b"access_remaining",
        }

class GuiBackend(QObject):
    #signals:
    pictureCountChanged = Signal()
    onLoginSuccess = Signal()
    onRegisterSuccess = Signal()
    membersUpdated = Signal(list)
    activeMembersUpdated = Signal(list)
    notificationSignal = Signal(str)
    usernameSignal = Signal(str)
    members = []
    picture_path_server = ""


    def trigger_notification(self, message):
        self.notificationSignal.emit(message)

    def __init__(self, mqtt: MQTTServer):
        super().__init__()
        self._user_commands = UserCommands(mqtt)
        self._picture_count = 0
        self.pictures_dir = "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/images"

        if not os.path.exists(self.pictures_dir):
            os.makedirs(self.pictures_dir)

        # Camera setup
        self.camera = QCamera()
        self.capture_session = QMediaCaptureSession()
        self.image_capture = QImageCapture(self.camera)

        # Configure capture session
        self.capture_session.setCamera(self.camera)
        self.capture_session.setImageCapture(self.image_capture)

    @Slot(str, str)
    def login_button(self, username, password):
        # call login from UserCommands
        try:
            if not username or not password:
                self.trigger_notification("Please enter your username and password")
            with open("mqtt_responses_cached/login_authorized.csv", "w") as file:
                file.write("")
            self._user_commands.login(username, password)
        except Exception as e:
            logger.debug(f"Error initiating login: {str(e)}")
            return

        # sleep(3) "Please wait"
        # self.show_notification(self, "Please wait :)")
        time.sleep(3)

        # check the login response using csv file and convert it to enum using string_to_enum
        try:
            with open("mqtt_responses_cached/login_authorized.csv", "r") as file:
                response = file.read().strip()

            try:
                login_code = LoginResponseCodes.string_to_enum(response)
            except Exception:
                login_code = LoginResponseCodes.FAILED

            match login_code:
                case LoginResponseCodes.OK:
                    logger.debug("Login successful")
                    self.trigger_notification("Login successful!")
                    self.onLoginSuccess.emit()
                case LoginResponseCodes.FAILED:
                    logger.debug("Login failed")
                    self.trigger_notification("Login failed!")
                case _:
                    logger.debug("Please try again")
                    self.trigger_notification("Please try again!")


        except Exception as e:
            logger.debug(f"Error reading login response: {str(e)}")

    @Slot(str, str, str)
    def register_button(self, username, password, repeat_password):
        try:
            if not username or not password or not repeat_password:
                self.trigger_notification("Please enter your username and password")
            if password != repeat_password:
                self.trigger_notification("Passwords do not match")

            if len(password) < 8:
                self.trigger_notification("Password must be at least 8 characters")
            if not re.search(r'[A-Z]', password):
                self.trigger_notification("Password must contain at least one uppercase letter")
            if "ndl" not in password:
                self.trigger_notification("Password must contain the substring ndl")

            with open("mqtt_responses_cached/register_authorized.csv", "w") as file:
                file.write("")
            self._user_commands.register(username, password, repeat_password)
        except Exception as e:
            logger.debug(f"Error initiating register: {str(e)}")
            return

        # sleep(3) "Please wait"
        # self.show_notification(self, "Please wait :)")
        time.sleep(3)

        # check the register response using csv file and convert it to enum using string_to_enum
        try:
            with open("mqtt_responses_cached/register_authorized.csv", "r") as file:
                response = file.read().strip()
            try:
                register_code = RegisterResponseCodes.string_to_enum(response)
            except Exception:
                register_code = RegisterResponseCodes.FAILED

            match register_code:
                case RegisterResponseCodes.OK:
                    logger.debug("Registration successful")
                    self.trigger_notification("Registration successful!")
                    self.onLoginSuccess.emit()
                case RegisterResponseCodes.FAILED:
                    logger.debug("Registration failed")
                    self.trigger_notification("Registration failed!")
                case _:
                    logger.debug("Please try again")
                    self.trigger_notification("Please try again!")


        except Exception as e:
            raise e

    @Slot()
    def forgot_password_button(self, msg):
        try:
            with open("mqtt_responses_cached/general_commands_authorized.csv", "w") as file:
                file.write("")
            self._user_commands.forgot_password()
        except Exception as e:
            logger.debug("Please press the button again")

        try:
            response = msg.payload.decode()
            if response.lower() == "ok":
                self._user_commands.forgot_password()
            else:
                logger.debug("Please press the button again")
        except Exception as e:
            raise e

    @Slot()
    def list_all_members_gui(self):
        members = []
        try:
            try:
                with open("mqtt_responses_cached/list_all_members_authorized.csv", "w") as file:
                    file.write("")
                self._user_commands.all_members()
            except Exception as e:
                logger.debug(f"Error reading all members: {str(e)}")
            time.sleep(2)
            csv_file = "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/mqtt_responses_cached/list_all_members_authorized.csv"

            with open(csv_file, "r") as file:
                members = json.load(file)
            logger.debug(f"List all members: {members}")

        except Exception as e:
            logger.debug(f"Error reading csv file: {str(e)}")
            members = []

        self.membersUpdated.emit(members)

    @Slot()
    def list_active_members_gui(self):
        members = []
        try:
            try:
                with open("mqtt_responses_cached/list_active_members_authorized.csv", "w") as file:
                    file.write("")
                self._user_commands.active_members()
            except Exception as e:
                logger.debug(f"Error reading active members: {str(e)}")

            time.sleep(5)
            csv_file = "mqtt_responses_cached/list_active_members_authorized.csv"

            with open(csv_file, "r") as file:
                # Read the content
                content = file.read().strip()

                if not content:
                    raise Exception("File is empty or contains only whitespace.")

                # Parse the JSON
                try:
                    data = json.loads(content)
                    # Handle both single object and array cases
                    if isinstance(data, dict):  # Single active member
                        members = [data]  # Wrap in a list
                    elif isinstance(data, list):  # Multiple active members
                        members = data
                    else:
                        raise Exception("Unexpected JSON format.")
                except json.JSONDecodeError as e:
                    raise Exception(f"Invalid JSON format: {str(e)}")

            logger.debug(f"List active members: {members}")

        except json.JSONDecodeError as e:
            logger.debug(f"Error decoding JSON: {str(e)}")
        except Exception as e:
            logger.debug(f"Error reading CSV file: {str(e)}")

        # Emit the list of active members
        self.activeMembersUpdated.emit(members)

    @Slot(str, str, str)
    def change_password_button(self, current_password, new_password, repeat_password):
        try:
            real_password = self._user_commands.get_current_password()
            hash_current_password = self._user_commands.hash_password(current_password)
            if real_password != hash_current_password:
                logger.debug("The entered password is wrong")
                self.trigger_notification("The entered password is wrong!")

            if new_password != repeat_password:
                logger.debug("Passwords do not match")
                self.trigger_notification("Passwords do not match!")

        except Exception as e:
            logger.debug(f"Error changing password: {e}")

        try:
            try:
                with open("mqtt_responses_cached/general_commands_authorized.csv", "w") as file:
                    file.write("")
            except Exception as e:
                logger.debug(f"Error editing the file: {str(e)}")
            self._user_commands.change_password(new_password)
            with open("mqtt_responses_cached/general_commands_authorized.csv", "r") as file:
                response = file.read().strip()
            try:
                change_password_response = ResponseCodes.string_to_enum(response)
            except Exception:
                change_password_response = ResponseCodes.FAILED

            match change_password_response:
                case ResponseCodes.OK:
                    logger.debug("Password has been changed")
                    self.trigger_notification("Password has been changed")
                    self.onLoginSuccess.emit()
                case ResponseCodes.FAILED:
                    logger.debug("Failed to change password")
                    self.trigger_notification("Failed to change password")
                case _:
                    logger.debug("Please try again")
                    self.trigger_notification("Please try again!")


        except Exception as e:
            raise e

    @Slot(int, int, int, int, int)
    def get_date_button(self, year, month, day, hour, minute):
        try:
            my_date = f"{year}-{month}-{day} {hour}:{minute}:00"
            time_format = "%Y-%m-%d %H:%M:%S"
            timestamp = datetime.strptime(my_date, time_format)
            with open("date/selected_datetime.txt", "w") as file:
                file.write(timestamp.strftime("%Y-%m-%d %H:%M:%S"))

            logger.debug(f"Date and Time saved: {timestamp}")
        except ValueError as e:
            logger.debug(f"Error creating datetime: {e}")

    #Function for handling members
    @Slot(str, str)
    def new_member_button(self, name, status):
        # picture_path_server = "/home/ubuntu/images/member@_two" # make it dynamic
        pictures_dir = "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/images"
        try:
            pictures = [
                os.path.join(pictures_dir, f)
                for f in os.listdir(pictures_dir)
                if os.path.isfile(os.path.join(pictures_dir, f)) and f.endswith((".jpg", ".png"))
            ]

            if len(pictures) != 6:
                logger.debug("Exactly 6 pictures are required")

            name_trimmed = name.strip().split(" ")
            values = [x for x in name_trimmed if x]
            name = values[0] if len(values) >= 1 else ""
            surname = values[1] if len(values) >= 2 else ""
            self.picture_path_server = f"/home/ubuntu/images/{name}_{surname}"

            try:
                file_transfer = FileTransfer(name, surname, pictures_dir)
                file_transfer.file_transfer()
            except Exception as e:
                raise Exception(e)


        except Exception as e:
            logger.debug(f"Error creating new member: {e}")

        try:
            try:
                with open("mqtt_responses_cached/general_commands_authorized.csv", "w") as file:
                    file.write("")
            except Exception as e:
                logger.debug(f"Error editing the file: {str(e)}")
            self._user_commands.create_new_member(name, pictures_dir, self.picture_path_server, status)
            time.sleep(1)
            self.clear_pictures_directory()

            with open(f"mqtt_responses_cached/general_commands_authorized.csv", "r") as file:
                response = file.read().strip()
            try:
                new_member_code = ResponseCodes.string_to_enum(response)
            except Exception:
                new_member_code = ResponseCodes.FAILED

            match new_member_code:
                case ResponseCodes.OK:
                    logger.debug("New member was created")
                case ResponseCodes.FAILED:
                    logger.debug("Failed to create new member")
                case _:
                    logger.debug("Please try again")

        except Exception as e:
            raise e

    @Slot(str, str)
    def edit_member_button(self, name, new_status):
        try:
            try:
                with open("mqtt_responses_cached/general_commands_authorized.csv", "w") as file:
                    file.write("")
            except Exception as e:
                logger.debug(f"Error editing the file: {str(e)}")
            self._user_commands.change_member(name, new_status)
            with open(f"mqtt_responses_cached/general_commands_authorized.csv", "r") as file:
                response = file.read().strip()
            try:
                edit_member_code = ResponseCodes.string_to_enum(response)
            except Exception:
                edit_member_code = ResponseCodes.FAILED

            match edit_member_code:
                case ResponseCodes.OK:
                    logger.debug("Member was edited")
                case ResponseCodes.FAILED:
                    logger.debug("Failed to edit member")
                case _:
                    logger.debug("Please try again")


        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")

    @Slot(str)
    def delete_member_button(self, id):
        try:
            with open("mqtt_responses_cached/general_commands_authorized.csv", "w") as file:
                file.write("")
            self._user_commands.delete_member(id)
            with open(f"mqtt_responses_cached/general_commands_authorized.csv", "r") as file:
                response = file.read().strip()
            try:
                delete_member_code = ResponseCodes.string_to_enum(response)
            except Exception:
                delete_member_code = ResponseCodes.FAILED

            match delete_member_code:
                case ResponseCodes.OK:
                    logger.debug("Member was deleted")
                case ResponseCodes.FAILED:
                    logger.debug("Failed to delete member")
                case _:
                    logger.debug("Please try again")

        except Exception as e:
            logger.debug(f"Error editing the file: {str(e)}")


    #Helper functions
    @Slot()
    def take_picture(self):
        try:
            cap = cv2.VideoCapture(0)  # Open the default camera
            if not cap.isOpened():
                logger.debug("Error: Cannot access the camera.")
                return

            logger.debug("Camera opened. Press 'c' to capture a picture or 'q' to quit.")

            while True:
                ret, frame = cap.read()
                if not ret:
                    logger.debug("Failed to capture frame.")
                    break

                # Display the camera feed
                cv2.imshow("Camera Feed", frame)

                # Wait for a key press
                key = cv2.waitKey(1) & 0xFF

                # If 'c' is pressed, capture a picture
                if key == ord('c'):
                    pictures = [
                        f for f in os.listdir(self.pictures_dir) if f.endswith(".jpg")
                    ]

                    if len(pictures) < 6:
                        file_path = os.path.join(self.pictures_dir, f"picture_{len(pictures) + 1}.jpg")
                        cv2.imwrite(file_path, frame)
                        self._picture_count = len(pictures) + 1
                        self.pictureCountChanged.emit()  # Notify QML of the updated count
                        logger.debug(f"Picture saved to {file_path}")
                    else:
                        logger.debug("6 pictures already taken.")
                        break

                # If 'q' is pressed, quit the camera
                elif key == ord('q'):
                    logger.debug("Exiting camera feed.")
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

    # @Slot()
    # def check_completion(self):
    #     if self.picture_count < 6:
    #         logger.debug(f"Only {self.picture_count}/6 pictures taken.")
    #     else:
    #         logger.debug("All 6 pictures have been taken.")

    @Property(int, notify=pictureCountChanged)
    def pictureCount(self):
        return self._picture_count

    @Slot()
    def clear_pictures_directory(self):
        try:
            for file in os.listdir(self.pictures_dir):
                file_path = os.path.join(self.pictures_dir, file)
                if os.path.isfile(file_path) and file.endswith(".jpg"):
                    os.remove(file_path)
            self._picture_count = 0
            self.pictureCountChanged.emit()  # Notify QML of the reset
            logger.debug("All pictures have been removed from the directory.")
        except Exception as e:
            logger.error(f"Error clearing pictures directory: {e}")

    @Slot()
    def move_pictures_to_app_folder(self):
        pictures = [
            f for f in os.listdir(self.default_camera_dir)
            if f.endswith((".jpg", ".png")) and not f.startswith(".")
        ]
        pictures = sorted(pictures, key=lambda x: os.path.getctime(os.path.join(self.default_camera_dir, x)))

        for i, picture in enumerate(pictures[:6]):  # Only take the latest 6 pictures
            source_path = os.path.join(self.default_camera_dir, picture)
            target_path = os.path.join(self.pictures_dir, f"picture_{i + 1}.jpg")
            move(source_path, target_path)
            logger.debug(f"Moved: {source_path} -> {target_path}")

        self._picture_count = len(pictures[:6])
        if self._picture_count < 6:
            QMessageBox.warning(None, "Incomplete", f"Only {self._picture_count}/6 pictures were found.")
        else:
            QMessageBox.information(None, "Success", "All 6 pictures have been moved to the app folder!")

    @Slot()
    def check_picture_completion(self):
        pictures = [
            f for f in os.listdir(self.pictures_dir) if f.endswith((".jpg", ".png")) and not f.startswith(".")
        ]
        if len(pictures) < 6:
            QMessageBox.warning(None, "Incomplete", f"You only have {len(pictures)}/6 pictures. Please take more!")
        else:
            QMessageBox.information(None, "Complete", "You have taken all 6 pictures!")

