from PySide6.QtWidgets import QMessageBox

class Notifications(QMessageBox):

    def show_login_failed_popup(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Login Failed")
        msg_box.setText("Invalid username or password. Please try again.")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

