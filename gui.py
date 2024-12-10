import os
import time
from shutil import move

import cv2
from PySide6.QtCore import QObject, Slot, QAbstractListModel, QModelIndex, Qt
from PySide6.QtMultimedia import QMediaCaptureSession, QImageCapture
from PySide6.QtWidgets import QMessageBox

from data_operations.data import FileTransfer
from mqtt import MQTTServer
from program_codes.login_response_codes import LoginResponseCodes
from PySide6.QtMultimedia import QCamera
from program_codes.new_member_response_codes import NewMemberResponseCodes
from program_codes.register_response_codes import RegisterResponseCodes
from UserCommands import UserCommands
from PySide6.QtCore import Property, Signal
from datetime import datetime

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
    loginSuccess = Signal()
    # notificationSignal = Signal(str)
    def __init__(self, mqtt: MQTTServer):
        super().__init__()
        self._user_commands = UserCommands(mqtt)
        self._picture_count = 0
        self.pictures_dir = "/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/images"

        if not os.path.exists(self.pictures_dir):
            os.makedirs(self.pictures_dir)

        #new:
        # Camera setup
        self.camera = QCamera()
        self.capture_session = QMediaCaptureSession()
        self.image_capture = QImageCapture(self.camera)

        # Configure capture session
        self.capture_session.setCamera(self.camera)
        self.capture_session.setImageCapture(self.image_capture)

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
    def login(self, username, password):
        # call login from UserCommands
        try:
            self._user_commands.login(username, password)
        except Exception as e:
            print(f"Error initiating login: {str(e)}")
            return

        # sleep(3) "Please wait"
        # self.show_notification(self, "Please wait :)")
        time.sleep(3)

        # check the login response using csv file and convert it to enum using string_to_enum
        try:
            with open("mqtt_responses_cached/login_authorized.csv", "r") as file:
                response = file.read().strip()
                login_code = LoginResponseCodes.string_to_enum(response)

                if login_code == LoginResponseCodes.OK:
                    print("Login successful")
                    # self.notificationSignal.emit("Login successful")
                    self.loginSuccess.emit()
                elif login_code == LoginResponseCodes.FAILED:
                    print("Login failed")
                    # self.notificationSignal.emit("Login failed")
                    # self.show_notification(self, "Login failed")
                    # self.stack_view.push("mainPage")
                else:
                    # self.show_notification(self, "Please try again")
                    print("Please try again")

        except Exception as e:
            raise e

    @Slot(str, str, str)
    def register(self, username, password, repeat_password):
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
                    print("Registration successful")
                    # self.show_notification(self, "Registration successful")
                    self.stackView.push(self.mainPage)
                elif register_code == RegisterResponseCodes.FAILED:
                    print("Registration failed")
                    # self.show_notification(self, "Registration failed")
                else:
                    # self.show_notification(self, "Please try again")
                    print("Please try again")

        except Exception as e:
            raise e


    def forgot_password(self):
        pass

    @Slot(str, str)
    def new_member(self, name, status):
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
            print(f"New member {name} created with status {status}.")

        except Exception as e:
            print(f"Error creating new member: {e}")

        try:
            with open("mqtt_responses_cached/add_member_response.csv", "r") as file:
                response = file.read().strip()
                new_member_code = NewMemberResponseCodes.string_to_enum(response)

                if new_member_code == NewMemberResponseCodes.OK:
                    # self.message_label.setText("New member was created!")
                    print("New member was created")
                    # self.members_model.add_member({"name": name, "status": status})
                    # # Emit signal to notify QML
                    # self.memberAdded.emit(name, status)
                elif new_member_code == NewMemberResponseCodes.FAILED:
                    print("New member was not created")
                    # self.message_label.setText("Failed to create a new member")
                else:
                    print("Please try again")
                    # self.message_label.setText("Please try again")

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

    def delete_user(self):
        pass

    def change_password(self, current_password, new_password, repeat_password):
        if new_password != repeat_password:
            print("Passwords do not match")

    @Slot(int, int, int, int, int)
    def get_date(self, year, month, day, hour, minute):
        try:
            my_date = f"{year}-{month}-{day} {hour}:{minute}:00"
            time_format = "%Y-%m-%d %H:%M:%S"
            timestamp = datetime.strptime(my_date, time_format)
            with open("date/selected_datetime.txt", "w") as file:
                file.write(timestamp.strftime("%Y-%m-%d %H:%M:%S"))

            print(f"Date and Time saved: {timestamp}")
        except ValueError as e:
            print(f"Error creating datetime: {e}")

