import json
import os
import re
import time
from shutil import move

import cv2
from PySide6.QtCore import QObject, Slot, QAbstractListModel, QModelIndex, Qt, Property
from PySide6.QtMultimedia import QMediaCaptureSession, QImageCapture
from PySide6.QtWidgets import QMessageBox
from data_operations.data import FileTransfer
from mqtt import MQTTServer
from program_codes.login_response_codes import LoginResponseCodes
from PySide6.QtMultimedia import QCamera

from program_codes.magnetic_lock_response_codes import MagneticLockResponseCodes
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

'''
This class takes user inputs from the Main.qnl and uses functions from UserCommands class
where the message is being send to the server via mqtt
'''

class GuiBackend(QObject):
    """The signals that are send to the app interface"""
    pictureCountChanged = Signal()
    loginSuccess = Signal()
    registerSuccess = Signal()
    membersUpdated = Signal(list)
    activeMembersUpdated = Signal(list)
    notificationSignal = Signal(str)
    magneticLockSignal = Signal(bool)
    defaultLoginSuccess = Signal()
    newMemberSignal = Signal()
    editMemberSignal = Signal()
    deleteMemberSignal = Signal()
    changePasswordSignal = Signal()
    saveDateSignal = Signal()

    members = []  #the array to keep the members
    picture_path_server = "" #the path to the face pictures of a member

    def __init__(self, mqtt: MQTTServer):
        super().__init__()
        self._mqtt = mqtt
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

    '''Function that triggers notifications'''
    def trigger_notification(self, message):
        self.notificationSignal.emit(message)


    '''Main functions'''
    '''Login function'''
    @Slot(str, str)
    def login_button(self, username, password):
        try:
            if not username or not password:
                self.trigger_notification("Please enter your username and password")
            with open("mqtt_responses_cached/login_authorized.csv", "w") as file:
                file.write("")
            self._user_commands.login(username, password)
        except Exception as e:
            logger.debug(f"Error initiating login: {str(e)}")
            return

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
                    self.loginSuccess.emit()
                case LoginResponseCodes.FAILED:
                    logger.debug("Login failed")
                    self.trigger_notification("Login failed!")
                case _:
                    logger.debug("Please try again")
                    self.trigger_notification("Please try again!")

        except Exception as e:
            logger.debug(f"Error reading login response: {str(e)}")

    '''Register function'''
    @Slot(str, str, str)
    def register_button(self, username, password, repeat_password):
        if not username or not password or not repeat_password:
            self.trigger_notification("Please enter your username and password")
        elif password != repeat_password:
            logger.debug("Passwords do not match")
            self.trigger_notification("Passwords do not match")

        elif len(password) < 8:
            self.trigger_notification("Password must be at least 8 characters")
            logger.debug("Password must be at least 8 characters")
        elif not re.search(r'[A-Z]', password):
            self.trigger_notification("Password must contain at least one uppercase letter")
            logger.debug("Password must contain at least one uppercase letter")
        elif "ndl" not in password:
            self.trigger_notification("Password must contain the substring ndl")
            logger.debug("Password must contain the substring ndl")

        with open("mqtt_responses_cached/register_authorized.csv", "w") as file:
            file.write("")
        self._user_commands.register(username, password, repeat_password)


        self.trigger_notification("Please wait :)")
        time.sleep(3)

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
                    self.registerSuccess.emit()
                case RegisterResponseCodes.FAILED:
                    logger.debug("Registration failed")
                    self.trigger_notification("Registration failed!")
                case _:
                    logger.debug("Please try again")
                    self.trigger_notification("Please try again!")

        except Exception as e:
            raise e

    '''Default login function'''
    @Slot(str, str)
    def default_login_button(self, username, password):
        with open("/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/resources/default_login/default_username", "r") as file:
            default_username = file.read().strip()
        with open("/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/resources/default_login/default_password", "r") as file:
            default_password = file.read().strip()
        try:
            if not username or not password:
                self.trigger_notification("Please enter default username and password")
                logger.debug("Default username and password were nor entered")
                return
            if password != default_password:
                self.trigger_notification("Default password is not correct")
                logger.debug("Default password is not correct")
                return
            if username != default_username:
                self.trigger_notification("Default username is not correct")
                logger.debug("Default username is not correct")
                return
            self.defaultLoginSuccess.emit()
            self.trigger_notification("Default login successful!")

        except Exception as e:
            logger.debug(f"Error initiating login: {str(e)}")

    '''List all members function'''
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

    '''List active members function'''
    @Slot()
    def list_active_members_gui(self):
        members = []
        try:
            self._user_commands.active_members()

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

    '''Change password function'''
    @Slot(str, str, str)
    def change_password_button(self, current_password, new_password, repeat_password):
        real_password = self._user_commands.get_current_password()
        hash_current_password = self._user_commands.hash_password(current_password)
        if not current_password or not new_password or not repeat_password:
            self.trigger_notification("Please enter current password and new password")
        elif real_password != hash_current_password:
            self.trigger_notification("The entered password is wrong!")
        elif new_password != repeat_password:
            self.trigger_notification("Passwords do not match!")

        else:
            try:
                try:
                    with open("mqtt_responses_cached/general_commands_authorized.csv", "w") as file:
                        file.write("")
                except Exception as e:
                    logger.debug(f"Error editing the file: {str(e)}")
                self._user_commands.change_password(new_password)
                time.sleep(3)
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
                        self.changePasswordSignal.emit()
                    case ResponseCodes.FAILED:
                        logger.debug("Failed to change password")
                        self.trigger_notification("Failed to change password")
                    case _:
                        logger.debug("Please try again")
                        self.trigger_notification("Please try again!")

            except Exception as e:
                logger.debug(f"Error changing password: {e}")


    '''Functions for handling operations on members'''
    '''Function to create a new member'''
    @Slot(str, str)
    def new_member_button(self, name, status):
        # picture_path_server = "/home/ubuntu/images/member@_two" # make it dynamic
        pictures_dir = "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/images"
        full_name = ""
        # self.trigger_notification("Please wait :)")
        try:
            pictures = [
                os.path.join(pictures_dir, f)
                for f in os.listdir(pictures_dir)
                if os.path.isfile(os.path.join(pictures_dir, f)) and f.endswith((".jpg", ".png"))
            ]

            if len(pictures) != 4:
                logger.debug("Exactly 4 pictures are required")

            name_trimmed = name.strip().split(" ")
            values = [x for x in name_trimmed if x]
            name = values[0] if len(values) >= 1 else ""
            surname = values[1] if len(values) >= 2 else ""
            self.picture_path_server = f"/home/ndl/images/{name}_{surname}" #f"/home/ubuntu/images/{name}_{surname}"
            full_name = name + " " + surname

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
            if status == "always":
                status = "authorized"

            self._user_commands.create_new_member(full_name, pictures_dir, self.picture_path_server, status)
            time.sleep(45)
            self.clear_pictures_directory()

            with open(f"mqtt_responses_cached/general_commands_authorized.csv", "r") as file:
                response = file.read().strip()
            try:
                new_member_code = ResponseCodes.string_to_enum(response)
            except Exception:
                new_member_code = ResponseCodes.FAILED

            match new_member_code:
                case ResponseCodes.OK:
                    self.trigger_notification("New member has been created!")
                    self.newMemberSignal.emit()
                    self.trigger_notification("Please reload the page")
                    logger.debug("New member was created")
                case ResponseCodes.FAILED:
                    self.trigger_notification("Failed to create new member")
                    self.newMemberSignal.emit()
                    logger.debug("Failed to create new member")
                case _:
                    self.trigger_notification("Please try again!")
                    logger.debug("Please try again")

        except Exception as e:
            logger.debug(f"Error creating new member: {e}")

    '''Function to edit a member'''
    @Slot(str, str)
    def edit_member_button(self, member_id, new_status):
        try:
            try:
                with open("mqtt_responses_cached/general_commands_authorized.csv", "w") as file:
                    file.write("")
            except Exception as e:
                logger.debug(f"Error editing the file: {str(e)}")

            if new_status == "always":
                new_status = "authorized"
            elif new_status == "no access":
                new_status = "not_authorized"
            else:
                new_status = "temporary"

            self._user_commands.change_member(member_id, new_status)
            time.sleep(3)
            # self.trigger_notification("Please wait :)")
            with open(f"mqtt_responses_cached/general_commands_authorized.csv", "r") as file:
                response = file.read().strip()
            try:
                edit_member_code = ResponseCodes.string_to_enum(response)
            except Exception:
                edit_member_code = ResponseCodes.FAILED

            match edit_member_code:
                case ResponseCodes.OK:
                    self.trigger_notification("Member has been edited!")
                    self.editMemberSignal.emit()
                    logger.debug("Member was edited")
                case ResponseCodes.FAILED:
                    # self.trigger_notification("Failed to edit member")
                    self.editMemberSignal.emit()
                    logger.debug("Failed to edit member")
                case _:
                    self.trigger_notification("Please try again!")
                    logger.debug("Please try again")

        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")

    '''Function to delete a member'''
    @Slot(str)
    def delete_member_button(self, member_id):
        try:
            with open("mqtt_responses_cached/general_commands_authorized.csv", "w") as file:
                file.write("")
            self._user_commands.delete_member(member_id)
            time.sleep(1)
            with open(f"mqtt_responses_cached/general_commands_authorized.csv", "r") as file:
                response = file.read().strip()
            try:
                delete_member_code = ResponseCodes.string_to_enum(response)
            except Exception:
                delete_member_code = ResponseCodes.FAILED

            match delete_member_code:
                case ResponseCodes.OK:
                    self.trigger_notification("Member has been deleted")
                    self.deleteMemberSignal.emit()
                    logger.debug("Member was deleted")
                case ResponseCodes.FAILED:
                    self.trigger_notification("Failed to delete member")
                    logger.debug("Failed to delete member")
                case _:
                    self.trigger_notification("Please try again!")
                    logger.debug("Please try again")

        except Exception as e:
            logger.debug(f"Error editing the file: {str(e)}")


    '''Functions for the lock'''
    '''Reads the lock state from a file, interprets it, and emits a signal'''
    @Slot()
    def lock_listener(self):
        try:
            with open(f"mqtt_responses_cached/magnetic_lock_authorized.csv", "r") as file:
                response = file.read().strip()
            try:
                magnetic_lock_code = MagneticLockResponseCodes.string_to_enum(response)
            except Exception:
                magnetic_lock_code = MagneticLockResponseCodes.CLOSE

            match magnetic_lock_code:
                case MagneticLockResponseCodes.OPEN:
                    logger.debug("Open")
                    self.magneticLockSignal.emit(True)
                case MagneticLockResponseCodes.CLOSE:
                    logger.debug("Close")
                    self.magneticLockSignal.emit(False)
                case _:
                    logger.debug("Please try again")
                    self.magneticLockSignal.emit(False)
        except Exception as e:
            logger.debug(f"Error lock listener: {str(e)}")

    '''Reads the lock state from a file, toggles the state, and sends the new state via MQTT'''
    @Slot()
    def on_lock_unlock(self):
        try:
            with open(f"mqtt_responses_cached/magnetic_lock_authorized.csv", "r") as file:
                response = file.read().strip()
            try:
                if response == "open":
                    magnetic_lock_code = MagneticLockResponseCodes.CLOSE
                else:
                    magnetic_lock_code = MagneticLockResponseCodes.OPEN
            except Exception:
                magnetic_lock_code = MagneticLockResponseCodes.CLOSE

            self._mqtt.send_message(str(magnetic_lock_code), "magnetic_lock")

        except Exception as e:
            logger.debug(f"Error switch_change: {str(e)}")

    '''Sets the lock state manually based on the provided input and emits a signal'''
    @Slot()
    def lock_status_manual(self, status):
        try:
            match status:
                case "open":
                    self.magneticLockSignal.emit(True)
                case _:
                    self.magneticLockSignal.emit(False)
        except Exception as e:
            logger.debug(f"Error lock_status_manual: {str(e)}")


    '''Helper functions'''
    '''Function to get the date'''
    @Slot(int, int, int, int, int)
    def get_date_button(self, year, month, day, hour, minute):
        try:
            my_date = f"{year}-{month}-{day} {hour}:{minute}:00"
            try:
                with open("//Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/date/current_date.txt", "r") as file:
                    current_date = file.read().strip()
            except Exception as e:
                logger.debug(f"Error reading the current date: {str(e)}")
            selected_date = datetime.strptime(my_date, "%Y-%m-%d %H:%M:%S")
            now = datetime.strptime(current_date, "%Y-%m-%d %H:%M:%S")
            if now > selected_date:
                self.trigger_notification("The date is invalid\nSelect the date again")
            else:
                time_format = "%Y-%m-%d %H:%M:%S"
                timestamp = datetime.strptime(my_date, time_format)
                with open("date/selected_datetime.txt", "w") as file:
                    file.write(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
                self.saveDateSignal.emit()
                logger.debug(f"Date and Time saved: {timestamp}")

        except ValueError as e:
            logger.debug(f"Error creating datetime: {e}")
    '''Function to get the current date'''
    @Slot()
    def get_current_datetime(self):
        try:
            # Get the current date and time
            now = datetime.now()
            my_date = now.strftime("%Y-%m-%d %H:%M:%S")

            # Parse the datetime to make sure it's in the correct format
            time_format = "%Y-%m-%d %H:%M:%S"
            timestamp = datetime.strptime(my_date, time_format)

            # Write the timestamp to a file
            with open("date/current_date.txt", "w") as file:
                file.write(timestamp.strftime("%Y-%m-%d %H:%M:%S"))

            logger.debug(f"Date and Time saved: {timestamp}")

        except ValueError as e:
            logger.debug(f"Error creating datetime: {e}")

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

                    if len(pictures) < 4:
                        file_path = os.path.join(self.pictures_dir, f"picture_{len(pictures) + 1}.jpg")
                        cv2.imwrite(file_path, frame)
                        self._picture_count = len(pictures) + 1
                        self.pictureCountChanged.emit()  # Notify QML of the updated count
                        logger.debug(f"Picture saved to {file_path}")
                    else:
                        logger.debug("4 pictures already taken.")
                        break

                # If 'q' is pressed, quit the camera
                elif key == ord('q'):
                    logger.debug("Exiting camera feed.")
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

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

        for i, picture in enumerate(pictures[:4]):  # Only take the latest 4 pictures
            source_path = os.path.join(self.default_camera_dir, picture)
            target_path = os.path.join(self.pictures_dir, f"picture_{i + 1}.jpg")
            move(source_path, target_path)
            logger.debug(f"Moved: {source_path} -> {target_path}")

        self._picture_count = len(pictures[:4])
        if self._picture_count < 4:
            QMessageBox.warning(None, "Incomplete", f"Only {self._picture_count}/4 pictures were found.")
        else:
            QMessageBox.information(None, "Success", "All 4 pictures have been moved to the app folder!")

    @Slot()
    def check_picture_completion(self):
        pictures = [
            f for f in os.listdir(self.pictures_dir) if f.endswith((".jpg", ".png")) and not f.startswith(".")
        ]
        if len(pictures) < 4:
            QMessageBox.warning(None, "Incomplete", f"You only have {len(pictures)}/4 pictures. Please take more!")
        else:
            QMessageBox.information(None, "Complete", "You have taken all 4 pictures!")

