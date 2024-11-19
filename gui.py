import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

#QA do I need this class?

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

    def login(self):
        pass
        # read the input fields
        # call login from UserCommands
        # sleep(5) "Please wait"
        # check the login response using csv file and convert it to enum using string_to_enum

