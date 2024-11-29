import os
import sys
import time
import subprocess
from shutil import move

import cv2
from PySide6.QtCore import QObject, Slot, QTimer, Property
from PySide6.QtMultimedia import QCamera, QMediaCaptureSession, QImageCapture
from PySide6.QtWidgets import QMessageBox
from mqtt import MQTTServer
from program_codes.login_response_codes import LoginResponseCodes
from PySide6.QtMultimedia import QCamera
from program_codes.new_member_response_codes import NewMemberResponseCodes
from program_codes.register_response_codes import RegisterResponseCodes
from UserCommands import UserCommands
from PySide6.QtCore import Property, Signal


class GuiBackend(QObject):
    pictureCountChanged = Signal()
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

    @Property(int, notify=pictureCountChanged)
    def pictureCount(self):
        return self._picture_count

    def _save_picture(self, id, preview, file_path):
        """Handle picture saving."""
        print(f"Picture saved to {file_path}")

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


    # @Slot()
    # def open_device_camera(self):
    #     """Open the device's default camera application."""
    #     try:
    #         if sys.platform == "darwin":  # macOS
    #             subprocess.run(["open", "-a", "Photo Booth"])  # Replace with your default camera app
    #         elif sys.platform == "win32":  # Windows
    #             subprocess.run(["start", "microsoft.windows.camera:"], shell=True)
    #         elif sys.platform.startswith("linux"):  # Linux
    #             subprocess.run(["cheese"])  # Cheese is a common Linux camera app
    #         else:
    #             QMessageBox.critical(None, "Error", "Unsupported platform")
    #     except Exception as e:
    #         QMessageBox.critical(None, "Error", f"Failed to open camera: {e}")

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

    # @Slot()
    # def capture_pictures(self):
    #     try:
    #         cap = cv2.VideoCapture(0)  # Open the default camera
    #         if not cap.isOpened():
    #             print("Error: Cannot access the camera.")
    #             return
    #
    #         print("Press 'Space' to take a picture and 'ESC' to exit.")
    #         self._picture_count = 0
    #
    #         while self._picture_count < 6:
    #             ret, frame = cap.read()
    #             if not ret:
    #                 print("Failed to capture frame. Exiting.")
    #                 break
    #
    #             cv2.imshow("Camera", frame)
    #             key = cv2.waitKey(1)
    #
    #             if key == 27:  # ESC key to exit
    #                 break
    #             elif key == 32:  # Space key to take a picture
    #                 file_path = os.path.join(self.pictures_dir, f"picture_{self._picture_count + 1}.jpg")
    #                 cv2.imwrite(file_path, frame)
    #                 self._picture_count += 1
    #                 print(f"Picture {self._picture_count} saved to {file_path}")
    #
    #     except KeyboardInterrupt:
    #         print("Capture interrupted by user.")
    #     finally:
    #         cap.release()
    #         cv2.destroyAllWindows()
    #         print("Camera closed.")

    @staticmethod
    def show_notification(self, message: str):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Notification")
        msg_box.setText(message)
        msg_box.setStyleSheet("QLabel {min-width: 150px;}")
        msg_box.show()
        QTimer.singleShot(3000, msg_box.close)

    def set_stack_view(self, stack_view):
        self.stackView = stack_view


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
                    # self.show_notification(self,"Login successful")
                    self.stackView.push(self.mainPage)
                elif login_code == LoginResponseCodes.FAILED:
                    print("Login failed")
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
        self.show_notification(self, "Please wait :)")
        time.sleep(3)

        # check the register response using csv file and convert it to enum using string_to_enum
        try:
            with open("mqtt_responses_cached/register_authorized.csv", "r") as file:
                response = file.read().strip()
                register_code = RegisterResponseCodes.string_to_enum(response)

                if register_code == RegisterResponseCodes.OK:
                    print("Registration successful")
                    self.show_notification(self, "Registration successful")
                    # self.stackView.push(self.mainPage)
                elif register_code == RegisterResponseCodes.FAILED:
                    print("Registration failed")
                    self.show_notification(self, "Registration failed")
                else:
                    self.show_notification(self, "Please try again")
                    print("Please try again")

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
        time.sleep(3)

        try:
            with open("mqtt_responses_cached/new_member_authorized.csv", "r") as file:
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