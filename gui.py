import os
import time
from shutil import move

import cv2
from PySide6.QtCore import QObject, Slot, QAbstractListModel, QModelIndex, Qt
from PySide6.QtMultimedia import QMediaCaptureSession, QImageCapture
from PySide6.QtWidgets import QMessageBox, QPushButton
from pyqttoast import Toast, ToastPreset

from data_operations.data import FileTransfer
from mqtt import MQTTServer
from program_codes.general_commands_response_codes import ResponseCodes
from program_codes.login_response_codes import LoginResponseCodes
from PySide6.QtMultimedia import QCamera
from program_codes.new_member_response_codes import NewMemberResponseCodes
from program_codes.register_response_codes import RegisterResponseCodes
from UserCommands import UserCommands
from PySide6.QtCore import Property, Signal
from datetime import datetime
from loguru import logger


class MembersModel(QAbstractListModel):
    def __init__(self, members=None):
        super().__init__()
        self._members = members or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._members)

    def data(self, index, role):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self._members[index.row()]

    def add_member(self, member):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._members.append(member)
        self.endInsertRows()

class GuiBackend(QObject):
    pictureCountChanged = Signal()
    onLoginSuccess = Signal()
    # notificationSignal = Signal(str)
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

    # def show_toast(self, title, text, preset=ToastPreset.SUCCESS, duration=3000):
    #     from PySide6.QtWidgets import QApplication
    #
    #     # Ensure a QApplication exists
    #     if QApplication.instance() is None:
    #         raise RuntimeError("QApplication must be created before using show_toast.")
    #
    #     toast = Toast()
    #     toast.setTitle(title)
    #     toast.setText(text)
    #     toast.applyPreset(preset)
    #     toast.setDuration(duration)
    #     toast.show()

    @Slot()
    def start_camera(self):
        self.picture_count = 0
        self.camera.start()
        print("Camera started. Ready to take pictures.")

    @Slot()
    def take_picture(self):
        """Take a picture and save it."""
        try:
            cap = cv2.VideoCapture(0)  # Open the default camera
            if not cap.isOpened():
                print("Error: Cannot access the camera.")
                return

            # cap.set(cv2.CAP_PROP_BRIGHTNESS, 10)
            # cap.set(cv2.CAP_PROP_CONTRAST, 0.5)
            # cap.set(cv2.CAP_PROP_EXPOSURE, 5)

            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame.")
                return

            if self._picture_count < 6:
                file_path = os.path.join(self.pictures_dir, f"picture_{self._picture_count + 1}.jpg")
                cv2.imwrite(file_path, frame)
                self._picture_count += 1
                self.pictureCountChanged.emit()  # Notify QML of the updated count
                print(f"Picture {self._picture_count} saved to {file_path}")
            else:
                print("6 pictures already taken.")
        finally:
            cap.release()
            cv2.destroyAllWindows()

    @Slot()
    def check_completion(self):
        """Verify if 6 pictures have been taken."""
        if self.picture_count < 6:
            print(f"Only {self.picture_count}/6 pictures taken.")
        else:
            print("All 6 pictures have been taken.")

    def set_picture_count(self, count):
        if self._picture_count != count:
            self._picture_count = count
            self.pictureCountChanged.emit()

    # @Slot(str)
    # def show_notification(self, message: str):
    #     print(f"Emitting notification: {message}")  # Debug print
    #     self.notificationSignal.emit(message)

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
            print(f"Moved: {source_path} -> {target_path}")

        self._picture_count = len(pictures[:6])
        if self._picture_count < 6:
            QMessageBox.warning(None, "Incomplete", f"Only {self._picture_count}/6 pictures were found.")
        else:
            QMessageBox.information(None, "Success", "All 6 pictures have been moved to the app folder!")

    @Slot()
    def check_picture_completion(self):
        """Ensure 6 pictures are available in the app's folder."""
        pictures = [
            f for f in os.listdir(self.pictures_dir) if f.endswith((".jpg", ".png")) and not f.startswith(".")
        ]
        if len(pictures) < 6:
            QMessageBox.warning(None, "Incomplete", f"You only have {len(pictures)}/6 pictures. Please take more!")
        else:
            QMessageBox.information(None, "Complete", "You have taken all 6 pictures!")

    @Slot(str, str)
    def login_button(self, username, password):
        # call login from UserCommands
        try:
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
                    #go to mainPage

                case LoginResponseCodes.FAILED:
                    logger.debug("Login failed")
                    #popup notification

                case _:
                    logger.debug("Please try again")

        except Exception as e:
            logger.debug(f"Error reading login response: {str(e)}")

    @Slot(str, str, str)
    def register_button(self, username, password, repeat_password):
        try:
            self._user_commands.register(username, password, repeat_password)
        except Exception as e:
            print(f"Error initiating register: {str(e)}")
            return

        # sleep(3) "Please wait"
        # self.show_notification(self, "Please wait :)")
        time.sleep(3)

        # check the register response using csv file and convert it to enum using string_to_enum
        try:
            with open("mqtt_responses_cached/register_authorized.csv", "r") as file:
                response = file.read().strip()
                register_code = RegisterResponseCodes.string_to_enum(response)

                if register_code == RegisterResponseCodes.OK:
                    logger.debug("Registration successful")
                    # self.show_notification(self, "Registration successful")
                    self.stackView.push(self.mainPage)
                elif register_code == RegisterResponseCodes.FAILED:
                    logger.debug("Registration failed")
                    # self.show_notification(self, "Registration failed")
                else:
                    # self.show_notification(self, "Please try again")
                    logger.debug("Please try again")

        except Exception as e:
            raise e

    @Slot()
    def forgot_password_button(self, msg):
        try:
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

    @Slot(str, str)
    def new_member_button(self, name, status):
        try:
            pictures_dir = "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/images"
            pictures = [
                os.path.join(pictures_dir, f)
                for f in os.listdir(pictures_dir)
                if os.path.isfile(os.path.join(pictures_dir, f)) and f.endswith((".jpg", ".png"))
            ]

            if len(pictures) != 6:
                raise Exception("You must have exactly 6 pictures before creating a new member.")

            name_trimmed = name.strip().split(" ")
            values = [x for x in name_trimmed if x]
            name = values[0] if len(values) == 1 else ""
            surname = values[1] if len(values) == 2 else ""

            try:
                file_transfer = FileTransfer(name, surname, pictures_dir)
                file_transfer.file_transfer()
            except Exception as e:
                raise Exception(e)

            # Call create_new_member in UserCommands
            self._user_commands.create_new_member(name, pictures, status, None)
            logger.debug(f"New member {name} created with status {status}.")

        except Exception as e:
            logger.debug(f"Error creating new member: {e}")

        try:
            with open("mqtt_responses_cached/add_member_authorized.csv", "r") as file:
                response = file.read().strip()
                new_member_code = NewMemberResponseCodes.string_to_enum(response)

                if new_member_code == NewMemberResponseCodes.OK:
                    # self.message_label.setText("New member was created!")
                    logger.debug("New member was created")
                    # self.members_model.add_member({"name": name, "status": status})
                    # # Emit signal to notify QML
                    # self.memberAdded.emit(name, status)
                elif new_member_code == NewMemberResponseCodes.FAILED:
                    logger.debug("New member was not created")
                    # self.message_label.setText("Failed to create a new member")
                else:
                    logger.debug("Please try again")
                    # self.message_label.setText("Please try again")

        except Exception as e:
            raise e


    def edit_member_button(self):
        pass


    def delete_member_button(self):
        pass

    def list_all_members_gui(self):
        pass

    def list_active_members_gui(self):
        pass



    #here I check the general_commands_authorized file
    @Slot(str, str, str)
    def change_password_button(self, current_password, new_password, repeat_password, msg):
        try:
            real_password = self._user_commands.get_current_password()
            hash_current_password = self._user_commands.hash_password(current_password)
            if real_password != hash_current_password:
                logger.debug("The entered password is wrong")

            if new_password != repeat_password:
                logger.debug("Passwords do not match")

            self._user_commands.change_password(new_password)
            logger.debug(f"Password has been changed")

        except Exception as e:
            logger.debug(f"Error changing password: {e}")

        try:
            response = msg.payload.decode()
            if response.lower() == "ok":
                logger.debug("The password has been changed")
            else:
                logger.debug("Please try again")

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

